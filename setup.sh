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

current_dir=$(dirname "$(readlink -f "$0")")
rickphis_dir="$current_dir"
rickphis_opt_dir="/opt/$(basename "$rickphis_dir")"

echo -e "${GREEN}Setting up the environment for RickPhis...${NO_COLOR}"

if [ -d "$rickphis_dir" ]; then
    if [ "$rickphis_dir" == "$rickphis_opt_dir" ]; then
        echo -e "\n${GREEN}$TICK${NO_COLOR} RickPhis directory already in /opt."
    else
        echo -e "\nMoving RickPhis directory to /opt..."
        (sudo mv "$rickphis_dir" /opt/ & spinner $!)
        echo -e "\n${GREEN}$TICK${NO_COLOR} RickPhis directory successfully moved to /opt."
    fi
else
    echo -e "\n${RED}$CROSS${NO_COLOR} RickPhis directory not found."
    exit 1
fi

if command -v python3 &> /dev/null; then
    echo -e "${GREEN}$TICK${NO_COLOR} Python found: $(python3 --version)"
else
    echo -e "${YELLOW}WARNING: ${RED}$CROSS${NO_COLOR} Python not found. Installing Python..."
    (sudo apt update && sudo apt install -y python3 python3-pip & spinner $!)
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}$CROSS${NO_COLOR} Python installation failed. Please install it manually."
        exit 1
    fi
fi

echo -e "\nInstalling required Python packages..."
requirements=("flask" "selenium" "webdriver_manager")

for package in "${requirements[@]}"
do
    if python3 -c "import $package" &> /dev/null; then
        echo -e "${GREEN}$TICK${NO_COLOR} $package is already installed"
    else
        echo -e "${YELLOW}Installing $package...${NO_COLOR}"
        (pip3 install $package & spinner $!)
        if ! python3 -c "import $package" &> /dev/null; then
            echo -e "${RED}$CROSS${NO_COLOR} Failed to install $package. Please install it manually."
        else
            echo -e "${GREEN}$TICK${NO_COLOR} $package installed successfully"
        fi
    fi
done

echo -e "\nCreating rickphis command..."
echo -e "#!/bin/bash\npython3 $rickphis_opt_dir/app.py \"\$@\"" | sudo tee /usr/local/bin/rickphis > /dev/null
sudo chmod +x /usr/local/bin/rickphis

echo -e "${GREEN}RickPhis setup completed successfully!${NO_COLOR}"
echo -e "You can now run the tool using the command: ${YELLOW}rickphis${NO_COLOR}"
