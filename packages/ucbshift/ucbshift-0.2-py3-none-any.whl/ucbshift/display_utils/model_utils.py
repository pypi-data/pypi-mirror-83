import numpy as np
import keras
import os
from keras.models import load_model
from ucbshift.data_processing.xyz_to_json import xyz_to_json
from ucbshift.data_processing.json_to_numpy import json_to_numpy
from ucbshift.data_processing.data_aug import rot_aug_data
from ucbshift.data_processing.density_gen import generate_density
from ucbshift.webapp_setup.manage_data_folders import get_path

INPUT_DIRECTORY = "input_xyz"
SAVED_XYZ_DIRECTORY = "saved_xyz"
PRED_XYZ_DIRECTORY = "pred_xyz"
JSON_DIRECTORY = "json"
PREPROCESS_DIRECTORY = "preprocess"
DENSITYGEN_DIRECTORY = "density_gen"
PREDICTION_DIRECTORY = "prediction"
MODEL_DIRECTORY = "models"

def convert_all_to_json(xyz_files, test=False):
    """
    Runs preprocessing of xyz files
    Input: xyz_files, list of the xyz files to preprocess
    """
    dirs = [SAVED_XYZ_DIRECTORY, JSON_DIRECTORY]
    if test:
        used_directories = [os.path.join('.', dir_) for dir_ in dirs]
    else:
        used_directories = list(map(get_path, dirs))

    xyz_to_json(used_directories[0], used_directories[1], xyz_files)

def convert_json_to_numpy(xyz_files, test=False):
    """
    Runs preprocessing of json files
    Input: xyz_files, list of the files to continue preprocessing
    """
    dirs = [JSON_DIRECTORY, PREPROCESS_DIRECTORY]
    if test:
        used_directories = [os.path.join('.', dir_) for dir_ in dirs]
    else:
        used_directories = list(map(get_path, dirs))

    for atom_type in ["H", "C", "N", "O"]:
        json_to_numpy(used_directories[0], used_directories[1], xyz_files, "test_" + atom_type, atom_type)

def data_augmentation(atom_type, test=False):
    """
    Runs data augmentation of the preprocessed files
    Input: atom_type, the element type to run data_augmentation on
                      (to prevent calling data_aug on elements not found)
    """
    dirs = [PREPROCESS_DIRECTORY]
    if test:
        used_directories = [os.path.join('.', dir_) for dir_ in dirs]
    else:
        used_directories = list(map(get_path, dirs))

    rot_aug_data(used_directories[0], "test_" + atom_type + "_xyz.npy", "test_" + atom_type + "_aug_xyz")

def density_generation(atom_type, test=False):
    """
    Runs density generation of the data
    Input: atom_type, the element type to run density generation on
    """
    dirs = [PREPROCESS_DIRECTORY, DENSITYGEN_DIRECTORY]
    if test:
        used_directories = [os.path.join('.', dir_) for dir_ in dirs]
    else:
        used_directories = list(map(get_path, dirs))

    generate_density(used_directories[0], used_directories[1], "test_" + atom_type, 1)

def predict(model_name, atom_type, test=False):
    """
    Generate an inference of the atom type requested
    Inputs: atom_type, a letter denoting the atom type chosen for inference
    """
    dirs = [PREPROCESS_DIRECTORY, DENSITYGEN_DIRECTORY, MODEL_DIRECTORY, PREDICTION_DIRECTORY]
    if test:
        used_directories = [os.path.join('.', dir_) for dir_ in dirs]
    else:
        used_directories = list(map(get_path, dirs))

    #Metadata: molecule size, number of molecules trained on, mean, scale, std
    metadata = {
        'H': (76214, 25.19, 1, 4.05),  # not excluded 40 outliers yet
        'C': (58148, 59.08, 10, 53.97),
        'O': (25924, -64.73, 40, 198.8),
        'N': (27814, -13.68, 30, 120.7)
        }
    mean = metadata[atom_type][1]
    scale = metadata[atom_type][2]
    test_y = np.load(os.path.join(used_directories[0], "test_" + atom_type + "_y.npy"))
    size = test_y.shape[0]
    test_x = np.zeros((size*8, 16, 16, 16, 20), dtype=np.float16)
    for i in range(8):
        s = str(i)
        test_x[size*i:size*(i+1)] = np.concatenate([np.load(os.path.join(used_directories[1], "test_" + atom_type + "_x_2A_" + s + ".npy")), 
                                                    np.load(os.path.join(used_directories[1], "test_" + atom_type + "_x_4A_" + s + ".npy")), 
                                                    np.load(os.path.join(used_directories[1], "test_" + atom_type + "_x_3A_" + s + ".npy")),
                                                    np.load(os.path.join(used_directories[1], "test_" + atom_type + "_x_5A_" + s + ".npy")),
                                                    np.load(os.path.join(used_directories[1], "test_" + atom_type + "_x_7A_" + s + ".npy"))], axis=-1)
    model = load_model(os.path.join(used_directories[2], model_name))
    pred = model.predict(test_x, batch_size=1)
    np.save(os.path.join(used_directories[3], "predicted_value_" + atom_type), pred)
    pred = np.mean(pred.reshape((8, -1)), axis=0)
    rms = np.sqrt(np.mean((pred*scale-test_y+mean) ** 2))
    return rms
    # 0.36-0.37 for H
    # 3.2-3.3 for C
    # 9.4-10.6 for N
    # 14.5-15.9 for O
