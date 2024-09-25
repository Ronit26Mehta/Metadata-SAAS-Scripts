import os
import subprocess
import datetime
import time
import sys
import signal
import platform

def print_banner():
    print("\n\n\033[1;33;40m ####################################################\033[0m")
    print("\033[1;33;40m#\033[0m                                                   \033[1;33;40m#\033[0m")
    print("\033[1;33;40m#\033[0m       Exiftool Metadata Extraction Script         \033[1;33;40m#\033[0m")
    print("\033[1;33;40m#\033[0m                                                   \033[1;33;40m#\033[0m")
    print("\033[1;33;40m ####################################################\033[0m")

def print_completion_message(output_file_path):
    print("\n\033[1;32;40m ####################################################\033[0m")
    print("\033[1;32;40m#\033[0m                                                   \033[1;32;40m#\033[0m")
    print("\033[1;32;40m#\033[0m           Metadata Extraction Completed           \033[1;32;40m#\033[0m")
    print(f"\033[1;32;40m#\033[0m  Output stored in: {output_file_path}  \033[1;32;40m#\033[0m")
    print("\033[1;32;40m#\033[0m                                                   \033[1;32;40m#\033[0m")
    print("\033[1;32;40m ####################################################\033[0m")

def handle_interrupt(signum, frame):
    print("\nProcess interrupted.")
    sys.exit(1)

def make_executable(file_path):
    if platform.system().lower() == "linux":
        try:
            subprocess.run(["chmod", "+x", file_path], check=True)
            print(f"Made {file_path} executable.")
        except subprocess.CalledProcessError as e:
            print(f"Error making {file_path} executable: {e}")

def run_exiftool(file_path):
    # Determine the platform and set the path to Exiftool accordingly
    if platform.system().lower() == "windows":
        exiftool_path = r"C:\Users\kavis\Downloads\exiftool-12.93_64\exiftool(-k).exe"
    else:
        exiftool_path = "/usr/local/bin/exiftool"  # Default path for Unix-based systems

    # Make Exiftool executable if on Unix-based systems
    if platform.system().lower() != "windows":
        make_executable(exiftool_path)

    # Construct the Exiftool command
    exiftool_command = [exiftool_path, file_path]

    # Run the Exiftool command and capture the output
    result = subprocess.run(exiftool_command, capture_output=True, text=True)
    
    # Return the captured output
    return result.stdout

def save_output_to_file(output, file_path, directory):
    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Construct the output file path based on the original file name
    output_file_name = f"{os.path.splitext(os.path.basename(file_path))[0]}_metadata.txt"
    output_file_path = os.path.join(directory, output_file_name)
    
    # Write the output to the file
    with open(output_file_path, 'w') as f:
        f.write(output)
    
    print_completion_message(output_file_path)
    
    # Introduce a small delay to ensure all operations are complete
    time.sleep(2)

def main():
    # Set up signal handling for interruptions
    signal.signal(signal.SIGINT, handle_interrupt)

    print_banner()

    # Ask user for the file path
    file_path = input("Enter the path to the file: ")
    
    # Validate file path
    if not os.path.isfile(file_path):
        print("Invalid file path. Please ensure the file exists and try again.")
        sys.exit(1)
    
    # Run Exiftool with the specified file
    output = run_exiftool(file_path)
    
    # Introduce a small delay to ensure that the output is fully captured
    time.sleep(1)

    # Save the output to a text file in an output directory with a timestamp
    script_directory = os.path.dirname(os.path.abspath(__file__))
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    output_directory = os.path.join(script_directory, f"output_{timestamp}")
    
    save_output_to_file(output, file_path, output_directory)

if __name__ == "__main__":
    main()
