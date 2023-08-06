"""
Turn json files into numpy files with xyz values, atom type and chemical shielding values into:
prefix_xyz.npy, prefix_points.npy and prefix_y.npy
IMPORTANT NOTE: the order of channels are H, C, O, N
"""
import json
import os
import numpy as np


def json_to_numpy(json_folder, np_folder, xyz_files, prefix, atom_type='H', k=320):
    
    """
    Turn json files to numpy files
    input: json_folder, the json file folder
           np_folder, the numpy output file folder
           xyz_files, list of the input files (to dictate the order they are added)
           prefix, the prefix string of the numpy files "$prefix$_xyz.npy"
           atom_type, the atom type of processing, 'H', 'C', 'O' or 'N'
           k, number of nearest atoms, default 320

    Modified: added np_folder for the np files to be saved to
    """
    xyz_n = []
    points_n = []
    y = []
    files = []
    #num_folder = sum([len(d) for r, d, f in os.walk(json_folder)])
    num_folder = len(xyz_files)
    for i in range(num_folder):
    #   folder_path = json_folder + "/" + str(i)
        filename, fileext = xyz_files[i].split('.')
        folder_path = os.path.join(json_folder, filename)
        num_files = sum([len(f) for r, d, f in os.walk(folder_path)])
        for j in range(num_files):
            files.append(os.path.join(folder_path, str(j) + ".json"))
    for f in files:
        #print(f)
        with open(f, 'r') as ff:
            lines = json.load(ff)
        if lines[0][0] != atom_type:
            continue
        y.append(lines[0][-1])
        xyz = []
        points = []
        # Note: the order of channels are H, C, O and N but not H, C, N, O currently
        for l in range(1, k+1):
            xyz.append(lines[l][1:4])
            if lines[l][0] == "H":
                points.append([1,0,0,0])
            elif lines[l][0] == "C":
                points.append([0,1,0,0])
            elif lines[l][0] == "O":
                points.append([0,0,1,0])
            else:
                points.append([0,0,0,1])
        xyz_n.append(xyz)
        points_n.append(points)
    np.save(os.path.join(np_folder, prefix + "_xyz"), xyz_n)
    np.save(os.path.join(np_folder, prefix + "_points"), points_n)
    np.save(os.path.join(np_folder, prefix + "_y"), y)

