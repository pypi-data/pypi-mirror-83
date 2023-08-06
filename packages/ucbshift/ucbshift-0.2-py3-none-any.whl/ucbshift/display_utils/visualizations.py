import numpy as np
import os
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import scipy.stats as stats
import urllib.parse
import ase
from ase.io import read
from ase.geometry.analysis import Analysis
from ase import Atoms
from math import sqrt
from ucbshift.webapp_setup.manage_data_folders import get_path

INPUT_DIRECTORY = "input_xyz"
SAVED_XYZ_DIRECTORY = "saved_xyz"
PRED_XYZ_DIRECTORY = "pred_xyz"
JSON_DIRECTORY = "json"
PREPROCESS_DIRECTORY = "preprocess"
DENSITYGEN_DIRECTORY = "density_gen"
PREDICTION_DIRECTORY = "prediction"
MODEL_DIRECTORY = "models"

def get_predicted_atoms(xyz_file, target_atom, start_index):
    """
    Appends predicted values, saves it to an xyz, and returns a Pandas object and csv data

    """
    used_directories = list(map(get_path, [PREDICTION_DIRECTORY, SAVED_XYZ_DIRECTORY, PRED_XYZ_DIRECTORY]))

    predicted = np.load(os.path.join(used_directories[0],"predicted_value_{}.npy".format(target_atom)))
    reshaped = np.reshape(predicted, (predicted.size//8, 8), order='F')
    
    mean = np.mean(reshaped, axis=1)
    std = np.std(reshaped, axis=1)
    mean_std = pd.DataFrame(np.stack((mean, std), axis=1), columns=['Predicted Shift', 'std'])
    
    molecule = read(os.path.join(used_directories[1], xyz_file))
    num_target_atoms = len([a for a in molecule.get_chemical_symbols() if a == target_atom])
    num_total_atoms = len(molecule.get_chemical_symbols())
    
    full_np = np.column_stack((np.transpose(molecule.get_chemical_symbols()), molecule.get_positions(), np.transpose(molecule.get_masses())))
    full = pd.DataFrame(full_np, columns=['Element', 'x', 'y', 'z', 'Mass'])
    full['Mass'] = pd.to_numeric(full['Mass'])
    full['Predicted Shift'] = [None]*num_total_atoms
    full['std'] = [None]*num_total_atoms
    
    indices = full.loc[full['Element'] == target_atom].index
    for index in range(len(indices)):
        i = indices[index]
        full.at[i, 'Predicted Shift'] = mean_std.loc[start_index + index, 'Predicted Shift']
        full.at[i, 'std'] = mean_std.loc[start_index + index, 'std']

    #Save as .xyz for use in molecule3dviewer
    #The shift value will occupy the 'CS' variable for each atom
    molecule.set_array('CS', None)
    molecule.set_array('CS', full['Predicted Shift'].to_numpy())
    pred_file = os.path.join(used_directories[2], f'pred_{target_atom}_{xyz_file}')
    molecule.write(pred_file)

    #Save as csv
    filename, ext = xyz_file.split('.')
    csv_name = f'{target_atom}_{filename}_{ext}.csv'
    csv_string = full.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)

    return full, num_target_atoms, csv_name, csv_string

def dist(pos, a, b):
    """
    Returns Euclidean distance between points a and b with coordinates
    in the dict pos.
    """
    a = pos[a]
    b = pos[b]
    sqrs = []
    for i in range(len(a)):
        sqrs.append((a[i] - b[i]) ** 2)
    return sqrt(sum(sqrs))

def predicted_to_json(file):
    """
    Generates target JSON format for Molecule3dViewer component
    Input: file, name of the file


    """
    used_directories = list(map(get_path, [PRED_XYZ_DIRECTORY]))

    filepath = os.path.join(used_directories[0], f'pred_{file}')
    molecule = read(filepath)
    elem = molecule.get_chemical_symbols()
    positions = molecule.get_positions()
    mass = molecule.get_masses()
    #Get atoms, styles
    atoms = []
    styles={}
    labels = []
    Cs = molecule.get_array('CS')
    colors = {'H': '#aaaeb5', 'C': '#000000', 'N': '#0000FF', 'O': '#ff0000'}
    for i in range(len(elem)):
        ele = elem[i]
        pos = positions[i]
        atoms.append(
            {'elem': ele, 
             'positions': pos, 
             'mass': mass[i], 
             'serial': i, 
            }
        )
        styles[str(i)] = {
                'color': colors[ele],
                'visualization_type': 'sphere',
                }

        if Cs[i] != 'None':
            labels.append(
                {'backgroundColor': '0x000000',
                  'backgroundOpacity': 0.5,
                  'borderColor': 'black',
                  'fontColor': '0xffffff',
                  'fontSize': 14,
                  'position': 
                    {'x': pos[0],
                     'y': pos[1], 
                     'z': pos[2]
                    },
                  'text': Cs[i]}
            )
    #Get bonds
    ana = Analysis(molecule)
    unique_bonds = ana.unique_bonds[0]
    bonds = []
    for i in range(len(unique_bonds)):
        for atom2 in unique_bonds[i]:
            bonds.append({
                  "atom1_index": i,
                  "atom2_index": atom2,
              })

    # Validating the Bonds, since there seems to be an issue with it forming large bonds randomly
    # possibly to ensure that all atoms are bonded.
    true_bonds = []
    for i in range(len(bonds)):
        a, b = bonds[i]['atom1_index'], bonds[i]['atom2_index']
        length = (ana.get_bond_value(0, (a, b)))
        true_length = dist(positions, a, b)
        if abs(length-true_length) < .5:
            true_bonds.append(bonds[i])

    modelData = {'atoms': atoms, 'bonds': true_bonds}
    return modelData, labels, styles

def plot_shift_spectra(pandas_atoms):
    """
    Simulate a NMR Spectra graph using a kernel density estimator
    Input: pandas_atoms, a Pandas DataFrame of the target predicted atoms
    """
    shift = pandas_atoms['Predicted Shift'].to_numpy()
    fig = make_subplots(rows=1, cols=1,shared_xaxes=True, 
                        vertical_spacing=0.02,
                        row_heights=[1])
    fig.add_trace(go.Box(
        x=shift, 
        marker_symbol='line-ns-open', 
        marker_color='blue',
        #marker_size=10,
        boxpoints='all',
        jitter=0,
        fillcolor='rgba(255,255,255,0)',
        line_color='rgba(255,255,255,0)',
        hoveron='points',
        name='sample'
    ), row=1, col=1)
    
    fig.update_layout(showlegend=False, height=200)
    fig.update_xaxes(title_text="Chemical Shift (ppm)", autorange='reversed', row=1, col=1)
    fig.update_yaxes(showticklabels=False)
    return fig