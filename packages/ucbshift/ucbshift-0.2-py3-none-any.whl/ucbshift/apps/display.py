import dash_daq as daq
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bio as dashbio
from dash.dependencies import Input, Output, State

from ucbshift.app import app
from ucbshift.display_utils.display_utils import * 
from ucbshift.display_utils.model_utils import *
from ucbshift.display_utils.visualizations import *
from ucbshift.webapp_setup.manage_data_folders import make_data_folders, clear_data_folders, clear_saved

layout = html.Div([
	html.Meta(charSet = 'utf-8'),
	html.H4(
		'UCBShift',
		style = dict(
			textAlign = 'center',
		),
		),
	html.Div([
		html.Div([
			dcc.Markdown(
				children="""
				This web application serves as an interface to interact with the following machine learning model from the [Head-Gordon Lab](https://thglab.berkeley.edu/home/).
				
				Read the paper [here](https://pubs.acs.org/doi/abs/10.1021/acs.jpclett.9b01570). &nbsp; &nbsp; &nbsp; See the code [here](https://github.com/THGLab/3D-DenseNet-ChemShift).
				""",
				className='maintext',
				),
				],
			className='bordered flex-container',
			style={
				'borderStyle': 'dashed',
				'borderColor': 'grey',
				'margin': '20px',
				}
			),
		html.Div([
			html.Div([
				html.Div([
					html.P('0', className='label'),
					dcc.Markdown(
						children="""
						### Guide
						
						Get started below by uploading your xyz files.

						The recommended order of steps is numbered.

						""",
						className='maintext',
						),
						],
					className='bordered flex-container',
					style={
						'boxSizing': 'border-box',
						'padding': '0px',
						'paddingRight': '10px',
						'marginBottom': '5px',
						'width': '100%',
						'height': '50%',
					}
					),
				html.Div(
					children=[
						html.P('1', className='label'),
						dcc.Markdown(
							children="""

							#### File Input

							Use the button below to upload your molecular files.
							""",
							className = 'maintext',
							),
						dcc.Upload(
							id='upload-xyz-button',
							children='Upload XYZ',
							multiple=True,
							accept='.xyz, .extxyz',
							className='button next',
							),
						],
					className='bordered flex-container',
					style={
						'boxSizing': 'border-box',
						'padding': '0px',
						'paddingRight': '10px',
						'marginTop': '5px',
						'width': '100%',
						'height': '50%',
					}
					),
					],
				className='bordered flex-container two-col',
				style={
					'border': 'none',
					'padding': '0px',
					'marginRight': '20px',
				},
				),		
			html.Div(
				id='uploading-files',
				children=[
					html.P('2', className='label'),
					dcc.Markdown(
						"""
						#### Input Choice

						Select which files you would like to predict from.
						
						These files will be screened to ensure they only contain H, C, N, and O.

						""",
						className = 'maintext',
						),
					html.Div([
						html.Div(
							id='input-changed', 
							children=0,
							style={'display':'none'}
							),
						dcc.Checklist(
							id="uploaded-files",
							options=[],
							value=[],
							className='filelist'
							),
							],
						className='overflow-box'
						),
					html.Div([
						html.Button(
							id='select-all-inputs-button-1',
							children='Select All',
							n_clicks=0,
							className='button',
							),
						html.Button(
							id='select-files-button',
							children='Load',
							n_clicks=0,
							className='button next',
							),
							],
						className='flex-row'
						),
					],
				className='bordered flex-container two-col',
				),
			
				],
			className='flex-row'
			),
		html.Div([html.Div(
				id='loading-files',
				children=[
					html.Div('3', className='label'),
					dcc.Markdown(
						"""
						#### Files Saved For Use

						These are the verified .xyz files with only H, C, N, and O.
						Click Prepare Data to begin preprocessing.

						"""
						),

					html.Div([
						html.Div(
							id='loaded-changed', 
							children=0,
							style={'display':'none'}
							),
						dcc.Checklist(
							id="loaded-files",
							options=[],
							value=[],
							className='filelist'
							),
							],
						className='overflow-box'
						),

					html.Div([
						html.Div(
							id='cleared', 
							children=0,
							style={'display':'none'}
							),
						html.Button(
							id='clear-data-button',
							children='Clear saved',
							n_clicks=0,
							className='button',
							),
						html.Button(
							id='select-all-inputs-button-2',
							children='Select All',
							n_clicks=0,
							className='button',
							),
							],
						className='flex-row'
						),
					html.Div([
						html.Button(
							id='preprocessing-button',
							children='Prepare Data',
							n_clicks=0,
							className='button next',
							),
							],
						className='flex-row'
						),
					],
				className='bordered flex-container two-col',
				),
			
			html.Div(
				id='choose-model',
				children=[
					html.P('4', className='label'),
					daq.Indicator(
						id='indicator',
						color='red', 
						className='indicator'
						),
					dcc.Markdown(
						"""
						#### Choose a model

						Currently accepting .h5 files format(s).
						If adding a new model, make sure the name 
						of the file fully includes one of hydrogen,
						carbon, nitrogen, or oxygen.

						The checkboxes below indicate whether or not
						the element was found in the preprocessed data.
						""",
						className = 'maintext',
						),

					dcc.Checklist(
						id='detected-elements',
						options=[
							{'label': 'H  ', 'value': 'H', 'disabled': True},
							{'label': 'C  ', 'value': 'C', 'disabled': True},
							{'label': 'N  ', 'value': 'N', 'disabled': True},
							{'label': 'O  ', 'value': 'O', 'disabled': True},
							],
						value=[],
						labelStyle={'display': 'inline-block'},
						),
					# Single Select Dropdown of models
					html.Div([
						html.Div(
							id='model-changed', 
							children=0,
							style={'display':'none'}
							),
						dcc.RadioItems(
							id="models",
							options=[],
							value='',
							className='filelist'
							),
							],
						className='overflow-box'
						),

					html.Div([
						dcc.Upload(
							id='upload-model-button',
							children='Upload Model',
							multiple=True,
							accept='.h5',
							className='button',
							),
						dcc.Loading(
							id='loading-preprocessing',
							children=[
								html.Button(
									id='prediction-button',
									children='Generate Predictions',
									n_clicks=0,
									disabled=True,
									title='Preprocessed Data Missing',
									className='button next',
									),
								],
							type='circle',
							),
							],
						className='flex-row'
						),
					html.Div(
						id='prepared-files',
						children='',
						style={'display': 'none'}
						),
					],
				className='bordered flex-container two-col'
				),	
				],
			className='flex-row'
			),
		html.Div(
			id='display-results',
			children=[
				html.P('5', className='label'),
				dcc.Markdown(
					"""
					#### Results
					""",
					className='maintext',
					),
				html.Div(
					children=[
						dcc.Loading(
							id='visualizations',
							children=[
								dcc.Tabs(
									id='tabs',
									children=[],
									value='',
									), 
								html.Div(
									children=[
										dcc.Markdown(
											'''
											Visualization Style
											\t Note: atoms that are not predicted to have covalent bonds
											by the program will not be rendered in stick mode. \n
											\t Note: If nothing appears below, enable hardware acceleration and refresh.
											'''
											),
										dcc.Tabs(
											id='visualization_type',
											value='sphere',
											children=[
												dcc.Tab(label= 'sphere', value='sphere', className='tab', selected_className='selected-tab'),
												dcc.Tab(label= 'stick', value='stick', className='tab', selected_className='selected-tab'),
											],
											),

									],
									style={
										'width': '50%',
										'margin': 'auto'
									}
									),
								dashbio.Molecule3dViewer(
									id='3d',
									modelData={'atoms': [{'chain': 'A',
														   'element': 'N',
														   'name': 'N',
														   'positions': [15.407, -8.432, 6.573],
														   'residue_index': 1,
														   'residue_name': 'GLY1',
														   'serial': 0}],
											 'bonds': []},
									atomLabelsShown=True,
									selectionType='atom',
									backgroundColor='#0032FF',
    								backgroundOpacity=0.5,
									),
								dcc.Store(
									id='3d-cache', 
									storage_type='session'
									),
								],
							type='circle'
							),
						],
					className='tabs',
					),

			],
			className='bordered flex-container',
			style={'margin': '20px'}
		), 

	],
	className='columns'
	),
]
)

