#!/usr/bin/env python3

import os
import glob
import shutil

def load_unique_inchi_map(index_path):
    """Maps InChI → filename from unique_com_files/index.txt"""
    inchi_to_filename = {}
    with open(index_path, "r") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 2 and not parts[0].startswith("Level"):
                filename, inchi = parts[0], parts[1]
                inchi_to_filename[inchi] = filename
    return inchi_to_filename

def fill_logs():
    unique_index_path = os.path.join("unique_com_files", "index.txt")
    if not os.path.exists(unique_index_path):
        print("Missing unique_com_files/index.txt")
        return

    inchi_map = load_unique_inchi_map(unique_index_path)

    for mhfr_dir in glob.glob("*.mhfr"):
        index_file = os.path.join(mhfr_dir, "index.txt")
        if not os.path.exists(index_file):
            print(f"Skipping {mhfr_dir}, missing index.txt")
            continue

        with open(index_file, "r") as f:
            lines = f.readlines()[3:]

        for line in lines:
            if line.startswith("Level") or not line.strip():
                continue
            parts = line.strip().split("\t")
            if len(parts) < 2:
                continue

            mhfr_filename, inchi = parts[0], parts[1]
            if inchi not in inchi_map:
                print(f"[WARNING] InChI not found: {inchi}")
                continue

            unique_name = inchi_map[inchi] + ".log"
            src_log_path = os.path.join("unique_com_files", unique_name)
            dst_log_path = os.path.join(mhfr_dir, mhfr_filename + ".log")

            if not os.path.exists(src_log_path):
                print(f"[WARNING] Missing log file: {src_log_path}")
                continue

            shutil.copyfile(src_log_path, dst_log_path)
            #print(f"Copied {src_log_path} → {dst_log_path}")

if __name__ == "__main__":
    fill_logs()

