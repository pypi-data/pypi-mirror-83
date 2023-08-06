hot_water: a residual deep learning model for predicting water hot-spots on protein surfaces. 
####################################################################################################################################################

How it works
=============

Supply a pdb file (or just the accession code) and rank the water molecules within it or scan the surface of the whole protein for most likely water hot spots. 

Installation
============

Note: This tool relies on EDTSurf, therefore runs only on Linux. 
If you have a linux system, install via pip from `PyPi <https://pypi.org/project/hotWater/>`_
(recommended):

.. code-block:: bash

    $ pip2 install --user hotWater


If your system lacks pip, `install it first <https://www.makeuseof.com/tag/install-pip-for-python/>`_. 


Python version
--------------

The tool was developed using Python 2.7.




Usage
=====


Python 2.7 shell


.. code-block:: bash

    >>> from hotWater import *
    >>> rank_waters('3m1k')
    Creating mesh around protein surface using EDTSurf
	[...other output messages...]
    Ranked water positions along with scores have been written out to a file



For the scan mode, you need to use a high performance server (depending on size of protein, can require up to 64GB RAM per core). You will be testing several million of points so please be aware that this will take some time. If your job dies (for e.g. due to insufficient memory resources), rerun it (using fewer threads) in the same folder. The calculation will restart from the last checkpoint. 

.. code-block:: bash

    >>> scan_surface('3m1k', threads=4, threshold=0.999)

The points predicted above the threshold will be written out to a PDB file ('<input>_predicted_waters.pdb'). You can append this output with the original PDB for viewing in pymol etc. The predicted waters are chain 'W'. If you wish to see more predictions, decrease the 'threshold' parameter (hint - not too drastically, a threshold of 0.99 will already yield several thousands of positive predictions and any threshold below 0.9 will yield very many false positive predictions). If you wish to remove excess waters (positively predicted water molecules that clash with one another), run:

.. code-block:: bash

    >>> cluster_predicted_waters('3m1k_predicted_waters.pdb', threshold = 1.4)

Licence
-------

MIT


Authors
-------

`Jan Zaucha <trelek2@gmail.com>`_
