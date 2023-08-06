import requests 
import os
import json

def download_models():
	"""
	Downloads .h5 data from 3D-DenseNet-ChemShift repository to an input directory
	Inputs: None
	Returns: None
	"""
	install_folder = get_models_folder()
	#Make the directory if it does not exist
	if not os.path.isdir(install_folder):
		os.mkdir(install_folder)
	models = os.listdir(install_folder)
	for model in [f'{element}_model.h5' for element in ['hydrogen', 'carbon', 'nitrogen', 'oxygen']]:
		if model not in os.listdir(install_folder):
			github_url = "https://github.com/THGLab/3D-DenseNet-ChemShift/blob/master/trained_models/"
			raw = '?raw=true'

			url = github_url + model + raw
			r = requests.get(url)
			filename = os.path.join(install_folder, model)
			f = open(filename, 'wb')
			f.write(r.content)
			f.close()

def get_models_folder():
	"""
	Returns the folder for models from ucbshift_config.json
	Inputs: None
	Returns: folder, string of the folder name
	"""
	#Searches for ucbshift_config.json. If not found, run set_models_folder()
	files = os.listdir(os.getcwd())

	if 'ucbshift_config.json' not in files:
		set_models_folder()

	#Returns folder name
	with open('ucbshift_config.json', 'r') as f:
		config = json.load(f)
	return os.path.join(config['base'], config['models'])

def set_models_folder(): 
	"""
	Creates a folder for .h5 files to be stored in
	Saves the folder in ucbshift_config.json
	Inputs: None, but the built-in input() function is used within.
	Returns: None
	"""
	folder = input('Enter folder name for models to live in (entering nothing defaults to "models"): ')
	if folder == '':
		folder = 'models'
	install_folder = os.path.join(os.getcwd(), folder)

	#While: it exists and is not empty, ask for new input
	while (os.path.isdir(install_folder) and (len(os.listdir(install_folder)) != 0)):
		folder = input('This directory already exists and is populated. \n Please choose another folder name: ')
		install_folder = os.path.join(os.getcwd(), folder)
	
	#Make the directory if it does not exist
	if not os.path.isdir(install_folder):
		print(f'Creating new folder: {folder}')
		os.mkdir(install_folder)

	#Save path, folder name to ucbshift_config.json
	create_config(folder)

def create_config(folder):
	"""
	Write to ucbshift_config.json, with a default of clear for the data folder
	Input: folder, the models folder
	Returns: None

	"""
	config = {'base': os.getcwd(), 'models': folder, 'data_folder': 'clear'}
	with open('ucbshift_config.json', 'w') as f:
		json.dump(config, f)
		
if __name__ == "__main__":
	download_models()