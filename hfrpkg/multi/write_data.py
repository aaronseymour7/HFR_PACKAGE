import os
import glob
import re
from hfrpkg.multi.compute_folder import compute_folder


def write_single_reaction(reaction_data, folder_path):
    output_path = os.path.join(folder_path, "reaction_summary.txt")
    with open(output_path, "w", encoding="utf-8") as fout:
        fout.write(f"{reaction_data['input_smiles']}\t{reaction_data['input_inchi']}\t{reaction_data['dft_hf']}\n")
        
        fout.write("REACTANTS\n")
        for coeff, smiles, inchi, atct in reaction_data['reactants']:
            fout.write(f"{coeff} {smiles}\t{inchi}\t{atct}\n")
        
        fout.write("PRODUCTS\n")
        for coeff, smiles, inchi, atct in reaction_data['products']:
            fout.write(f"{coeff} {smiles}\t{inchi}\t{atct}\n")
        
        fout.write("\n")
    return reaction_data['input_smiles'],reaction_data['level'],reaction_data['input_inchi'],reaction_data['dft_hf'],reaction_data['input_atct']
