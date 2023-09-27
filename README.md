
# Hack The Box Controller

This script provides an interactive interface to automate various tasks on the Hack The Box platform using the HTB API. The script can list all available machines, start and stop machines, submit flags, view the IP of a running machine, and download VPN configurations.

## Features
- List all available machines with their name, OS, and difficulty level in a tabulated form.
- Start a machine from the available machine list.
- Stop a running machine.
- Submit flags and rate the difficulty of a machine.
- View the IP of a running machine.
- Download VPN configurations for the selected server.
- User-friendly interactive interface using PyInquirer.

## Installation
1. Clone this repository or download the script to your local machine.
   ```sh
   git clone https://github.com/fancyc-bsi/htb-controller
   ```
2. Navigate to the project directory.
   ```sh
   cd htb-controller
   ```
3. Install the required Python packages.
   ```sh
   pip install -r requirements.txt
   ```
   **Note:** It’s recommended to use a virtual environment to avoid conflicts with other Python packages.

## Usage
1. Create a `.env` file in the project directory and add your Hack The Box App Token.
   ```env
   HTB_APP_TOKEN=your-app-token
   ```
1. Run the script.
   ```sh
   python htb.py
   ```
2. Follow the interactive prompts to perform the desired actions.
