#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 22:45:59 2021

@author: albertocabrera
"""

import numpy as np
import re

ANGSTROM_TO_BOHR = 1.8897259886
BOHR_TO_ANGSTROM = 1.0 / ANGSTROM_TO_BOHR 

ONE = 1.0

ATOMS = {'H': 1.0,
         'C': 6.0,
         'N': 7.0,
         'O': 8.0,
         'Fe': 26.0}
CHARGES = {value:key for key, value in ATOMS.items()}

XYZ_RE = re.compile('xyz')
KT_RE = re.compile('kt')
TIME_RE = re.compile('\d\d\:\d\d\:\d\d\.\d\d\d')
BLANK = '\n'

def xyz_to_np(file_xyz, conversor):
    
    print(' xyz_to_np(conversor= {})'.format(conversor))
    
    # Read all lines
    f = open(file_xyz, 'r')
    lines = f.readlines()
    f.close()
    
    # Initialize array
    n_atoms = int(lines[0])
    v_arr = np.zeros((n_atoms, 4))
    
    # Iterate and save all atoms as X Y Z CHARGE
    for i in range(n_atoms):
        
        # Skip first two lines
        elems = lines[i+2].split()
        
        # Define atom
        sym = elems[0]
        c = ATOMS[sym]
        x = float(elems[1]) * conversor
        y = float(elems[2]) * conversor
        z = float(elems[3]) * conversor
        v_arr[i, :] = np.array([x, y, z, c])
        
        print('[{:>10.5f}, {:>10.5f}, {:>10.5f}, {:.5f}],'.format(x, y, z, c))
        
    return v_arr

def np_to_gjf(file_xyz, v_arr, conversor):
    
    print(' np_to_gjf(conversor= {})'.format(conversor))
    
    # Rename files
    file_gjf = XYZ_RE.sub('gjf', file_xyz)
    file_chk = XYZ_RE.sub('chk', file_xyz)
    
    # Params
    keywords = '# hf/sto-3g \n'
    title = ' {} written with babel.py \n'.format(file_gjf)
    charge_and_multiplicity = '0 1 \n'
    
    # Write gjf file
    f = open(file_gjf, 'w')
    f.write('%chk={} \n'.format(file_chk))
    f.write(keywords)
    f.write(BLANK)
    f.write(title)
    f.write(BLANK)
    f.write(charge_and_multiplicity)
    for v in v_arr:
        x = v[0] * conversor
        y = v[1] * conversor
        z = v[2] * conversor
        c = v[3]
        symbol = CHARGES[c]
        f.write('{:<6} {:>10.6f} {:>10.6f} {:>10.6f} \n'.format(symbol, x, y, z))
    f.write(BLANK)
    f.close()
    
    print(' File {} written successfully.'.format(file_gjf))
    
def np_to_xyz(file_xyz, v_arr, conversor):
    
    print(' np_to_xyz(conversor= {})'.format(conversor))
    
    # Write gjf file
    f = open(file_xyz, 'w')
    f.write('{}\n'.format(v_arr.shape[0]))
    f.write('{} written with babel.py \n'.format(file_xyz))
    for v in v_arr:
        x = v[0] * conversor
        y = v[1] * conversor
        z = v[2] * conversor
        c = v[3]
        symbol = CHARGES[c]
        f.write('{:<6} {:>10.6f} {:>10.6f} {:>10.6f} \n'.format(symbol, x, y, z))
    f.write(BLANK)
    f.close()
    
    print(' File {} written successfully.'.format(file_xyz))
    
def np_to_kt(v_arr, conversor):
    
    print(' np_to_kt(conversor= {})'.format(conversor))
    
    for v in v_arr:
        
        x = v[0] * conversor
        y = v[1] * conversor
        z = v[2] * conversor
        c = v[3]
        
        new_line = ['{:9.5f}'.format(x), '{:9.5f}'.format(y), '{:9.5f}'.format(z), '{:9.5f}'.format(c)]
        print('doubleArrayOf({0}), '.format(', '.join(new_line)))
        
def kt_to_console(file_kt, starting, ending):
    
    print(' np_to_gjf(\n\tstarting= "{}"\n\tending= "{}"\n )'.format(starting, ending))
    
    # Read all lines
    f = open(file_kt, 'r')
    lines = f.readlines()
    f.close()
    
    # Read the file backwards until special label is found
    i = len(lines) - 1
    while i > 0 and starting not in lines[i]:
        i -= 1
        
    if i == 0:
        raise RuntimeError(' The file {} does not contain the phrase "{}"'.format(file_kt, starting))
    
    # Move one line forward
    i += 1
    
    # Move forward until the special label is found
    kount = 0
    while i < len(lines) and ending not in lines[i]:
        
        # The line is divided with ":"
        res = lines[i].split(': ')[-1]
        res = res.strip('\n')
        
        print(res)
        
        kount += 1
        i += 1
    
def main():
    
    file = 'Ethene.xyz'
    print(' Reading file {}'.format(file))
    
    v_arr = xyz_to_np(file, ANGSTROM_TO_BOHR)

if __name__ == '__main__':
    
    main()
    
    

