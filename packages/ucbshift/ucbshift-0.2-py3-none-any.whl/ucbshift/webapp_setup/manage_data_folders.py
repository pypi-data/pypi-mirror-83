import json
import os
import shutil
import atexit
from ucbshift.webapp_setup.download_models import get_models_folder

INPUT_DIRECTORY = "input_xyz"
SAVED_XYZ_DIRECTORY = "saved_xyz"
PRED_XYZ_DIRECTORY = "pred_xyz"
JSON_DIRECTORY = "json"
PREPROCESS_DIRECTORY = "preprocess"
DENSITYGEN_DIRECTORY = "density_gen"
PREDICTION_DIRECTORY = "prediction"
MODEL_DIRECTORY = "models"

#All folders except saved_xyz and model
temp_dirs = [INPUT_DIRECTORY, PRED_XYZ_DIRECTORY, JSON_DIRECTORY, PREPROCESS_DIRECTORY, DENSITYGEN_DIRECTORY, PREDICTION_DIRECTORY]

def make_data_folders():
	"""
	Creates all temporary folders
	Input: None
	Returns: None
	"""
	#Might create different specifications for this data_folder instead of all using the same name
	folder = 'ucbshift_data_folder'
	
	with open('ucbshift_config.json', 'r') as f:
		config = json.load(f)
		#print(f"Config cwd: {config['base']}")
	#print(f"process cwd: {os.getcwd()}")

	if os.path.isdir(folder):
		clear_data_folders()

	os.mkdir(folder)
	if not os.path.isdir(os.path.join(os.getcwd(), SAVED_XYZ_DIRECTORY)):
		os.mkdir(os.path.join(os.getcwd(), SAVED_XYZ_DIRECTORY))
	for temp_dir in temp_dirs:
		os.mkdir(os.path.join(os.getcwd(), folder, temp_dir))
	
	rewrite_config_folder(folder)

def get_path(folder):
	"""
	Returns filepaths of the requested folder
	Input: folder, the folder name string
	Returns: path of the folder
	"""
	with open('ucbshift_config.json', 'r') as f:
		config = json.load(f)

	if (folder == MODEL_DIRECTORY):
		return get_models_folder()
	elif (folder == SAVED_XYZ_DIRECTORY):
		return os.path.join(config['base'], SAVED_XYZ_DIRECTORY)
	else:
		return (os.path.join(config['base'], 
							  config['data_folder'],
							  folder))
@atexit.register
def clear_data_folders():
    """
	Checks if ucbshift_config.json indicates that there is temporary data in data_folder.
	If there is, it removes the folders and resets the ucbshift_config.json

	This is run when the program is terminated with Ctrl+C. 
	Input: None
	Returns: None
    """
    #check if ucbshift_config.json has data_folder, clear if it does and then clear the folders
    if os.path.isfile('ucbshift_config.json'):
	    with open('ucbshift_config.json', 'r') as f:
	    	config = json.load(f)

	    if (config['data_folder'] != 'clear'):
	    	shutil.rmtree(os.path.join(config['base'], config['data_folder']))
	    	rewrite_config_folder('clear')

def clear_saved():
	"""
	Clears the saved .xyz files folder
	Input: None
	Returns: None
	"""
	#If saved folder doesn't exist, make one.
	with open('ucbshift_config.json', 'r') as f:
		config = json.load(f)
	path = os.path.join(config['base'], SAVED_XYZ_DIRECTORY)
	if not os.path.isdir(path):
		os.mkdir(path)
	else:
		for root, dirs, files in os.walk(path):
			for f in files:
				os.unlink(os.path.join(root, f))
			for d in dirs:
				shutil.rmtree(os.path.join(root, d))


def rewrite_config_folder(name):
	with open('ucbshift_config.json', 'r+') as f:
		config = json.load(f)
		config['data_folder'] = name
		f.seek(0)
		json.dump(config, f)
		f.truncate()