import sys
import os
import numpy as np

residue_types = {'ALA': 1, 'ARG': 2, 'ASP': 3, 'ASN': 4, 'CYS': 5, 'GLU': 6,
                 'GLY': 7, 'HIS': 8, 'ILE': 9, 'LEU': 10, 'MET': 11, 'LYS': 12,
                 'PHE': 13, 'PRO': 14, 'SEC': 15, 'SER': 16, 'THR': 17,
                 'TYR': 18, 'TRP': 19, 'VAL': 20, 'HOH': 21, 'OTHERS': 22}

atom_types = {'C': 1, 'N': 2, 'O': 3, 'S': 4, 'H': 5, 'Others': 6}


def get_internal_coords(data):

    pass


def find_distances(water_coor, atoms_coords):
    """
    find distances between one water and every other atoms
    ----------------------------------------------------------------------------
    water_coor: ndrray 1 x 3
    Chosen water's coordinate

    atom_coords: ndarray N x 3
    Array of protein atom coordinates

    ----------------------------------------------------------------------------
    Returns:
    dist: N x 1
    distances between given water and N prtein atoms
    """
    delta = water_coor - atoms_coords
    delta_sq = np.square(delta)
    dist = np.sqrt(np.sum(delta_sq, axis=1))

    return dist


def find_nth_closest_atoms(waters, atoms, n):
    """
    find n closest atoms near any water
    ----------------------------------------------------------------------------
    waters: ndrray N x 3
    Array of water coordinates

    atoms: ndarray N x 3
    Array of protein atom coordinates

    n: int
    Number of closest atoms
    ----------------------------------------------------------------------------
    Returns:
    nth_min_distances: N x 1
    nth minimum distances from N water molecules
    """
    water_coors = np.array([np.fromiter(water.values(), dtype=float)[0:3] for
                            water in waters])
    water_coors = water_coors.astype(float)
    atoms_coords = np.array([np.fromiter(atom.values(), dtype=float) for
                             atom in atoms])
    n_min_distances = []
    for water_coor in water_coors:
        dist = find_distances(water_coor, atoms_coords)
        sorted_dist = np.sort(dist)
        n_min_distances.append(sorted_dist[:n])

    return n_min_distances


def feature_encoder_atom(feature_number):
    """
    takes a number and outputs [cos(number), sin(number)]
    ----------------------------------------------------------------------------
    feature_number: int
    a number that represents atom_types
    ----------------------------------------------------------------------------
    Returns: ndarray
    An array of [cos(number), sin(number)]

    """
    return np.array([np.cos(feature_number), np.sin(feature_number)])


def feature_encoder_residue(feature_number):
    """
    takes a number and outputs [sin(number), cos(number)]
    ----------------------------------------------------------------------------
    feature_number: int
    a number that represents residue_types
    ----------------------------------------------------------------------------
    Returns: ndarray
    An array of [sin(number), cos(number)]

    """
    return np.array([np.sin(feature_number), np.cos(feature_number)])


def read_pdb(input_pdb):
    # read in the pdb file
    pdb_file = open(input_pdb)
    atom_info = [line for line in pdb_file.readlines()
                 if line.startswith('ATOM  ') or line.startswith('HETATM')]
    water_data = []
    protein_data = []
    for line in atom_info:
        one_data = np.array([])
        xyz = [float(x) for x in line[30:53].split()]
        # read in the atom name
        atom_type = str(line[76:78]).strip()
        res_type = str(line[17:20]).strip()
        try:
            atom_encode = feature_encoder_atom(atom_types[atom_type])
            residue_encode = feature_encoder_residue(residue_types[res_type])
        except KeyError:
            atom_types.setdefault(atom_type, 6)
            residue_types.setdefault(res_type, 22)
            atom_encode = feature_encoder_atom(atom_types[atom_type])
            residue_encode = feature_encoder_residue(residue_types[res_type])

        one_data = np.append(one_data, atom_encode)
        one_data = np.append(one_data, residue_encode)
        one_data = np.append(one_data, xyz)
        if res_type == 'HOH':
            water_data.append(one_data)
        else:
            protein_data.append(one_data)

    return np.array(water_data), np.array(protein_data)


if __name__ == '__main__':
    input_pdb = sys.argv[1]
    water_data, protein_data = read_pdb(input_pdb)

    pass
