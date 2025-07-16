#!/usr/bin/env python3

import os
from hfrpkg.runner import run_reaction
reaction_map = {
    "1": "isogyric",
    "2": "isodesmic",
    "3": "hypohomodesmotic",
    "4": "homodesmotic"
}

def main(input_file):
    with open(input_file, "r") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) != 2:
                print(f"[SKIP] Line {i} malformed: {line}")
                continue

            level, smiles = parts
            reaction_type = reaction_map.get(level)
            if not reaction_type:
                print(f"[SKIP] Invalid level {level} on line {i}")
                continue

            outfolder = f"{i}.mhfr"
            print(f"[RUN] Line {i}: level={level}, type={reaction_type}, SMILES={smiles}, folder={outfolder}")

            try:
                run_reaction(
                    action_type="write",
                    reaction_type=reaction_type,
                    input_smiles=smiles,
                    lhs=None,
                    rhs=None,
                    substruct=None,
                    replacement=None,
                    outfolder=outfolder
                )
                print(f"[DONE] Folder written: {outfolder}")
            except Exception as e:
                print(f"[ERROR] Line {i} failed: {e}")
def main_cli():
    import sys
    if len(sys.argv) != 2:
        print("Usage: multi <input_file.txt>")
        sys.exit(1)
    main(sys.argv[1])

if __name__ == "__main__":
    main_cli()