###################################
#########    CALLBACKS    #########
###################################

#Clear Old Data
#--------------------------------#
#Clear on startup and button press
@app.callback(Output('cleared', 'children'),
			 [Input('clear-data-button', 'n_clicks')],
			 [State('cleared', 'children')])
def clear(clicks, cleared):
	if clicks == 0:
		#This occurs every start up
		print('++++++++++++++++++++++++++++++++++++')
		make_data_folders()
	if clicks > 0:
		clear_saved()
	return cleared + 1

#Get Input Files
#--------------------------------#
@app.callback(Output('input-changed', 'children'),
			 [Input('upload-xyz-button', 'filename')],
			 [State('upload-xyz-button', 'contents'),
			  State('input-changed', 'children')])
def upload_files(filenames, contents, changed):
	#Save from upload component to actual files in input_files
	if filenames is None or contents is None:
		return changed + 1
	else:
		for index, filename in enumerate(filenames):
			create_file('molecule', filenames[index-1], contents[index-1])

		return changed + 1

#Select Input Files to Infer
#--------------------------------#
@app.callback(Output('uploaded-files', 'value'),
			  [Input('select-all-inputs-button-1', 'n_clicks')],
			  [State('uploaded-files', 'options')])
def select_all_first(clicks, options):
	if clicks > 0:
		return [n for n in range(len(options))]
	else:
		return []

