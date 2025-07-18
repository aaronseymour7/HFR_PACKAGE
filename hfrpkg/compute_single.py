#!/usr/bin/env python3

import glob
import re
import sys
from AaronTools.fileIO import FileReader
def get_B(filename):

    base = filename.replace(".log", "")  

    part1 = base.split("_")[0]  

    B_str = part1[1:]  

    return int(B_str)

def get_final_R_coefficient():
    pattern = re.compile(r"^R(\d+)_(\d+)\.log$")
    max_B = -1
    coeff_C = None
    log_files = glob.glob("*.log")

    for filename in log_files:
        match = pattern.match(filename)
        if match:
            B = int(match.group(1))
            C = int(match.group(2))
            if B > max_B:
                max_B = B
                coeff_C = C

    if coeff_C is not None:
        return coeff_C
    else:
        print("No error reading coefficients.")
        return None


def extract_coeff_and_type(filename):
    pattern = re.compile(r"^([PR])\d+_(\d+)\.log$")
    m = pattern.match(filename)
    if not m:
        print(f"Warning: filename {filename} does not match expected pattern.")
        return None, None
    mol_type = filename.replace(".log", "")  # actual filename base 
    coeff = int(m.group(2))
    return mol_type, coeff

def get_enthalpy(logfile):
    try:
        reader = FileReader(logfile, just_geom=False)
        enthalpy = None
        if 'enthalpy' in reader.keys():
            enthalpy = reader['enthalpy']
        else:
            print(f"Warning: No enthalpy found in {logfile}.")
            return None
        return enthalpy
    except Exception as e:
        print(f"Error reading {logfile}: {e}")
        return None


def get_inchi(log_filename, index_path="index.txt"):
    name = log_filename
    try:
        with open(index_path, "r") as f:
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) < 3:
                    continue  
                index_name = parts[0]
                inchi = parts[1]
                if index_name == name:
                    return inchi
        print(f"InChI not found for {name} in {index_path}")
        return None
    except FileNotFoundError:
        print(f"Index file '{index_path}' not found.")
        return None


def get_Hf(inchi):
    #atct_path="/home/ads09449/bin/ATcT_lib.txt"
    try:
        with importlib.resources.open_text("hfrpkg.data", "ATcT_lib.txt", encoding="utf-8") as f:
        #with open(atct_path, encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) >= 6 and parts[3] == inchi:
                    return float(parts[5])
    except Exception:
        pass
    return None

def main():
    log_files = glob.glob("*.log")
    log_files.sort(key=get_B)
    if not log_files:
        print("No .log files found in current directory.")
        sys.exit(1)
    products = []
    reactants = []

    for f in log_files:
        if f.startswith("P"):
            products.append(f)
        elif f.startswith("R"):
            reactants.append(f)

    reactants.sort()
    reactants_to_use = reactants[:-1]
    total_products = 0.0
    total_reactants = 0.0
    Hf_products = 0.0
    Hf_reactants = 0.0
    for f in products:
        mol_type, coeff = extract_coeff_and_type(f)
        if mol_type is None or coeff is None:
            continue

        enthalpy = get_enthalpy(f)
        if enthalpy is None:
            continue
        enthalpy_scaled = enthalpy * coeff
        total_products += enthalpy_scaled
        
    for f in reactants:
        mol_type, coeff = extract_coeff_and_type(f)
        if mol_type is None or coeff is None:
            continue


        enthalpy = get_enthalpy(f)
        if enthalpy is None:
            continue
        enthalpy_scaled = enthalpy * coeff
        total_reactants += enthalpy_scaled
    
    
    
    reaction = 2625.5*(total_products - total_reactants)
    
    
    
    final_coeff = get_final_R_coefficient()
    usable_reactants = reactants[:-1]
    for f in usable_reactants:
        mol_type, coeff = extract_coeff_and_type(f)
        if mol_type is None or coeff is None:
            continue
        inchi = get_inchi(mol_type)
        Hf = get_Hf(inchi)
        if Hf is None:
            print(f"No ATcT value for {mol_type}")
        else:
            Hf_reactants += Hf * coeff
            print(f"{f}: coeff={coeff}, Hf={Hf}")
    for f in products:
        mol_type, coeff = extract_coeff_and_type(f)
        if mol_type is None or coeff is None:
            continue
        inchi = get_inchi(mol_type)
        Hf = get_Hf(inchi)
        if Hf is None:
            print(f"No ATcT value for {mol_type}")
        else:
            Hf_products += Hf * coeff
            print(f"{f}: coeff={coeff}, Hf={Hf}")

    input_hf = (Hf_products-Hf_reactants-reaction)/final_coeff
    
    
    
    
    
    print(f"REACTION ENTHALPY (kJ/mol): {reaction:.6f}")
    print(f"ENTHALPY OF FORMATION (kJ/mol): {input_hf:.6f}")
    inmol = reactants[-1]
    a,b = extract_coeff_and_type(inmol)
    i = get_inchi(a)
    if get_Hf(i):
        atct = get_Hf(i)
        print(f"ATcT Hf (kJ/mol): {atct}")
def main_cli():
    main()

if __name__ == "__main__":
    main_cli()

