import sys
import os
import glob
import argparse
from AaronTools.input import Theory, FileWriter
from AaronTools.geometry import Geometry
from AaronTools.job_control import SubmitProcess
from AaronTools.utils import grab_geom


def make_spec(method, basis):
    folder = "unique_com_files/"
    log_files = glob.glob(os.path.join(folder, "*.log"))

    if not log_files:
        print("No .log files found in unique_com_files.")
        sys.exit(1)

    theory = Theory(method=method, basis=basis, job_type=["SP"])
    com_files = []

    for log_path in log_files:
        name = os.path.splitext(os.path.basename(log_path))[0]
        com_path = os.path.join(folder, name + ".com")

        try:
            geom = Geometry(grab_geom(log_path))
            FileWriter.write_file(geom=geom, style="com", outfile=com_path, theory=theory)
            com_files.append(com_path)
            print(f"Wrote: {com_path}")
        except Exception as e:
            print(f"Error processing {log_path}: {e}")

    for com_path in com_files:
        try:
            submit_process = SubmitProcess(com_path, 12, 8, 12)
            submit_process.submit()
            print(f"Submitted: {com_path}")
        except Exception as e:
            print(f"Failed to submit {com_path}: {e}")

def main_cli():
    parser = argparse.ArgumentParser(description="Generate and submit SP .com files from optimized .log files")
    parser.add_argument("--m", "--method", dest="method", default="m06-2x", help="DFT method (default: m06-2x)")
    parser.add_argument("--b", "--basis", dest="basis", default="def2tzvp", help="Basis set (default: def2tzvp)")
    args = parser.parse_args()

    make_spec(method=args.method, basis=args.basis)

if __name__ == "__main__":
    main_cli()
