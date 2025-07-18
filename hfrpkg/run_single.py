import sys
import glob
from AaronTools.job_control import SubmitProcess

def run_jobs():
    com_files = glob.glob("*.com")
    if not com_files:
        print("No .com files found in current directory.")
        sys.exit(1)

    for f in com_files:
        submit_process = SubmitProcess(f, 12, 8, 12)

         # submit job
        try:
            submit_process.submit()
        except Exception as e:
            print(f"failed to submit {f}: {e}")
def main_cli():
    run_jobs()

if __name__ == "__main__":
    main_cli()
