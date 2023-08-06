import os
import json
from tempfile import NamedTemporaryFile, TemporaryDirectory
from ucbshift.webapp_setup.download_models import download_models, get_models_folder

def test_no_config(monkeypatch):
	"""
	Tests get_models_folder() when no ucbshift_config.json file has been created
	Should run set_models_folder()
	"""
	#Monkeypatch provides the input for python builtin input function
	#This is used for set_models_folder()
	monkeypatch.setattr('builtins.input', lambda _: "")
	#Create tempdir
	tempdir = TemporaryDirectory()
	os.chdir(tempdir.name)

	#Returns path of the new folder
	models_folder_path = get_models_folder()
	config_created = 'ucbshift_config.json' in os.listdir(tempdir.name)
	folder_created = os.path.isdir(models_folder_path)
	assert (config_created and folder_created)

def test_download_no_config(monkeypatch):
	"""
	Tests download_models without a ucbshift_config.json file
	"""
	#Create tempdir
	monkeypatch.setattr('builtins.input', lambda _: "")
	tempdir = TemporaryDirectory()
	os.chdir(tempdir.name)

	download_models()
	#In tempdir, should have 'ucbshift_config.json', new folder '/models', 
	#and downloaded the 4 models in '/models'
	files = [f'{element}_model.h5' for element in ['hydrogen', 'carbon', 'nitrogen', 'oxygen']].sort()
	config_created = 'ucbshift_config.json' in os.listdir(tempdir.name)
	folder_created = os.path.isdir(os.path.join(tempdir.name, 'models'))
	#models_downloaded = (files == os.listdir(os.path.join(tempdir.name, 'models')))
	assert (config_created and folder_created and 
			(files == os.listdir(os.path.join(tempdir.name, 'models')).sort()))

def test_download_with_config():
	"""
	Tests download_models with existing ucbshift_config.json file but no folder
	"""
	#Create tempdir
	tempdir = TemporaryDirectory()
	os.chdir(tempdir.name)
	#Create ucbshift_config.json
	config = {'base': os.getcwd(), 'models': 'models'}
	with open('ucbshift_config.json', 'w') as f:
		json.dump(config, f)

	download_models()
	#In tempdir, should have 'ucbshift_config.json', new folder '/models', 
	#and downloaded the 4 models in '/models'
	files = [f'{element}_model.h5' for element in ['hydrogen', 'carbon', 'nitrogen', 'oxygen']].sort()
	config_created = 'ucbshift_config.json' in os.listdir(tempdir.name)
	folder_created = os.path.isdir(os.path.join(tempdir.name, 'models'))
	#models_downloaded = (files == os.listdir(os.path.join(tempdir.name, 'models')))
	assert (config_created and folder_created and 
			(files == os.listdir(os.path.join(tempdir.name, 'models')).sort()))

def test_download_existing_folder():
	"""
	Tests download_models with existing ucbshift_config.json file, partially populated folder
	"""
	#Create tempdir
	tempdir = TemporaryDirectory()
	os.chdir(tempdir.name)
	#Create ucbshift_config.json
	config = {'base': os.getcwd(), 'models': 'models'}
	with open('ucbshift_config.json', 'w') as f:
		json.dump(config, f)
	#Create folder, add a model file
	os.mkdir(os.path.join(config['base'], config['models']))
	with open('hydrogen_model.h5', 'w') as f:
		f.write('test')

	download_models()
	#In tempdir, should have 'ucbshift_config.json', new folder '/models', 
	#and downloaded the 4 models in '/models'
	files = [f'{element}_model.h5' for element in ['hydrogen', 'carbon', 'nitrogen', 'oxygen']].sort()
	config_created = 'ucbshift_config.json' in os.listdir(tempdir.name)
	folder_created = os.path.isdir(os.path.join(tempdir.name, 'models'))
	#models_downloaded = (files == os.listdir(os.path.join(tempdir.name, 'models')))
	assert (config_created and folder_created and 
			(files == os.listdir(os.path.join(tempdir.name, 'models')).sort()))