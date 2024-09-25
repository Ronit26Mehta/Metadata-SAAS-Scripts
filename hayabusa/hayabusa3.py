import os
import subprocess
import datetime
import time
import sys
import signal
import platform

class Hayabusa:
    def __init__(self, hayabusa_path):
        self.hayabusa_path = hayabusa_path
        self.make_executable()
    
    def make_executable(self):
        if platform.system().lower() == "linux":
            try:
                subprocess.run(["chmod", "+x", self.hayabusa_path], check=True)
                print(f"Made {self.hayabusa_path} executable.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to make {self.hayabusa_path} executable: {e}")
        elif platform.system().lower() == "windows":
            # No need to change permissions on Windows
            print(f"Path is set for Windows: {self.hayabusa_path}")

    def run_command(self, command, options=None):
        if options is None:
            options = []
        cmd = [self.hayabusa_path, command] + options
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace')
            return result.stdout, result.stderr
        except Exception as e:
            print(f"An error occurred while running the command: {e}")
            return None, str(e)
    
    def csv_timeline(self, input_file, output_file, options=None):
        if options is None:
            options = []
        options += ["-f", input_file, "-o", output_file]
        return self.run_command("csv-timeline", options)
    
    def json_timeline(self, input_file, output_file, options=None):
        if options is None:
            options = []
        options += ["-f", input_file, "-o", output_file]
        return self.run_command("json-timeline", options)

    def level_tuning(self, options=None):
        return self.run_command("level-tuning", options)
    
    def list_profiles(self, options=None):
        return self.run_command("list-profiles", options)
    
    def set_default_profile(self, profile, options=None):
        if options is None:
            options = []
        options += ["-p", profile]
        return self.run_command("set-default-profile", options)
    
    def update_rules(self, options=None):
        return self.run_command("update-rules", options)
    
    def computer_metrics(self, input_file, options=None):
        if options is None:
            options = []
        options += ["-f", input_file]
        return self.run_command("computer-metrics", options)
    
    def eid_metrics(self, input_file, options=None):
        if options is None:
            options = []
        options += ["-f", input_file]
        return self.run_command("eid-metrics", options)
    
    def logon_summary(self, input_file, options=None):
        if options is None:
            options = []
        options += ["-f", input_file]
        return self.run_command("logon-summary", options)
    
    def pivot_keywords_list(self, input_file, options=None):
        if options is None:
            options = []
        options += ["-f", input_file]
        return self.run_command("pivot-keywords-list", options)

    def search(self, input_file, keywords, options=None):
        if options is None:
            options = []
        options += ["-f", input_file, "-s", keywords]
        return self.run_command("search", options)

def print_banner():
    print("\n\n\033[1;33;40m ####################################################\033[0m")
    print("\033[1;33;40m#\033[0m                                                   \033[1;33;40m#\033[0m")
    print("\033[1;33;40m#\033[0m              Hayabusa Operations Script            \033[1;33;40m#\033[0m")
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

    hayabusa_path = "C:/Users/kavis/OneDrive/Desktop/School/hayabusa-2.17.0-win-x64.exe"

    hayabusa = Hayabusa(hayabusa_path)

    # Ask user for the operation to perform
    print("\nSelect an operation:")
    print("1. CSV Timeline")
    print("2. JSON Timeline")
    print("3. Level Tuning")
    print("4. List Profiles")
    print("5. Set Default Profile")
    print("6. Update Rules")
    print("7. Computer Metrics")
    print("8. Event ID Metrics")
    print("9. Logon Summary")
    print("10. Pivot Keywords List")
    print("11. Search")

    choice = input("Enter the number of the operation: ")

    # Initialize file_path variable
    file_path = None

    # Ask user for the file path if the operation requires it
    if choice in ['1', '2', '7', '8', '9', '10', '11']:
        file_path = input("Enter the path to the EVTX file or directory: ")
        if not os.path.exists(file_path):
            print("Invalid file path. Please ensure the file or directory exists and try again.")
            sys.exit(1)

    # Perform the chosen operation
    if choice == '1':
        output_file = input("Enter the path to save the CSV timeline: ")
        output, errors = hayabusa.csv_timeline(file_path, output_file)
    elif choice == '2':
        output_file = input("Enter the path to save the JSON timeline: ")
        output, errors = hayabusa.json_timeline(file_path, output_file)
    elif choice == '3':
        output, errors = hayabusa.level_tuning()
    elif choice == '4':
        output, errors = hayabusa.list_profiles()
        # Default output file path for operations without a specific file path
        output_file = "list_profiles_output.txt"
    elif choice == '5':
        profile = input("Enter the profile to set as default: ")
        output, errors = hayabusa.set_default_profile(profile)
    elif choice == '6':
        output, errors = hayabusa.update_rules()
    elif choice == '7':
        output, errors = hayabusa.computer_metrics(file_path)
    elif choice == '8':
        output, errors = hayabusa.eid_metrics(file_path)
    elif choice == '9':
        output, errors = hayabusa.logon_summary(file_path)
    elif choice == '10':
        output, errors = hayabusa.pivot_keywords_list(file_path)
    elif choice == '11':
        keywords = input("Enter the keywords or regex to search for: ")
        output, errors = hayabusa.search(file_path, keywords)
    else:
        print("Invalid choice.")
        sys.exit(1)

    # Introduce a small delay to ensure the output is fully captured
    time.sleep(1)

    # Save the output to a text file in an output directory with a timestamp
    script_directory = os.path.dirname(os.path.abspath(__file__))
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    output_directory = os.path.join(script_directory, f"hayabusa_output_{timestamp}")
    
    if choice in ['1', '2', '7', '8', '9', '10', '11']:
        if file_path:
            save_output_to_file(output, file_path, output_directory)
    elif choice == '4':
        save_output_to_file(output, "list_profiles_output.txt", output_directory)
    else:
        print("\nOutput:\n" + output)

    if errors:
        print(f"\nErrors:\n{errors}")

if __name__ == "__main__":
    main()
