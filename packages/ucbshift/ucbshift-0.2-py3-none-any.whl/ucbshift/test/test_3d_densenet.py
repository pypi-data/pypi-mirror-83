from ase.io import read
import keras
from keras.models import load_model
import numpy as np
import os
import shutil
from tempfile import NamedTemporaryFile, TemporaryDirectory
import pytest

#Imports of preprocessing functions
from ucbshift.display_utils.model_utils import convert_all_to_json, convert_json_to_numpy, data_augmentation, density_generation, predict
from ucbshift.webapp_setup.download_models import download_models
INPUT_DIRECTORY = "input_xyz"
SAVED_XYZ_DIRECTORY = "saved_xyz"
PRED_XYZ_DIRECTORY = "pred_xyz"
JSON_DIRECTORY = "json"
PREPROCESS_DIRECTORY = "preprocess"
DENSITYGEN_DIRECTORY = "density_gen"
PREDICTION_DIRECTORY = "prediction"
MODEL_DIRECTORY = "models"

"""
Helper Functions
"""
def create_xyz():
	atoms_1 = '3\n' + \
	'Lattice="1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 1.0" Properties=species:S:1:pos:R:3 pbc="F F F" \n' + \
	'C        0.00000000       0.00000000       0.00000000\n' + \
	'O        0.00000000       0.00000000       1.17865800\n' + \
	'O        0.00000000       0.00000000      -1.17865800\n'
	atoms_2 = '4\n' + \
	'Lattice="1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 1.0" Properties=species:S:1:pos:R:3 pbc="F F F" \n' + \
	'C        0.00000000       1.00000000       0.00000000\n' + \
	'H        0.00000000       0.00000000       1.17865800\n' + \
	'N        1.00000000       0.00000000       1.17865800\n' + \
	'O        0.00000000       0.00000000      -1.17865800\n'
	with open(os.path.join(SAVED_XYZ_DIRECTORY, 'atoms_1.xyz'), 'w') as f:
		print(atoms_1)
		f.write(atoms_1)
	with open(os.path.join(SAVED_XYZ_DIRECTORY, 'atoms_2.xyz'), 'w') as f:
		print(atoms_2)
		f.write(atoms_2)

def get_files(dir_):
	return [f for f in os.listdir(dir_) if os.path.isfile(os.path.join(dir_, f))]

def get_atoms(file):
	return read(os.path.join(SAVED_XYZ_DIRECTORY, file))

def get_elements():
    existing_elements = []

    for atom_type in ['H', 'C', 'N', 'O']:
        points = np.load(os.path.join(PREPROCESS_DIRECTORY, "test_" + atom_type + "_y.npy"))
        if points.size != 0:
            existing_elements.append(atom_type)

    return existing_elements

def setup_dir(dirs):
	for dir_ in dirs:
		os.mkdir(dir_)

"""
Test functions
"""
def test_to_json():
	"""
	Run xyz_to_json
	Check if the number of output folders is correct
	"""
	### Setup
	#Create temp dir and file dirs, create xyz files
	dirs = [SAVED_XYZ_DIRECTORY, JSON_DIRECTORY]

	tempdir = TemporaryDirectory()
	os.chdir(tempdir.name)
	setup_dir(dirs)
	create_xyz()

	### Tests 
	xyz_files = get_files(SAVED_XYZ_DIRECTORY)
	files = []
	for file in xyz_files:
		files.append(get_atoms(file))
	num_atoms = []
	for file in files:
		num_atoms.append(len(file.get_chemical_symbols()))

	#Run function
	convert_all_to_json(xyz_files, test=True)

	#Check that the number of files == number of atoms
	true_outputs = [len(xyz_files), num_atoms]
	test_outputs = [0, []]
	for root, dirs, files in os.walk(JSON_DIRECTORY):
		test_outputs[0] = test_outputs[0] + len(dirs)
		if len(files) > 0:
			test_outputs[1].append(len(files))
	true_outputs[1] = true_outputs[1].sort()
	test_outputs[1] = test_outputs[1].sort()
	assert true_outputs == test_outputs

def test_to_npy():
	"""
	Run json_to_numpy
	Check if 4 numpy files are created
	"""
	### Setup
	#Create temp dir and file dirs, create xyz files
	dirs = [SAVED_XYZ_DIRECTORY, JSON_DIRECTORY, PREPROCESS_DIRECTORY]

	tempdir = TemporaryDirectory()
	os.chdir(tempdir.name)
	setup_dir(dirs)
	create_xyz()
	
	### Tests 
	xyz_files = get_files(SAVED_XYZ_DIRECTORY)
	convert_all_to_json(xyz_files, test=True)

	#Run function
	convert_json_to_numpy(xyz_files, test=True)

	#Check for 4 output numpy files
	numpy_files = get_files(PREPROCESS_DIRECTORY)
	true_outputs = [12] + ['npy']*12
	test_outputs = [len(numpy_files)]
	for i in range(len(numpy_files)):
		__, ext = numpy_files[i].split('.')
		test_outputs.append(ext)
	assert true_outputs == test_outputs

