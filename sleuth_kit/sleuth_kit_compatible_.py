import os
import subprocess
import datetime
import time
import sys
import signal
import platform

class SleuthKit:
    def __init__(self, sleuthkit_path):
        self.sleuthkit_path = sleuthkit_path
        self.make_executable()

    def make_executable(self):
        if platform.system().lower() == "linux":
            try:
                subprocess.run(["chmod", "+x", self.sleuthkit_path], check=True)
                print(f"Made {self.sleuthkit_path} executable.")
            except subprocess.CalledProcessError as e:
                print(f"Error making {self.sleuthkit_path} executable: {e}")

    def run_command(self, command, options=None):
        if options is None:
            options = []
        cmd = [self.sleuthkit_path] + command.split() + options
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace', shell=True)
            return result.stdout, result.stderr
        except Exception as e:
            print(f"An error occurred while running the command: {e}")
            return None, str(e)

    def fls(self, image_name, offset, options=None):
        if options is None:
            options = []
        options += ["-o", str(offset), image_name]
        return self.run_command("fls", options)

    def mmls(self, image_name, options=None):
        if options is None:
            options = []
        return self.run_command(f"mmls {image_name}", options)

    def fsstat(self, image_name, offset, options=None):
        if options is None:
            options = []
        options += ["-o", str(offset), image_name]
        return self.run_command("fsstat", options)

    def tsk_recover(self, image_name, offset, destination_dir, options=None):
        if options is None:
            options = []
        options += ["-o", str(offset), "-i", "raw", image_name, destination_dir]
        return self.run_command("tsk_recover", options)

    def img_stat(self, image_name, options=None):
        return self.run_command(f"img_stat {image_name}", options)

def print_banner():
    print("\n\n\033[1;33;40m ####################################################\033[0m")
    print("\033[1;33;40m#\033[0m                                                   \033[1;33;40m#\033[0m")
    print("\033[1;33;40m#\033[0m           Sleuth Kit Operations Script             \033[1;33;40m#\033[0m")
    print("\033[1;33;40m#\033[0m                                                   \033[1;33;40m#\033[0m")
    print("\033[1;33;40m ####################################################\033[0m")

def print_completion_message(output_file_path):
    print("\n\033[1;32;40m ####################################################\033[0m")
    print("\033[1;32;40m#\033[0m                                                   \033[1;32;40m#\033[0m")
    print("\033[1;32;40m#\033[0m                Operation Completed                 \033[1;32;40m#\033[0m")
    print(f"\033[1;32;40m#\033[0m  Output stored in: {output_file_path}  \033[1;32;40m#\033[0m")
    print("\033[1;32;40m#\033[0m                                                   \033[1;32;40m#\033[0m")
    print("\033[1;32;40m ####################################################\033[0m")

def handle_interrupt(signum, frame):
    print("\nProcess interrupted.")
    sys.exit(1)

def save_output_to_file(output, file_path, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

    output_file_name = f"{os.path.splitext(os.path.basename(file_path))[0]}_output.txt"
    output_file_path = os.path.join(directory, output_file_name)

    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            if output:
                f.write(output)
            else:
                f.write("No output generated.")
    except UnicodeEncodeError as e:
        print(f"Encoding error: {e}")
        print(f"Output content: {output}")

    print_completion_message(output_file_path)
    time.sleep(2)

def main():
    signal.signal(signal.SIGINT, handle_interrupt)

    print_banner()

    sleuthkit_path = "C:/Path/To/SleuthKit/Binaries"  # Update this to the actual path of Sleuth Kit binaries on your system

    sleuthkit = SleuthKit(sleuthkit_path)

    # Ask user for the operation to perform
    print("\nSelect an operation:")
    print("1. List Files and Directories (fls)")
    print("2. Display Partition Layout (mmls)")
    print("3. Display File System Details (fsstat)")
    print("4. Recover Deleted Files (tsk_recover)")
    print("5. Display Image Details (img_stat)")

    choice = input("Enter the number of the operation: ")

    # Initialize file_path variable
    image_name = None

    # Ask user for the file path if the operation requires it
    if choice in ['1', '2', '3', '4', '5']:
        image_name = input("Enter the path to the disk image file: ")
        if not os.path.exists(image_name):
            print("Invalid file path. Please ensure the file or directory exists and try again.")
            sys.exit(1)

    # Perform the chosen operation
    if choice == '1':
        offset = input("Enter the offset value: ")
        output, errors = sleuthkit.fls(image_name, offset)
    elif choice == '2':
        output, errors = sleuthkit.mmls(image_name)
    elif choice == '3':
        offset = input("Enter the offset value: ")
        output, errors = sleuthkit.fsstat(image_name, offset)
    elif choice == '4':
        offset = input("Enter the offset value: ")
        destination_dir = input("Enter the destination directory for recovered files: ")
        output, errors = sleuthkit.tsk_recover(image_name, offset, destination_dir)
    elif choice == '5':
        output, errors = sleuthkit.img_stat(image_name)
    else:
        print("Invalid choice.")
        sys.exit(1)

    # Introduce a small delay to ensure the output is fully captured
    time.sleep(1)

    # Save the output to a text file in an output directory with a timestamp
    script_directory = os.path.dirname(os.path.abspath(__file__))
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    output_directory = os.path.join(script_directory, f"sleuthkit_output_{timestamp}")

    if choice in ['1', '2', '3', '4', '5']:
        if image_name:
            save_output_to_file(output, image_name, output_directory)

    if errors:
        print(f"\nErrors:\n{errors}")

if __name__ == "__main__":
    main()
