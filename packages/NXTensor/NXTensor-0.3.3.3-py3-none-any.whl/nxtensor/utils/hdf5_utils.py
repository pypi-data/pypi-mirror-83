

import h5py
import numpy as np


def write_ndarray_to_hdf5(file_path: str, ndarray: np.ndarray) -> None:
    hdf5_file = h5py.File(file_path, 'w')
    hdf5_file.create_dataset('dataset', data=ndarray)
    hdf5_file.close()


def read_ndarray_from_hdf5(file_path: str) -> np.ndarray:
    hdf5_file = h5py.File(file_path, 'r')
    data = hdf5_file.get('dataset')
    return np.array(data)
