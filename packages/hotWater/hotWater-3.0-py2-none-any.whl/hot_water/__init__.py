'''
@author: Jan Zaucha. Created on 23 Jan 2020

Purpose: To predict water hot spots on the surface of proteins

MAIN methods here 
'''

import sys
from Bio.PDB import *
from h2o_bind import *
import numpy as np
import random
import time
import matplotlib as mpl
mpl.use('pdf')
import matplotlib.pyplot as plt
from numpy import linalg as LA
from model import *
import operator


def worker_task_ply():
    while True:
        #file_,i,model = task_queue_ply.get()
        print('trying to get data to process')
        to_process = task_queue_ply.get()
        print ('got data to process')
        if to_process is None:
            task_queue_ply.task_done()
            print ('breaking')
            break
        print("processing %s,%s,%s" % (to_process['file_'],to_process['model'],to_process['i']))
        process_layer(to_process['file_'],to_process['model'],to_process['i'])
        task_queue_ply.task_done()



def process_layers(file_, model, k,threads=4):
    global task_queue_ply
    task_queue_ply = JoinableQueue()
    for i in range(threads):
        print("starting thread %s" % i)
        p = Process(target=worker_task_ply)
        p.start()

    for j in range(k):
        #print(j,file_,model)
        #to_process = {'file_':file_,'model':model,'i':j}
        task_queue_ply.put({'file_':file_,'model':model,'i':j})

    #Add a sentinal task for each child so that they know when to terminate
    for thread in range(threads):
        task_queue_ply.put(None)

    task_queue_ply.join()
    task_queue_ply.close()
    return True

def process_layer(file_,model, i):
    print ("processing layer %s" % i)
    vectors =[]
    b_values = []
    #model = pickle.load(open(model, 'rb'))
    #print ("loaded model in task %s" % i)
    if os.path.isfile("%s_%s_processed.pickle" % (file_.split('.')[0], i+1)):
        print ("%s_%s_processed.pickle is present" % (file_.split('.')[0], i+1) )
            return True
    data = pickle.load(open("%s_%s.pickle" % (file_.split('.')[0], i+1), 'rb'))
    vectors, b_values ,original_coords= process_waters(data['non_waters'], vectors, b_values, output_original_coordinates= True)
    #y_pred = model['model'].predict({'atom_vectors':np.array(vectors) ,'beta':np.array(b_values)}).ravel().tolist()
    data_processed = {'vectors':vectors, 'b_values':b_values ,'original_coords':original_coords}
    pickle.dump(data_processed, open("%s_%s_processed.pickle" % (file_.split('.')[0], i+1), 'wb'),protocol=pickle.HIGHEST_PROTOCOL)


def define_vertices_for_waters(coordinates, real_waters, name, print_angles=True):
    '''
    real waters must be an array of vectors
    This identifies for all waters the closes vertices
    TODO : rewrite this function for onion scheme- check if real waters are no further than grid size away from mesh points, what is the average distance, how many are too far? are they near the centre?
    mesh layer: proportion of total waters in each onion layer
    '''
    print ('Checking occupied water vertcies')
    #proteins_centre = Vector(np.array([i.get_array() for i in coordinates]).mean(0).tolist()) ## this is completele unnecessary?
    occupied_by_waters = set()
    water_coordinates = []
    mesh_layer = len(coordinates)*[0]
    captured = []
    coord_trie =  cKDTree(coordinates[-1,:,:])
    grid_sizes = []
    for i in range(100):
        grid_sizes.append(coord_trie.query(coordinates[-1,random.choice(range(len(coordinates))),:], k=2)[0][1])
    grid_size = np.mean(grid_sizes)
    print ("Maximal grid size is about %s" % grid_size)
    for real_water in real_waters:
        dist2mesh = []
        index_min = []
        original_coord = []
        for j in range(len(coordinates)):
            distances = coordinates[j]-real_water.get_array() 
            norms = LA.norm(distances, axis=1).tolist()
            assert (len(norms)==len(coordinates[j]))
            index_min.append(norms.index(min(norms)))
            dist2mesh.append(min(norms))
            original_coord.append(coordinates[0][norms.index(min(norms))])
        if min(dist2mesh) < grid_size*np.sqrt(3):
            captured.append(True)
            occupied_by_waters.add(index_min[dist2mesh.index(min(dist2mesh))])
            mesh_layer[dist2mesh.index(min(dist2mesh))]+=1
            print("water captured %s, distance from mesh %s, index %s, original_coord %s" % (real_water.get_array(),min(dist2mesh), index_min[dist2mesh.index(min(dist2mesh))], original_coord[dist2mesh.index(min(dist2mesh))] ))
        else:
            print("water missed %s, distance from mesh %s" % (real_water.get_array(),min(dist2mesh) ) )
            captured.append(False)
    if captured:
        frac_captured = sum(captured)/float(len(captured))
    else:
        frac_captured=1.0
    return occupied_by_waters, frac_captured, np.array(mesh_layer)/float(sum(mesh_layer)), captured