def test_data_aug():
	"""
	Run data_augmentation
	Check if 8 * num_elements files are created
	"""
	### Setup
	#Create temp dir and file dirs, create xyz files
	dirs = [SAVED_XYZ_DIRECTORY, JSON_DIRECTORY, PREPROCESS_DIRECTORY]

	tempdir = TemporaryDirectory()
	os.chdir(tempdir.name)
	setup_dir(dirs)
	create_xyz()
	
	### Tests 
	xyz_files = get_files(SAVED_XYZ_DIRECTORY)
	convert_all_to_json(xyz_files, test=True)
	convert_json_to_numpy(xyz_files, test=True)
	elements = get_elements()
	num_elements = len(elements)

	#Run function
	for atom_type in elements: 
		data_augmentation(atom_type, test=True)

	#Check for 8 * num_elements new files
	numpy_files = get_files(PREPROCESS_DIRECTORY)
	true_output = 8 * num_elements
	test_output = len([f for f in numpy_files if 'aug' in f])
	assert true_output == test_output

@pytest.mark.timeout(60)
def test_density_gen():
	"""
	Run density_generation
	Check if 8 * 5 * num_elements files are created
	"""
	### Setup
	#Create temp dir and file dirs, create xyz files
	dirs = [SAVED_XYZ_DIRECTORY, JSON_DIRECTORY, PREPROCESS_DIRECTORY, DENSITYGEN_DIRECTORY]

	tempdir = TemporaryDirectory()
	os.chdir(tempdir.name)
	setup_dir(dirs)
	create_xyz()
	
	### Tests
	xyz_files = get_files(SAVED_XYZ_DIRECTORY)
	convert_all_to_json(xyz_files, test=True)
	convert_json_to_numpy(xyz_files, test=True)
	elements = get_elements()
	num_elements = len(elements)
	for atom_type in elements: 
		data_augmentation(atom_type, test=True)

	#Run function
	for atom_type in elements:
		density_generation(atom_type, test=True)

	#Check for 8 * 5 * num_elements new files
	density_files = get_files(DENSITYGEN_DIRECTORY)
	true_output = 8 * 5 * num_elements
	test_output = len(density_files)
	assert true_output == test_output

@pytest.mark.timeout(120)
def test_prediction_shape(monkeypatch):
	"""
	Run predict
	Check for: correct number of predicted atoms
	"""
	### Setup
	#Create temp dir and file dirs, create xyz files
	dirs = [SAVED_XYZ_DIRECTORY, JSON_DIRECTORY, PREPROCESS_DIRECTORY, DENSITYGEN_DIRECTORY, MODEL_DIRECTORY, PREDICTION_DIRECTORY]

	tempdir = TemporaryDirectory()
	os.chdir(tempdir.name)
	setup_dir(dirs)
	create_xyz()
	
	# Download models
	monkeypatch.setattr('builtins.input', lambda _: "")
	download_models()

	### Tests
	xyz_files = get_files(SAVED_XYZ_DIRECTORY)
	convert_all_to_json(xyz_files, test=True)
	convert_json_to_numpy(xyz_files, test=True)
	elements = get_elements()
	num_elements = len(elements)
	for atom_type in elements: 
		data_augmentation(atom_type, test=True)
	for atom_type in elements:
		density_generation(atom_type, test=True)

	#Run function
	given_models = {
		'H': 'hydrogen_model.h5',
		'C': 'carbon_model.h5',
		'N': 'nitrogen_model.h5',
		'O': 'oxygen_model.h5',
	}
	inputs = []
	for element in elements:
		inputs.append((given_models[element], element))
	for i in inputs:
		__ = predict(i[0], i[1], test=True)

	#Check assertions:
	#	get total number of each predicted atom_type (add up after reading from each molecule)
	#   compare 
	atom_counts = {
		'H': 0,
		'C': 0,
		'N': 0,
		'O': 0,
	}
	for file in xyz_files:
		molecule = get_atoms(file)
		for element in elements:
			num_target_atoms = len([a for a in molecule.get_chemical_symbols() if a == element])
			atom_counts[element] = atom_counts[element] + num_target_atoms

	true_outputs = [True] * num_elements
	test_outputs = []
	for element in elements:
		new_predicted = np.load(os.path.join(PREDICTION_DIRECTORY, "predicted_value_{}.npy".format(element)))
		shape = new_predicted.shape[0]//8
		test_outputs.append(shape == atom_counts[element])

	assert true_outputs == test_outputs