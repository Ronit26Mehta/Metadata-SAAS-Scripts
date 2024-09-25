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
    
    print(f"\nOperation Completed.\nOutput stored in: {output_file_path}")
    time.sleep(2)

def main():
    signal.signal(signal.SIGINT, handle_interrupt)

    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Automate Hayabusa tool for analyzing EVTX files.')
    parser.add_argument('file', help='The file path to analyze with Hayabusa.')
    parser.add_argument('--csv-timeline', help='Run CSV Timeline', action='store_true')
    parser.add_argument('--json-timeline', help='Run JSON Timeline', action='store_true')
    parser.add_argument('--level-tuning', help='Run Level Tuning', action='store_true')
    parser.add_argument('--list-profiles', help='List Profiles', action='store_true')
    parser.add_argument('--set-default-profile', help='Set Default Profile')
    parser.add_argument('--update-rules', help='Update Rules', action='store_true')
    parser.add_argument('--computer-metrics', help='Run Computer Metrics', action='store_true')
    parser.add_argument('--eid-metrics', help='Run EID Metrics', action='store_true')
    parser.add_argument('--logon-summary', help='Run Logon Summary', action='store_true')
    parser.add_argument('--pivot-keywords-list', help='Run Pivot Keywords List', action='store_true')
    parser.add_argument('--search', help='Search for specific keywords')
    
    args = parser.parse_args()

    # Initialize Hayabusa
    hayabusa_path = "/home/ronit/hayabusa-2.17.0-lin-x64-gnu"
    hayabusa = Hayabusa(hayabusa_path)

    output_file = f"{os.path.splitext(args.file)[0]}_output.txt"

    if args.csv_timeline:
        output, errors = hayabusa.csv_timeline(args.file, output_file)
    elif args.json_timeline:
        output, errors = hayabusa.json_timeline(args.file, output_file)
    elif args.level_tuning:
        output, errors = hayabusa.level_tuning()
    elif args.list_profiles:
        output, errors = hayabusa.list_profiles()
    elif args.set_default_profile:
        output, errors = hayabusa.set_default_profile(args.set_default_profile)
    elif args.update_rules:
        output, errors = hayabusa.update_rules()
    elif args.computer_metrics:
        output, errors = hayabusa.computer_metrics(args.file)
    elif args.eid_metrics:
        output, errors = hayabusa.eid_metrics(args.file)
    elif args.logon_summary:
        output, errors = hayabusa.logon_summary(args.file)
    elif args.pivot_keywords_list:
        output, errors = hayabusa.pivot_keywords_list(args.file)
    elif args.search:
        output, errors = hayabusa.search(args.file, args.search)
    else:
        print("No valid operation provided.")
        sys.exit(1)

    if output:
        save_output_to_file(output, args.file, "hayabusa_output")

    if errors:
        print(f"\nErrors:\n{errors}")

if __name__ == "__main__":
    main()
