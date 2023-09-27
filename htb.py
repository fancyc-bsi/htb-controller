import os
from dotenv import load_dotenv
from hackthebox import HTBClient
from PyInquirer import prompt
from tabulate import tabulate

# Load environment variables from .env file
load_dotenv()

# Initialize HTBClient with your App Token from .env file
client = HTBClient(app_token=os.getenv('HTB_APP_TOKEN'))

def get_machine_choices():
    machines = client.get_machines()
    choices = [{'name': f"{machine.name} - {machine.difficulty}"} for machine in machines]
    # Add an option to return to the main menu
    choices.append({'name': 'Return to main menu'})
    return choices

def start_machine():
    questions = [{'type': 'list', 'name': 'machine', 'message': 'Which machine do you want to start?', 'choices': get_machine_choices()}]
    answers = prompt(questions)
    selected_machine_name = answers['machine'].split(' - ')[0]

    # If user chooses to return to the main menu
    if selected_machine_name == 'Return to main menu':
        return

    selected_machine = next(machine for machine in client.get_machines() if machine.name == selected_machine_name)
    result = client.do_request(endpoint=f'machines/{selected_machine.id}/start', post=True)
    print(f'Started machine: {selected_machine.name}, Result: {result}')

def stop_machine():
    active_machine = client.get_active_machine()
    if active_machine:
        active_machine.stop()
        print(f"Stopped machine: {active_machine.machine.name}")
    else:
        print("No active machine found.")

def submit_flag():
    questions = [
        {'type': 'input','name': 'flag','message': 'Enter the flag:'},
        {'type': 'input','name': 'difficulty','message': 'Rate the difficulty (10 to 100, multiple of 10):'}
    ]
    answers = prompt(questions)
    flag = answers['flag']
    difficulty = int(answers['difficulty'])
    active_machine = client.get_active_machine()
    if active_machine:
        response = active_machine.machine.submit(flag, difficulty)
        print(f"Flag submission response: {response}")
    else:
        print("No active machine found.")

def view_running_machine_ip():
    active_machine = client.get_active_machine()
    if active_machine:
        print(f"Running machine: {active_machine.machine.name}, IP: {active_machine.ip}")
    else:
        print("No active machine found.")

def list_machines():
    machines = client.get_machines()
    table_data = [[machine.name, machine.os, machine.difficulty] for machine in machines]
    headers = ['Name', 'OS', 'Difficulty']
    print(tabulate(table_data, headers, tablefmt='grid'))

def download_vpn():
    vpn_servers = client.get_all_vpn_servers()
    questions = [
        {'type': 'list', 'name': 'server', 'message': 'Which VPN server do you want to download the configuration for?',
         'choices': [{'name': server.friendly_name} for server in vpn_servers]},
        {'type': 'input', 'name': 'path', 'message': 'Enter the path where you want to save the configuration (default: current directory):'},
        {'type': 'confirm', 'name': 'tcp', 'message': 'Do you want to download TCP configuration?', 'default': False}
    ]
    answers = prompt(questions)
    selected_server_name = answers['server']
    selected_server = next(server for server in vpn_servers if server.friendly_name == selected_server_name)
    path = selected_server.download(path=answers['path'], tcp=answers['tcp'])
    print(f"VPN configuration downloaded to: {path}")

def main_menu():
    questions = [
        {
            'type': 'list',
            'name': 'action',
            'message': 'What do you want to do?',
            'choices': [
                'List all machines',
                'Start a machine',
                'Stop the running machine',
                'Submit a flag',
                'View running machine IP',
                'Download VPN Configuration',
                'Exit'
            ]
        }
    ]
    answers = prompt(questions)
    return answers['action']

# Run the script
if __name__ == "__main__":
    while True:
        action = main_menu()
        if action == 'List all machines':
            list_machines()
        elif action == 'Start a machine':
            start_machine()
        elif action == 'Stop the running machine':
            stop_machine()
        elif action == 'Submit a flag':
            submit_flag()
        elif action == 'View running machine IP':
            view_running_machine_ip()
        elif action == 'Download VPN Configuration':
            download_vpn()
        elif action == 'Exit':
            break
