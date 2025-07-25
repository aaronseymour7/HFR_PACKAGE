
import os
import sys
import argparse
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import AllChem
from pulp import LpProblem, LpVariable, lpSum, LpMinimize, LpInteger, PULP_CBC_CMD, LpStatus
from rdkit.Chem import Descriptors, rdMolDescriptors
from itertools import combinations
from AaronTools.geometry import Geometry
from AaronTools.atoms import Atom
from AaronTools.theory import Theory, OptimizationJob, FrequencyJob
from AaronTools.fileIO import FileWriter
from hfrpkg.core import Isogyric, Isodesmic, Hypohomodesmotic, Homodesmotic


def isogyric_count(mol):
    atom_counts = {}
    if isinstance(mol, Chem.Atom):
        key = (mol.GetSymbol())
        atom_counts[key] = atom_counts.get(key, 0) + 1
        return atom_counts
    for atom in mol.GetAtoms():

        key = (atom.GetSymbol())
        atom_counts[key] = atom_counts.get(key, 0) + 1
    return atom_counts

def isodesmic_count(mol):
    bond_counts = {}
    for bond in mol.GetBonds():
        atom1 = bond.GetBeginAtom()
        atom2 = bond.GetEndAtom()

        atom_pair = tuple(sorted([atom1.GetSymbol(), atom2.GetSymbol()]))

        bond_type = (atom_pair, bond.GetBondType())
        bond_counts[bond_type] = bond_counts.get(bond_type, 0) + 1


    atom_counts = {}
    if isinstance(mol, Chem.Atom):
        key = (mol.GetSymbol())
        atom_counts[key] = atom_counts.get(key, 0) + 1
        return atom_counts
    for atom in mol.GetAtoms():
        if atom.GetSymbol() !='H':
            key = (atom.GetSymbol())
            atom_counts[key] = atom_counts.get(key, 0) + 1
    return bond_counts,atom_counts

def hypohomodesmotic_count(mol):
    mol = Chem.AddHs(mol)
    hydrogen_counts = {}
    mol = Chem.MolFromSmiles(Chem.MolToSmiles(mol))
    for atom in mol.GetAtoms():
        key = (atom.GetSymbol(), atom.GetNumExplicitHs())
        hydrogen_counts[key] = hydrogen_counts.get(key, 0) + 1
    mol = Chem.RemoveHs(mol)
    atom_counts = {}
    mol = Chem.MolFromSmiles(Chem.MolToSmiles(mol))
    for atom in mol.GetAtoms():
        key = (atom.GetSymbol(), atom.GetHybridization())
        atom_counts[key] = atom_counts.get(key, 0) + 1
    return hydrogen_counts, atom_counts

def homodesmotic_count(mol):
    bond_counts = {}
    for bond in mol.GetBonds():
        if bond.GetBeginAtom().GetSymbol()== 'H' or bond.GetEndAtom().GetSymbol()== 'H':
            continue 
        atom1 = bond.GetBeginAtom()
        atom2 = bond.GetEndAtom()

        atom_pair = tuple(sorted(
            [(atom1.GetSymbol(), atom1.GetHybridization()), 
             (atom2.GetSymbol(), atom2.GetHybridization())]
        ))

        bond_type = (atom_pair, bond.GetBondType())
        bond_counts[bond_type] = bond_counts.get(bond_type, 0) + 1


    hydrogen_counts = {}
    mol = Chem.MolFromSmiles(Chem.MolToSmiles(mol))
    for atom in mol.GetAtoms():
        key = (atom.GetSymbol(), atom.GetHybridization(), atom.GetNumExplicitHs())
        hydrogen_counts[key] = hydrogen_counts.get(key, 0) + 1
    return bond_counts, hydrogen_counts

def display_reaction_counts(input_mol, reaction_fn):
    def format_key(k):
        if isinstance(k, tuple):
            return "(" + ", ".join(format_key(i) for i in k) + ")"
        if hasattr(k, 'name'):  # for RDKit enums like HybridizationType
            return k.name
        return str(k)

    def print_dict(title, d):
        if not d:
            return
        print(f"\n{title}:")
        print("-" * len(title))
        for key, val in sorted(d.items()):
            print(f"{format_key(key):<60} : {val}")    

    if reaction_fn is Isogyric:
        atom_counts = isogyric_count(input_mol)
        print_dict("Isogyric Atom Counts", atom_counts)

    elif reaction_fn is Isodesmic:
        bond_counts, atom_counts = isodesmic_count(input_mol)
        print_dict("Isodesmic Bond Counts", bond_counts)
        print_dict("Isodesmic Atom Counts", atom_counts)

    elif reaction_fn is Hypohomodesmotic:
        hydrogen_counts, atom_counts = hypohomodesmotic_count(input_mol)
        print_dict("Hypohomodesmotic Hydrogen Counts", hydrogen_counts)
        print_dict("Hypohomodesmotic Atom Counts", atom_counts)

    elif reaction_fn is Homodesmotic:
        bond_counts, hydrogen_counts = homodesmotic_count(input_mol)
        print_dict("Homodesmotic Bond Counts", bond_counts)
        print_dict("Homodesmotic Hydrogen Counts", hydrogen_counts)


def geom_from_rdkit(rdkitmol):
    """
    Takes an RDKit molecule (already embedded) and returns an AaronTools Geometry along with
    the weighted adjacency matrix
    """
    result = AllChem.EmbedMolecule(rdkitmol)
    if result != 0:
        raise ValueError("Embedding failed")

    atom_list = []
    for i, atom in enumerate(rdkitmol.GetAtoms()):
        positions = rdkitmol.GetConformer().GetAtomPosition(i)
        atom_list.append(Atom(element=atom.GetSymbol(), coords=positions))
    return Geometry(atom_list)
