import subprocess
import time

# Function to check if the screen session is running
def is_screen_session_running(session_name):
    try:
        # Run the "screen -ls" command and capture its output
        output = subprocess.check_output(["screen", "-ls"]).decode("utf-8")

        # Check if the session_name is in the output
        return session_name in output
    except subprocess.CalledProcessError:
        # Handle the case where the screen command returns an error
        return False

# Check if the "simulation_screen" session is running every x seconds
check_interval = 2

while True:
    if is_screen_session_running("simulation_screen"):
        print("The 'simulation_screen' session is running.")
    else:
        print("The 'simulation_screen' session is not running.")
    
    # Wait for the specified interval before checking again
    time.sleep(check_interval)
