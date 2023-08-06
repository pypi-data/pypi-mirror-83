#Imports
import base64
import os
import ase
from ase.io import read
import numpy as np
from ucbshift.webapp_setup.manage_data_folders import get_path

INPUT_DIRECTORY = "input_xyz"
SAVED_XYZ_DIRECTORY = "saved_xyz"
PRED_XYZ_DIRECTORY = "pred_xyz"
JSON_DIRECTORY = "json"
PREPROCESS_DIRECTORY = "preprocess"
DENSITYGEN_DIRECTORY = "density_gen"
PREDICTION_DIRECTORY = "prediction"
MODEL_DIRECTORY = "models"

def check_and_convert_xyz(filename):
    """
    This function:
        takes an input file from the inputted files, 
        extracts the ASE representation of the atoms,
        checks to make sure only H, C, N, and O are included,
        and if so, saves it as .xyz file in SAVED_XYZ_DIRECTORY.
    Inputs: filename, a string with the file's name
    """
    used_directories = list(map(get_path, [INPUT_DIRECTORY, SAVED_XYZ_DIRECTORY]))

    #Load ASE representation and check for HCNO
    atoms = get_atoms('input', filename)
    approved_atoms = [1, 6, 7, 8]
    only_HCNO = True
    for atomic_number in atoms.numbers:
        if atomic_number not in approved_atoms:
            only_HCNO = False
            break

    #Save to .xyz in SAVED_XYZ_DIRECTORY
    name, ext = filename.split('.')
    if only_HCNO:
        atoms.write(os.path.join(used_directories[1], name+'.xyz'), format = 'xyz')

def create_file(type, filename, file):
    """
    Returns nothing
    Creates a molecular file from file
    Inputs: filename, string of the file name
            file, b64 encoded file (from dash Upload module)
    """
    if type == 'molecule':
        used_directories = list(map(get_path, [INPUT_DIRECTORY]))
    elif type == 'model':
        used_directories = list(map(get_path, [MODEL_DIRECTORY]))

    content_type, content_string = file.split(',')

    with open(os.path.join(used_directories[0], filename), "wb") as fp:
       fp.write(base64.b64decode(content_string + "=="))

def get_atoms(folder, filename):
    """
    Returns an Atoms object (ASE)
    Inputs:  folder, string of the folder the file is stored in
            filename, a string of the filepath of the targeted molecular file
    """
    if folder == 'input':
        used_directories = list(map(get_path, [INPUT_DIRECTORY]))
    elif folder == 'loaded':
        used_directories = list(map(get_path, [SAVED_XYZ_DIRECTORY]))

    filepath = os.path.join(used_directories[0], filename)
    return read(filepath)

def get_elements():
    """
    Returns a list of the elements found during preprocessing
    """
    used_directories = list(map(get_path, [PREPROCESS_DIRECTORY]))

    existing_elements = []

    for atom_type in ['H', 'C', 'N', 'O']:
        points = np.load(os.path.join(used_directories[0], "test_" + atom_type + "_y.npy"))
        if points.size != 0:
            existing_elements.append(atom_type)

    return existing_elements

def get_files(folder):
    """
    Returns the list of files in the target folder, in a dict format
    Inputs: folder, the target folder
    """
    if folder == 'input':
        used_directories = list(map(get_path, [INPUT_DIRECTORY]))
    elif folder == 'loaded':
        used_directories = list(map(get_path, [SAVED_XYZ_DIRECTORY]))
    elif folder == 'models':
        used_directories = list(map(get_path, [MODEL_DIRECTORY]))


    f = []
    for root, dirs, files in os.walk(used_directories[0]):
        for file in files:
            if not (file.lower() == '.DS_store'.lower()):
                f.append(file)


    if len(f) == 0:
        return []
    if folder == 'input':
        return [{'label': filename, 'value': index} for index, filename in enumerate(f)]
    if folder == 'loaded':
        return [{'label': filename, 'value': filename} for index, filename in enumerate(f)]
    if folder == 'models':
        return [{'label': filename, 'value': filename, 'disabled': True} for index, filename in enumerate(f)]
