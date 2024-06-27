#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NO_COLOR='\033[0m'
TICK="\xE2\x9C\x94"
CROSS="\xE2\x9D\x8C"

spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\'
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

text_art=(
"░░░░░░░░░░░░░░░▄▄░░░░░░░░░░░"
"░░░░░░░░░░░░░░█░░█░░░░░░░░░░"
"░░░░░░░░░░░░░░█░░█░░░░░░░░░░"
"░░░░░░░░░░░░░░█░░█░░░░░░░░░░"
"░░░░░░░░░░░░░░█░░█░░░░░░░░░░"   
"██████▄███▄████░░███▄░░░░░░░  ██╗███╗░░██╗░██████╗████████╗░█████╗░" 
"▓▓▓▓▓▓█░░░█░░░█░░█░░░███░░░░  ██║████╗░██║██╔════╝╚══██╔══╝██╔══██╗"
"▓▓▓▓▓▓█░░░█░░░█░░█░░░█░░█░░░  ██║██╔██╗██║╚█████╗░░░░██║░░░███████║"
"▓▓▓▓▓▓█░░░░░░░░░░░░░░█░░█░░░  ██║██║╚████║░╚═══██╗░░░██║░░░██╔══██║"
"▓▓▓▓▓▓█░░░░░░░░░░░░░░░░█░░░░  ██║██║░╚███║██████╔╝░░░██║░░░██║░░██║"
"▓▓▓▓▓▓█░░░░░░░░░░░░░░██░░░░░  ╚═╝╚═╝░░╚══╝╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝"
"▓▓▓▓▓▓█████░░░░░░░░░██░░░░░░"
"███████▀▀███████████▀"
)

for line in "${text_art[@]}"; do
    echo -e "${GREEN}$line${NO_COLOR}"
    sleep 0.1
done

current_dir=$(dirname "$(readlink -f "$0")")
rickphis_dir="$current_dir"
rickphis_opt_dir="/opt/$(basename "$rickphis_dir")"


if [ -d "$rickphis_dir" ]; then
    if [ "$rickphis_dir" == "$rickphis_opt_dir" ]; then
        echo -e "\n${GREEN}$TICK${NO_COLOR} RickPhis directory in /opt."
    else
        echo -e "\nRickPhis directory found. Moving to /opt directory..."
        (sudo mv "$rickphis_dir" /opt/ & spinner $!)
        sleep 2
        echo -e "\n${GREEN}$TICK${NO_COLOR} RickPhis directory successfully moved to /opt."
    fi
else
    echo -e "\n${RED}$CROSS${NO_COLOR} RickPhis directory not found."
fi

if command -v python3 &> /dev/null; then
    echo -e "${GREEN}$TICK${NO_COLOR} Python found: $(python3 --version)"
else
    echo -e "${YELLOW}WARNING: ${RED}$CROSS${NO_COLOR} Python not found. Installing Python..."
    (sudo apt update && sudo apt install -y python3 python3-pip & spinner $!)
    sleep 1
    if command -v python3 &> /dev/null; then
        echo -e "${GREEN}$TICK${NO_COLOR} Python successfully installed: $(python3 --version)"
    else
        echo -e "${YELLOW}WARNING: ${RED}$CROSS${NO_COLOR} Python installation failed. Please install manually."
        exit 1
    fi
fi

requirements=("colorama" "argparse" "selenium" "webdriver-manager" "pyngrok")

for package in "${requirements[@]}"
do
    sleep 1
    if python3 -c "import $package" &> /dev/null; then
        echo -e "${GREEN}$TICK${NO_COLOR} $package is installed"
    else
        echo -e "${YELLOW}WARNING: ${RED}$CROSS${NO_COLOR} $package is not installed. Installing..."
        (pip3 install $package & spinner $!)
        sleep 1
        if python3 -c "import $package" &> /dev/null; then
            echo -e "${GREEN}$TICK${NO_COLOR} $package successfully installed"
        else
            echo -e "${YELLOW}WARNING: ${RED}$CROSS${NO_COLOR} $package installation failed"
        fi
    fi
done

echo -e "${GREEN}All checks completed. Environment is ready!${NO_COLOR}\n"

read -p "Do you want to create an alias? (Y/n):" alias_choice

if [ "$alias_choice" == "y" ] || [ "$alias_choice" == "Y" ]; then
    if [ -n "$BASH_VERSION" ]; then
        shell_rc="$HOME/.bashrc"
    elif [ -n "$ZSH_VERSION" ]; then
        shell_rc="$HOME/.zshrc"
    else
        echo -e "${YELLOW}WARNING: ${RED}$CROSS${NO_COLOR} Unsupported shell. Alias not created."
        exit 1
    fi

    echo "alias Rickphis='python3 /opt/$(basename "$rickphis_dir")/server.py'" >> $shell_rc
    source $shell_rc
    echo -e "${GREEN}$TICK${NO_COLOR} Alias successfully created: Rickphis"
else
    echo -e "Alias creation cancelled."
fi
