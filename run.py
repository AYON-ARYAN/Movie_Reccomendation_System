import subprocess

# Paths
venv_path = "/Volumes/BLACK_SHARK/Moodix/Movie_Reccomendation_System/.venv/bin/activate"
script1 = "/Volumes/BLACK_SHARK/Moodix/Movie_Reccomendation_System/app.py"
script2 = "/Volumes/BLACK_SHARK/Moodix/Movie_Reccomendation_System/Movie_recommender_ML-main/app.py"

# Format the command string for AppleScript safely
def run_in_new_terminal(command):
    # Escape double quotes and backslashes for AppleScript
    escaped_cmd = command.replace('"', '\\"')
    apple_script = f'''
    tell application "Terminal"
        do script "{escaped_cmd}"
        activate
    end tell
    '''
    subprocess.run(["osascript", "-e", apple_script])

# First Terminal - run Python script
cmd1 = f'source "{venv_path}" && python "{script1}"'
run_in_new_terminal(cmd1)

# Second Terminal - run Streamlit app
cmd2 = f'source "{venv_path}" && streamlit run "{script2}"'
run_in_new_terminal(cmd2)
