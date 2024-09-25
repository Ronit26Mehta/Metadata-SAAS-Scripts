import os
import subprocess
import sys
import argparse
import datetime
import time
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

def handle_interrupt(signum, frame):
    print("\nProcess interrupted.")
    sys.exit(1)

def save_output_to_file(output, file_path, command, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    output_file_name = f"{os.path.splitext(os.path.basename(file_path))[0]}_{command}_output.txt"
    output_file_path = os.path.join(directory, output_file_name)
    
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            if output:
                f.write(f"Command: {command}\n\n")
                f.write(output)
            else:
                f.write(f"Command: {command}\n\n")
                f.write("No output generated.")
    except UnicodeEncodeError as e:
        print(f"Encoding error: {e}")
        print(f"Output content: {output}")
    
    print(f"\nOperation Completed.\nOutput stored in: {output_file_path}")
    time.sleep(2)

def main():
    signal.signal(signal.SIGINT, handle_interrupt)

    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Automate Hayabusa tool for analyzing files.')
    parser.add_argument('file', help='The file path to analyze with Hayabusa.')
    
    args = parser.parse_args()

    # Initialize Hayabusa
    hayabusa_path = "/home/ronit/hayabusa-2.17.0-lin-x64-gnu"
    hayabusa = Hayabusa(hayabusa_path)

    output_dir = f"hayabusa_output_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Run List Profiles (This will always run regardless of file type)
    output, errors = hayabusa.list_profiles()
    save_output_to_file(output, "list_profiles", "list_profiles", output_dir)
    
    file_extension = os.path.splitext(args.file)[1].lower()

    if file_extension == ".evtx":
        # Run all tests for EVTX files
        print(f"Running tests for EVTX file: {args.file}")

        # CSV Timeline
        output_file = os.path.join(output_dir, f"{os.path.splitext(args.file)[0]}_csv_timeline_output.txt")
        output, errors = hayabusa.csv_timeline(args.file, output_file)
        save_output_to_file(output, args.file, "csv-timeline", output_dir)
        
        # JSON Timeline
        output_file = os.path.join(output_dir, f"{os.path.splitext(args.file)[0]}_json_timeline_output.txt")
        output, errors = hayabusa.json_timeline(args.file, output_file)
        save_output_to_file(output, args.file, "json-timeline", output_dir)

        # Computer Metrics
        output, errors = hayabusa.computer_metrics(args.file)
        save_output_to_file(output, args.file, "computer-metrics", output_dir)
        
        # Event ID Metrics
        output, errors = hayabusa.eid_metrics(args.file)
        save_output_to_file(output, args.file, "eid-metrics", output_dir)
        
        # Logon Summary
        output, errors = hayabusa.logon_summary(args.file)
        save_output_to_file(output, args.file, "logon-summary", output_dir)
        
        # Pivot Keywords List
        output, errors = hayabusa.pivot_keywords_list(args.file)
        save_output_to_file(output, args.file, "pivot-keywords-list", output_dir)

        # Search (using placeholder keyword)
        placeholder_keywords = "example"
        output, errors = hayabusa.search(args.file, placeholder_keywords)
        save_output_to_file(output, args.file, "search", output_dir)
    else:
        print(f"Unsupported file type: {file_extension}. No tests were run.")
        sys.exit(1)

    print(f"\nAll applicable tests have been run. Results are stored in the directory: {output_dir}")

if __name__ == "__main__":
    main()
