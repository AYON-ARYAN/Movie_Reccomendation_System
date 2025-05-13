"""
This module runs two Python scripts in separate terminals on macOS using AppleScript and subprocess.
"""

import subprocess

# Constants
VENV_PATH = "/Volumes/BLACK_SHARK/Moodix/Movie_Reccomendation_System/.venv/bin/activate"
SCRIPT1 = "/Volumes/BLACK_SHARK/Moodix/Movie_Reccomendation_System/app.py"
SCRIPT2 = "/Volumes/BLACK_SHARK/Moodix/Movie_Reccomendation_System/Movie_recommender_ML-main/app.py"

# Format the command string for AppleScript safely
def run_in_new_terminal(command):
    """
    This function runs a command in a new Terminal window using AppleScript.

    Args:
    command (str): The command to be executed in the Terminal.
    """
    # Escape double quotes and backslashes for AppleScript
    escaped_cmd = command.replace('"', '\\"')
    apple_script = f'''
    tell application "Terminal"
        do script "{escaped_cmd}"
        activate
    end tell
    '''
    subprocess.run(["osascript", "-e", apple_script], check=True)

# First Terminal - run Python script
cmd1 = f'source "{VENV_PATH}" && python "{SCRIPT1}"'
run_in_new_terminal(cmd1)

# Second Terminal - run Streamlit app
cmd2 = f'source "{VENV_PATH}" && streamlit run "{SCRIPT2}"'
run_in_new_terminal(cmd2)