def download_pdb_file(pdbcode):
    if os.path.isfile('%s.pdb' % pdbcode): 
        print ("Creating mesh around protein surface using EDTSurf")
        os.system('./EDTSurf -i %s.pdb -o %s -f 20 -h 2' % (pdbcode, pdbcode))
    else:
        try:
            print("Downloading PDB file from RCSB PDB: accession no. %s" % pdbcode)
            url = "http://files.rcsb.org/download/%s.pdb.gz" % pdbcode
            fname = '%s.pdb' % pdbcode
            r = requests.get(url)
            num_bytes = open('%spdb.gz' % pdbcode , 'wb').write(r.content)
            with gzip.open('%spdb.gz' % pdbcode, 'rb') as f_in:
                with open('%s.pdb' % pdbcode, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        except:
            print("Error: Downloading/unpacking %s failed; skipping..." % pdbcode)
            sys.exit(0)


def scan_surface(pdbcode, model_='water_hot_spots_adv_new.h5', threads=4, threshold=0.99):
    '''
    This fills the file white
    '''
    download_pdb_file(pdbcode)
    model = water_glue_model(L=30,K=4, n=1).base_model
    model.load_weights(model_)
    mesh, data, atoms = read_surface("%s.ply" % pdbcode)
    data['waters'] = OrderedDict(data['waters'])
    vertices_occupied, frac_captured, mesh_layer, captured = define_vertices_for_waters(mesh, data['waters'],pdbcode)
    if predict and not load_:
        waters, non_waters, waters_rejected, total_waters = parse_waters(atoms, data['waters'], print_nonwaters=False, generate_nonwaters = True, nonwater_positions = mesh, all_nonwaters = pdbcode)
        predictions = np.zeros(np.array(mesh).shape[:2])
        process_layers("%s.ply" % pdbcode, model_, np.array(mesh).shape[0],threads=4)
        for i in range(0, np.array(mesh).shape[0]):
            print ("Trying command pickle load open %s_%s_processed.pickle" % (pdbcode, i+1))
            data_processed = pickle.load(open("%s_%s_processed.pickle" % (pdbcode, i+1), 'rb'))
            predictions[i,:] = model.predict({'atom_vectors':np.array(data_processed['vectors']) ,'beta':np.array(data_processed['b_values'])}).ravel().tolist()
        collapsed_predictions = predictions.max(axis=0)
        data = {'predictions':predictions, 'mesh':mesh}
        pickle.dump(data, open("%s_pred.pickle" % pdbcode, 'wb'),protocol=pickle.HIGHEST_PROTOCOL)
    elif predict and load_:
        data2 = pickle.load(open("%s_pred.pickle" % pdbcode, 'rb'))
        print("Finished loading precalculated predictions")
        # get positions predicted as water (only maximum onion layer for each mesh point above chosen threshold)
        max_pred = np.amax(data2['predictions'],axis=0) # this is the maximum prediction at each point on surface
        arg_max =data2['predictions'].argmax(axis=0) # this is the index of the maximum points
        meets_threshold =max_pred>threshold
        index_if_meets_threshold = arg_max[meets_threshold]
        predicted_waters = []
        for i in range(data2['mesh'][:,meets_threshold].shape[1]):
            predicted_waters.append(data2['mesh'][:,meets_threshold][index_if_meets_threshold[i]][i])
        print_nonwaters_as_pdb(None, predicted_waters, pdbcode)
        print ('Finished printing predicted waters to pdb')
        collapsed_predictions = data2['predictions'].max(axis=0)
    handle.close()
    handle2.close()


def rank_waters(pdbcode, model_='water_hot_spots_adv_new.h5'):
    download_pdb_file(pdbcode)
    model = water_glue_model(L=30,K=4, n=1).base_model
    model.load_weights(model_)
    waters, non_waters, waters_rejected, total_waters = parse_waters(atoms, data['waters'], print_nonwaters=False, generate_nonwaters = False)
    vectors =[]
    b_values = []
    vectors, b_values ,original_coords= process_waters(data['waters'], vectors, b_values, output_original_coordinates= True)
    predictions = model.predict({'atom_vectors':np.array(vectors) ,'beta':np.array(b_values)}).ravel().tolist()
    results  =  {}
    for i,j in zip(predictions,original_coords):
        results[j]=i
    results = sorted(results.items(), key=operator.itemgetter(1))[::-1]
    handle = open('%s_water_ranking.txt' % pdbcode)
    handle.write('Water-position\tprediction-score\n')
    for i in results:
        handle.write('%s\t%s\n' % (i[0],i[1]))
    handle.close()
    print ("Ranked waters positions along with score have been written out to file")

