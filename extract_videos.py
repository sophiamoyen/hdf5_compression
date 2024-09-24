import h5py
import numpy as np
import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
import json
import glob
import cv2

in_folder = "./original_files/"
out_folder = "./interactive_recordings_just_videos/"



os.makedirs(os.path.dirname(out_folder), exist_ok=True)
files = [y for y in glob.glob(os.path.join(in_folder, '**/*.h5'), recursive=True) if isfile(y)]

print(f"found {len(files)}")



def compress_and_store_video(video_array, file_name, file_type,fps):

    # Get video properties
    num_frames, height, width, channels = video_array.shape

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Using XVID codec, you can choose other codecs like 'mp4v', 'X264', etc.
    # video_name = os.path.join(out_folder, file_name.split(".")[0] + "_" + file_type ) 
    video_name = "."  +file_name.split(".")[1] + "_" + file_type 
    print(video_name)
    out = cv2.VideoWriter(video_name + '.avi', fourcc, fps, (width, height))

    # Write each frame to the video writer
    for i in range(num_frames):
        out.write(video_array[i])

    # Release the VideoWriter
    out.release()

    



def copy_dataset(name, demo, compressed, f):
    d = demo[name]
    compression_list = ['agent_view_right', 'fixed_view_right']
    if name not in compression_list:
        compressed.create_dataset(name, data=d)
    else:
        compress_and_store_video(d, file_name = f, file_type = name, fps=30)
        

for f in files:
    new_path = f.replace(in_folder, out_folder).replace('.h5', '.hdf5')
    os.makedirs(os.path.dirname(new_path), exist_ok=True)

    with h5py.File(f, 'r') as demo:    
        # print(demo.keys())
        with h5py.File(new_path, 'w') as compressed:
            for n in ['q', 'dq', 'tau', 'positions', 'orientations', 'gripper', 'target_gripper', 'target_orientations', 'target_positions', 'agent_view_right', 'fixed_view_right']:
                copy_dataset(n, demo, compressed, new_path)