@app.callback(Output('loaded-files', 'value'),
			  [Input('select-all-inputs-button-2', 'n_clicks')],
			  [State('loaded-files', 'options')])
def select_all_second(clicks, options):
	if clicks > 0:
		return [option['value'] for option in options]
	else:
		return []


@app.callback(Output('loaded-changed', 'children'),
			 [Input('select-files-button', 'n_clicks'),],
			 [State('uploaded-files', 'value'),
			  State('uploaded-files', 'options'),
			  State('loaded-files', 'options'),
			  State('loaded-changed', 'children')])
def load_files(select_clicks, values, options, loaded_files, changed):
	if select_clicks > 0:
		for val in values:
			#Get name of the file
			filename = options[val]['label']
			#Check if file is already loaded
			is_loaded = False
			if len(loaded_files) > 0:
				for file in loaded_files:
					if filename in file.values():
						is_loaded = True
						break

			#Check for H,C,N,O and convert to xyz
			if not is_loaded:
				check_and_convert_xyz(filename)

	return changed + 1

#Upload model
#--------------------------------#
@app.callback(Output('model-changed', 'children'),
			 [Input('upload-model-button', 'filename')],
			 [State('upload-model-button', 'contents'),
			  State('model-changed', 'children')])
def upload_models(filenames, contents, changed):
	if filenames is None or contents is None:
		return changed + 1
	else:
		for index, filename in enumerate(filenames):
			create_file('model', filenames[index-1], contents[index-1])
		return changed + 1

#Reload file lists
#--------------------------------#
@app.callback([Output('uploaded-files', 'options'),
			   Output('loaded-files', 'options'),
			   Output('models', 'options')],
			  [Input('input-changed', 'children'),
			   Input('loaded-changed', 'children'),
			   Input('model-changed', 'children'),
			   Input('cleared', 'children'),
			   Input('detected-elements', 'value')]) 
			  #[State('detected-elements', 'value')])
def reload_lists(input, loaded, model, cleared, det_elem):

	elements = {'H': 'hydrogen', 'C': 'carbon', 'N': 'nitrogen', 'O': 'oxygen'}
	new_models = get_files('models')
	for i in range(len(new_models)):
		for atom_type in det_elem:
			if elements[atom_type] in new_models[i]['label'].lower():
				new_models[i]['disabled'] = False


	return [get_files('input'), get_files('loaded'), new_models]

#Run Model
#--------------------------------#
@app.callback([Output('prediction-button', 'disabled'),
			   Output('prediction-button', 'title'),
			   Output('prediction-button', 'style'),
			   Output('prepared-files', 'children'),
			   Output('detected-elements', 'value')],
			  [Input('preprocessing-button', 'n_clicks')],
			  [State('loaded-files', 'value')])
def preprocessing(clicks, files):
	style={
			'opacity': '.6',
			'cursor': 'not-allowed',
		}

	if clicks == 0 or files == []:
		return [True, 'Preprocessed Data Missing', style, files, []]

	else:
		#xyz_to_json, json_to_numpy, and data_augmentation use temporary directories
		#xyz_to_json, json_to_numpy
		first_functions = [convert_all_to_json, convert_json_to_numpy]
		dummy_functions = [print]

		for func in first_functions:
			func(files)
		elements = get_elements()

		if elements == []:
			return [True, 'Preprocessed Data Missing', style, files, elements]

		#data_augmentation, density_generation
		last_functions = [data_augmentation, density_generation]


		for atom_type in elements:
			#for func in last_functions:
			for func in dummy_functions:
				func(atom_type)
		style={
			'opacity': '1',
			'cursor': 'default',
		}

		return [False, 'Generate Prediction', style, files, elements]

