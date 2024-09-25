import os
import subprocess
import argparse
import datetime
import time
import signal
import sys

def print_banner():
    print("\n\n\033[1;33;40m ####################################################\033[0m")
    print("\033[1;33;40m#\033[0m                                                   \033[1;33;40m#\033[0m")
    print("\033[1;33;40m#\033[0m       Hachoir Metadata Extraction Script          \033[1;33;40m#\033[0m")
    print("\033[1;33;40m#\033[0m                                                   \033[1;33;40m#\033[0m")
    print("\033[1;33;40m ####################################################\033[0m")

def print_completion_message(output_file_path):
    print("\n\033[1;32;40m ####################################################\033[0m")
    print("\033[1;32;40m#\033[0m                                                   \033[1;32;40m#\033[0m")
    print("\033[1;32;40m#\033[0m           Metadata Extraction Completed           \033[1;32;40m#\033[0m")
    print(f"\033[1;32;40m#\033[0m  Output stored in: {output_file_path}  \033[1;32;40m#\033[0m")
    print("\033[1;32;40m#\033[0m                                                   \033[1;32;40m#\033[0m")
    print("\033[1;32;40m ####################################################\033[0m")

def print_error_message(message):
    print("\n\033[1;31;40m ####################################################\033[0m")
    print("\033[1;31;40m#\033[0m                                                   \033[1;31;40m#\033[0m")
    print(f"\033[1;31;40m#\033[0m           ERROR: {message}                        \033[1;31;40m#\033[0m")
    print("\033[1;31;40m#\033[0m                                                   \033[1;31;40m#\033[0m")
    print("\033[1;31;40m ####################################################\033[0m")

def handle_interrupt(signum, frame):
    print("\nProcess interrupted.")
    sys.exit(1)

def run_hachoir_metadata(file_path, options):
    # Construct the hachoir-metadata command
    hachoir_command = f"hachoir-metadata {options} \"{file_path}\""
    
    try:
        # Run the hachoir-metadata command and capture the output
        result = subprocess.run(hachoir_command, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            # If the command failed, check if there is an error message
            error_message = result.stderr.strip()
            if error_message:
                print_error_message(error_message)
            else:
                print_error_message("Unknown error occurred while running hachoir-metadata.")
            return None
        
        # Return the captured output
        return result.stdout
    
    except Exception as e:
        print_error_message(f"An exception occurred: {str(e)}")
        return None

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
    
    parser = argparse.ArgumentParser(description='Automate hachoir-metadata tool for extracting metadata from files.')
    parser.add_argument('file', help='The file path to analyze with hachoir-metadata.')
    parser.add_argument('--type', action='store_true', help='Only display file type (description).')
    parser.add_argument('--mime', action='store_true', help='Only display MIME type.')
    parser.add_argument('--level', type=int, help='Quantity of information to display from 1 to 9 (9 is the maximum).')
    parser.add_argument('--raw', action='store_true', help='Raw output.')
    parser.add_argument('--bench', action='store_true', help='Run benchmark.')
    parser.add_argument('--force-parser', help='Force a specific parser.')
    parser.add_argument('--parser-list', action='store_true', help='List all parsers then exit.')
    parser.add_argument('--profiler', action='store_true', help='Run profiler.')
    parser.add_argument('--version', action='store_true', help='Display version and exit.')
    parser.add_argument('--quality', type=float, help='Information quality (0.0=fastest, 1.0=best, default is 0.5).')
    parser.add_argument('--maxlen', type=int, help='Maximum string length in characters (0 means unlimited).')
    parser.add_argument('--verbose', action='store_true', help='Verbose mode.')
    parser.add_argument('--debug', action='store_true', help='Debug mode.')

    args = parser.parse_args()

    # Construct the options string to include all possible tests
    options = "--type --mime --raw --bench --profiler --verbose --debug"
    
    # Optionally include additional options based on arguments
    if args.level:
        options += f" --level={args.level}"
    if args.force_parser:
        options += f" --force-parser={args.force_parser}"
    if args.parser_list:
        options += " --parser-list"
    if args.version:
        options += " --version"
    if args.quality:
        options += f" --quality={args.quality}"
    if args.maxlen:
        options += f" --maxlen={args.maxlen}"

    print_banner()
    
    # Run hachoir-metadata with the specified options and file
    output = run_hachoir_metadata(args.file, options)
    
    if output is not None:
        # Introduce a small delay to ensure that the output is fully captured
        time.sleep(1)

        # Save the output to a text file in an output directory with a timestamp
        script_directory = os.path.dirname(os.path.abspath(__file__))
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        output_directory = os.path.join(script_directory, f"output_{timestamp}")
        
        save_output_to_file(output, args.file, output_directory)

if __name__ == "__main__":
    main()
