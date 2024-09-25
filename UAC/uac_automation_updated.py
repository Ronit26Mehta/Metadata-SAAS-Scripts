import os
import subprocess
from pathlib import Path

def run_command(command):
    """
    Run the given command and handle exceptions.
    """
    try:
        subprocess.run(command, check=True, shell=True)
        print(f"Command '{command}' executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

def extract_tar_gz(file_path, output_dir):
    """
    Extract a tar.gz file to the specified output directory.
    """
    extract_command = f"tar -xzvf {file_path} -C {output_dir}"
    run_command(extract_command)

def main():
    # Step 1: Clone the repo
    repo_url = "https://github.com/tclahr/uac.git"
    clone_command = f"git clone {repo_url}"
    
    # Clone the repository
    print("Cloning the repository...")
    run_command(clone_command)

    # Change directory to the cloned repo
    os.chdir('uac')

    # Step 2: User selects a scenario
    print("\nSelect a scenario to run:")
    print("1. Collect all artifacts based on the full profile, and create the output file in /tmp.")
    print("2. Collect all live_response, and the bodyfile/bodyfile.yaml artifact, and create the output file in the current directory.")
    print("3. Collect all artifacts based on the full profile, but exclude the bodyfile/bodyfile.yaml artifact, and create the output file in /tmp.")
    print("4. Collect the memory dump, then all artifacts based on the full profile.")
    print("5. Collect the memory dump, then all artifacts based on the ir_triage profile excluding the bodyfile/bodyfile.yaml artifact.")
    print("6. Collect all artifacts based on the full profile, but limit the data collection based on the date range provided.")
    print("7. Collect all but live response artifacts from a Linux disk image mounted in /mnt/ewf.")
    
    choice = input("\nEnter the number of the scenario you want to run: ")

    # Step 3: Determine the output directory (Desktop)
    desktop_path = Path.home() / "Desktop" / "uac_output"
    desktop_path.mkdir(parents=True, exist_ok=True)

    # Step 4: Run the selected scenario with output directed to the Desktop
    if choice == '1':
        scenario = f"./uac -p full {desktop_path}"
    elif choice == '2':
        scenario = f"./uac -a live_response/*,bodyfile/bodyfile.yaml {desktop_path}"
    elif choice == '3':
        scenario = f"./uac -p full -a !bodyfile/bodyfile.yaml {desktop_path}"
    elif choice == '4':
        scenario = f"./uac -a artifacts/memory_dump/avml.yaml -p full {desktop_path}"
    elif choice == '5':
        scenario = f"./uac -a ./artifacts/memory_dump/avml.yaml -p ir_triage -a !artifacts/bodyfile/bodyfile.yaml {desktop_path}"
    elif choice == '6':
        scenario = f"./uac -p full {desktop_path} --date-range-start 2021-05-01 --date-range-end 2021-08-31"
    elif choice == '7':
        scenario = f"./uac -p full -a !live_response/* {desktop_path} --mount-point /mnt/ewf --operating-system linux"
    else:
        print("Invalid selection. Exiting.")
        return

    print(f"\nExecuting scenario {choice}: {scenario}")
    run_command(scenario)

    # Step 5: Extract the tar.gz file if it exists
    output_tar_gz = next(desktop_path.glob("*.tar.gz"), None)
    if output_tar_gz:
        print(f"\nExtracting {output_tar_gz} to {desktop_path}...")
        extract_tar_gz(output_tar_gz, desktop_path)
    else:
        print("\nNo tar.gz file found to extract.")

if __name__ == "__main__":
    main()
