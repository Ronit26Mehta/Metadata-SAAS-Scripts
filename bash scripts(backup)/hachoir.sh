#!/bin/bash

print_banner() {
    echo -e "\n\n\033[1;33;40m ####################################################\033[0m"
    echo -e "\033[1;33;40m#\033[0m                                                   \033[1;33;40m#\033[0m"
    echo -e "\033[1;33;40m#\033[0m       Hachoir Metadata Extraction Script          \033[0m"
    echo -e "\033[1;33;40m#\033[0m                                                   \033[1;33;40m#\033[0m"
    echo -e "\033[1;33;40m ####################################################\033[0m"
}

print_completion_message() {
    echo -e "\n\033[1;32;40m ####################################################\033[0m"
    echo -e "\033[1;32;40m#\033[0m                                                   \033[1;32;40m#\033[0m"
    echo -e "\033[1;32;40m#\033[0m           Metadata Extraction Completed           \033[1;32;40m#\033[0m"
    echo -e "\033[1;32;40m#\033[0m  Output stored in: $1  \033[1;32;40m#\033[0m"
    echo -e "\033[1;32;40m#\033[0m                                                   \033[1;32;40m#\033[0m"
    echo -e "\033[1;32;40m ####################################################\033[0m"
}

handle_interrupt() {
    echo -e "\nProcess interrupted."
    exit 1
}

run_hachoir_metadata() {
    local file_path="$1"
    local hachoir_command="hachoir-metadata \"$file_path\""
    local output=$(eval "$hachoir_command")
    echo "$output"
}

save_output_to_file() {
    local output="$1"
    local file_path="$2"
    local directory="$3"

    mkdir -p "$directory"
    local output_file_name=$(basename "$file_path" | sed 's/\.[^.]*$//')_metadata.txt
    local output_file_path="$directory/$output_file_name"
    echo "$output" > "$output_file_path"
    print_completion_message "$output_file_path"
}

main() {
    trap handle_interrupt SIGINT

    print_banner

    local file_path="$1"

    if [[ ! -f "$file_path" ]]; then
        echo "Invalid file path. Please ensure the file exists and try again."
        exit 1
    fi

    local output=$(run_hachoir_metadata "$file_path")
    sleep 1

    local timestamp=$(date '+%Y%m%d_%H%M%S')
    local script_directory=$(dirname "$(realpath "$0")")
    local output_directory="$script_directory/output_$timestamp"

    save_output_to_file "$output" "$file_path" "$output_directory"
}

main "$1"
