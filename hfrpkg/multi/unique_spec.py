import sys
import os
import glob
import argparse
import shutil
from AaronTools.input import Theory, FileWriter
from AaronTools.geometry import Geometry
from AaronTools.job_control import SubmitProcess
from AaronTools.theory.job_types import SinglePointJob
from hfrpkg.run_unique import run_jobs
from hfrpkg.utils import get_extensions


def make_spec(method, basis, extension):
    extension_map = {
        "g": ".com",
        "o": ".inp",
        "p": ".in"
    }
    out_map = {
        "g": ".log",
        "o": ".out",
        "p": ".dat"
    }
    ext = extension_map.get(extension.lower())
    out = out_map.get(extension.lower())
    
    if ext is None or out is None:
        print(f"Unknown software code '{extension}'. Please use 'g', 'o', or 'p'.")
        sys.exit(1)
    os.makedirs("unique_files/spec", exist_ok=True)
    folder = "unique_files/spec/"
    index_path = os.path.join(folder, "index.txt")
    shutil.copyfile("unique_files/index.txt", index_path)
    optin, optout = get_extensions(index_path)
    log_files = glob.glob(os.path.join(folder, "*"+ optout))

    if not log_files:
        print(f"No {optout} files found in folder.")
        
        sys.exit(1)

    level = Theory(
        method=method,
        basis=basis,
        job_type=SinglePointJob()
    )
    com_files = []
    
    for log_path in log_files:
        name = os.path.splitext(os.path.basename(log_path))[0]
        com_path = os.path.join(folder, name + ext)

        try:
            geom = Geometry(log_path)
            geom.write(outfile=com_path, theory=level)
        except Exception as e:
            print(f"Error processing {log_path}: {e}")

    cwd = os.getcwd()
    os.chdir(folder)
    try:
        run_jobs()
    finally:
        os.chdir(cwd)

def main_cli():
    parser = argparse.ArgumentParser(description="Generate and submit SP .com files from optimized .log files")
    parser.add_argument("--m", "--method", dest="method", default="m06-2x", help="DFT method (default: m06-2x)")
    parser.add_argument("--b", "--basis", dest="basis", default="def2tzvp", help="Basis set (default: def2tzvp)")
    parser.add_argument(
        "--s", choices=["g", "o", "p"], default="g",
        help="Software to use: 'g' for Gaussian, 'o' for Orca, 'p' for Psi4 (default: 'g')"
    )
    args = parser.parse_args()

    make_spec(method=args.method, basis=args.basis, extension = args.s)

if __name__ == "__main__":
    main_cli()
