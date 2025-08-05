

import sys
import os
import glob
import argparse
from AaronTools.input import Theory, FileWriter
from AaronTools.geometry import Geometry
from AaronTools.job_control import SubmitProcess
from AaronTools.theory.job_types import SinglePointJob
from hfrpkg.run_single import run_jobs

def make_spec(method, basis, extension):
    
    folder = os.getcwd()
    log_files = glob.glob(os.path.join(folder, "*.log"))
    extension_map = {
        "g": ".com",
        "o": ".inp",
        "p": ".in"
    }
    ext = extension_map.get(extension.lower())
    if ext is None:
        print(f"Unknown software code '{extension}'. Please use 'g', 'o', or 'p'.")
        sys.exit(1)
    if not log_files:
        print("No .log files found in folder.")
        
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
            print(f"Wrote: {com_path}")
        except Exception as e:
            print(f"Error processing {log_path}: {e}")
            
    run_jobs()

    
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
