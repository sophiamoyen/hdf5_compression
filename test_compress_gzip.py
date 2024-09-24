import h5py
import numpy as np
import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
import json
import glob

in_folder = "./original_files/"
out_folder = "./interactive_recordings_small/"
downsampling = 15


os.makedirs(os.path.dirname(out_folder), exist_ok=True)
files = [y for y in glob.glob(os.path.join(in_folder, '**/*.h5'), recursive=True) if isfile(y)]

print(f"found {len(files)}")

def copy_dataset(name, demo, compressed):
    d = demo[name]
    compression_list = ['agent_view_left', 'fixed_view_left']
    if name not in compression_list:
        compressed.create_dataset(name, data=d)
    else:
        compressed.create_dataset(name, data=d, compression="gzip", dtype=np.uint8, compression_opts = 9)

for f in files:
    new_path = f.replace(in_folder, out_folder).replace('.h5', '.hdf5')
    os.makedirs(os.path.dirname(new_path), exist_ok=True)

    with h5py.File(f, 'r') as demo:    
        # print(demo.keys())
        with h5py.File(new_path, 'w') as compressed:
            for n in ['q', 'dq', 'tau', 'positions', 'orientations', 'gripper', 'target_gripper', 'target_orientations', 'target_positions', 'agent_view_left', 'fixed_view_left']:
                copy_dataset(n, demo, compressed)