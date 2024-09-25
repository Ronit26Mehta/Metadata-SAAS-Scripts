#!/bin/bash

print_banner() {
    echo -e "\n\n\033[1;33;40m ####################################################\033[0m"
    echo -e "\033[1;33;40m#\033[0m                                                   \033[1;33;40m#\033[0m"
    echo -e "\033[1;33;40m#\033[0m              Hayabusa Operations Script            \033[0m"
    echo -e "\033[1;33;40m#\033[0m                                                   \033[1;33;40m#\033[0m"
    echo -e "\033[1;33;40m ####################################################\033[0m"
}

print_completion_message() {
    echo -e "\n\033[1;32;40m ####################################################\033[0m"
    echo -e "\033[1;32;40m#\033[0m                                                   \033[1;32;40m#\033[0m"
    echo -e "\033[1;32;40m#\033[0m                Operation Completed                 \033[0m"
    echo -e "\033[1;32;40m#\033[0m  Output stored in: $1  \033[1;32;40m#\033[0m"
    echo -e "\033[1;32;40m#\033[0m                                                   \033[1;32;40m#\033[0m"
    echo -e "\033[1;32;40m ####################################################\033[0m"
}

handle_interrupt() {
    echo -e "\nProcess interrupted."
    exit 1
}

run_command() {
    local cmd="$1"
    local options="$2"
    eval "$cmd $options"
}

save_output_to_file() {
    local output="$1"
    local file_path="$2"
    local directory="$3"

    mkdir -p "$directory"
    local output_file_name=$(basename "$file_path" | sed 's/\.[^.]*$//')_output.txt
    local output_file_path="$directory/$output_file_name"
    echo "$output" > "$output_file_path"
    print_completion_message "$output_file_path"
}

main() {
    trap handle_interrupt SIGINT

    print_banner

    local hayabusa_path="$1"
    local file_path="$2"
    chmod +x "$hayabusa_path"

    if [[ ! -f "$file_path" && ! -d "$file_path" ]]; then
        echo "Invalid file path. Please ensure the file or directory exists and try again."
        exit 1
    fi

    local output=""
    local output_directory=$(dirname "$(realpath "$file_path")")

    # Run all possible operations
    output+="$(run_command "$hayabusa_path csv-timeline -f \"$file_path\" -o \"${output_directory}/csv_timeline.csv\"")\n"
    output+="$(run_command "$hayabusa_path json-timeline -f \"$file_path\" -o \"${output_directory}/json_timeline.json\"")\n"
    output+="$(run_command "$hayabusa_path level-tuning")\n"
    output+="$(run_command "$hayabusa_path list-profiles")\n"
    output+="$(run_command "$hayabusa_path update-rules")\n"
    output+="$(run_command "$hayabusa_path computer-metrics -f \"$file_path\"")\n"
    output+="$(run_command "$hayabusa_path eid-metrics -f \"$file_path\"")\n"
    output+="$(run_command "$hayabusa_path logon-summary -f \"$file_path\"")\n"
    output+="$(run_command "$hayabusa_path pivot-keywords-list -f \"$file_path\"")\n"

    save_output_to_file "$output" "$file_path" "$output_directory"
}

main "$1" "$2"
