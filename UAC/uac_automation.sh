#!/bin/bash

run_command() {
    if $1; then
        echo "Command '$1' executed successfully."
    else
        echo "Error executing command: $1"
        exit 1
    fi
}

extract_tar_gz() {
    local file_path=$1
    local output_dir=$2
    local extract_command="tar -xzvf $file_path -C $output_dir"
    run_command "$extract_command"
}

main() {
    local input_file=$1
    if [[ -z $input_file ]]; then
        echo "No input file provided. Usage: ./uac_automation.sh <input_file>"
        exit 1
    fi

    local repo_url="https://github.com/tclahr/uac.git"
    local clone_command="git clone $repo_url"

    echo "Cloning the repository..."
    run_command "$clone_command"

    cd uac || { echo "Failed to change directory to uac."; exit 1; }

    local desktop_path="/home/kali/Desktop/uac_output"
    mkdir -p "$desktop_path"

    # Determine which scenario to run based on the input file type
    local scenario=""
    case "$input_file" in
        *.tar.gz) scenario="./uac -p full $desktop_path" ;;
        *.yaml) scenario="./uac -a live_response/*,bodyfile/bodyfile.yaml $desktop_path" ;;
        *.img) scenario="./uac -p full -a !live_response/* $desktop_path --mount-point /mnt/ewf --operating-system linux" ;;
        *.dump) scenario="./uac -a artifacts/memory_dump/avml.yaml -p full $desktop_path" ;;
        *) echo "Unsupported file type. Exiting."; exit 1 ;;
    esac

    echo -e "\nExecuting scenario for input file $input_file: $scenario"
    run_command "$scenario"

    output_tar_gz=$(ls "$desktop_path"/*.tar.gz 2>/dev/null)
    if [[ -n $output_tar_gz ]]; then
        echo -e "\nExtracting $output_tar_gz to $desktop_path..."
        extract_tar_gz "$output_tar_gz" "$desktop_path"
    else
        echo -e "\nNo tar.gz file found to extract."
    fi
}

main "$1"
