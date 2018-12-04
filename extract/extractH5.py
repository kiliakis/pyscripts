import h5py
import sys
import numpy as np

with h5py.File(sys.argv[1], 'r') as hf:
    print 'List of arrays in this file: \n', hf.keys()
    # group = hf.get('Slices')
    # data = hf["Slices/n_macroparticles"][:10]
    print hf["Beam/n_macroparticles_alive"][:]
    print hf["Beam/mean_dt"][:]
    print hf["Beam/mean_dE"][:]
    # print data
    # print 'List of items in the group', group.items()
    # np_data = np.array(data)
    # print 'Shape of the array dataset_1: \n', np_data.shape