@app.callback(Output('indicator', 'color'),
			 [Input('loaded-files', 'value'),
			  Input('prepared-files', 'children')])
def light_indicator(loaded_files, prepared_files):
	if loaded_files != prepared_files or loaded_files == []:
		return 'red'
	else: 
		return 'springgreen'

@app.callback(
			 [Output('tabs', 'children'),
			  Output('tabs', 'value')],
			 [Input('prediction-button', 'n_clicks')],
			 [State('models', 'value'),
			  State('detected-elements', 'value'), 
			  State('prepared-files', 'children'),
			  State('tabs', 'children')])
def prediction(clicks, model, elements, prepared_files, existing_tabs):
	if clicks == 0:
		return [[], '']
	else:
		#Get atom_type of model
		atom_type = ''
		for element, symbol in [('hydrogen', 'H'), ('carbon', 'C'), ('nitrogen', 'N'), ('oxygen', 'O')]:
			if element in model.lower():
				atom_type = symbol


		# *** RUN PREDICTION *** #
		#RMS = predict(model_name, atom_type)
		RMS = 1
		tabs = existing_tabs
		last_file = ''

		start_index = 0
		for file in prepared_files:
			#Add predictions to xyz data, output in pandas DataFrame
			new_pd, atoms_used, csv_name, csv_string = get_predicted_atoms(file, atom_type, start_index)

			#Get a copy with just the target atom_type
			target_pd = new_pd.loc[new_pd['Element'] == atom_type]
			start_index += atoms_used

			#Get spectra, DataTable
			fig = plot_shift_spectra(target_pd)
			graph = dcc.Graph(figure=fig, style={'width': '100%'})
			shifts = html.Div(children=[graph], className='flex-row')
			table = dash_table.DataTable(
							columns=[{"name": i, "id": i} for i in new_pd.columns],
							data = new_pd.to_dict('records'),
							filter_action='native',
							fixed_columns={'headers': True, 'data': 1},
							style_cell={
								'textOverflow': 'ellipsis',
							},
							style_cell_conditional = [
								{'if': {'column_id': 'Element'},
        						 'width': '20%'},
        						{'if': {'column_id': 'x'},
        						 'width': '10%'},
        						{'if': {'column_id': 'y'},
        						 'width': '10%'},
        						{'if': {'column_id': 'z'},
        						 'width': '10%'},
        						{'if': {'column_id': 'Mass'},
        						 'width': '10%'},
        						{'if': {'column_id': 'Predicted Shift'},
        						 'width': '20%'},
        						{'if': {'column_id': 'std'},
        						 'width': '20%'},
							],
							style_table={
								'height': '250px',
								'minWidth': '100%',
								'overflowY': 'auto'
							},
							virtualization=True,
						)

			#Download Link
			button = html.Button(
						children='Download CSV',
						n_clicks=0,
						className='button next',
				 		),
			download_link = html.A(
						        button,
						        download=csv_name,
						        href=csv_string,
						        target="_blank"
						    )
			RMS_text = html.P(children=f'RMS of shifts: {RMS}')
			#Create a tab for the molecule
			tab_name = f'{atom_type}_{file}'
			last_file = tab_name
			tab = dcc.Tab(label=tab_name, value=tab_name, children=[download_link, table, RMS_text, shifts])
			tabs.append(tab)
		#Generate visualizations for each predicted file
		return [tabs, last_file]

@app.callback([Output('3d', 'modelData'),
			   Output('3d', 'labels'),
			   Output('3d', 'styles'),
			   Output('3d-cache', 'data')], 
			  [Input('tabs', 'value'),
			   Input('visualization_type', 'value')],
			  [State('3d-cache', 'data')],
			  prevent_initial_call=True)
def retrieve_mol3d(file, visualization_type, cache):
	if file == '':
		return {'atoms': [],'bonds': []}, [], [], cache 

	if cache == None:
		cache = {}
	if file not in cache.keys():
		modelData, labels, styles = predicted_to_json(file)
		data = (modelData, labels, styles)
		cache[file] = data
	else:
		data = cache[file]
	# Update visualization type based on tab input
	for k in data[2].keys():
		data[2][k]['visualization_type'] = visualization_type
	return data[0], data[1], data[2], cache