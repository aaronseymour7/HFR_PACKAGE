#!/usr/bin/env python3

import glob
import os
import csv
from hfrpkg.multi.compute_folder import run_folder
def main():
    results = []
    cwd = os.getcwd()

    for mhfr_file in sorted(glob.glob("*.mhfr"), key=lambda x: int(x.split(".")[0])):
        folder = mhfr_file
        if os.path.isdir(folder):
            try:
                result = run_folder(folder)
                if result is not None:
                    results.append(result)
            except Exception as e:
                print(f"Error processing {folder}: {e}")

    with open("enthalpies_summary.csv", "w", newline="") as fout:
        writer = csv.writer(fout)
        writer.writerow(["SMILES","LEVEL","InChI", "ΔHf DFT (kcal/mol)", "ΔHf ATcT (kcal/mol")
        writer.writerows(results)

if __name__ == "__main__":
    main()
