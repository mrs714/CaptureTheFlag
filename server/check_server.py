import subprocess
import time
from pushbullet import Pushbullet


# Replace with your Pushbullet API key
pushbullet_api_key = "your_pushbullet_api_key"

# Interval in seconds to check if the session is running
check_interval = 60  # Change this to your desired interval
log_path = "simulation.log" # Change this to the path of your log file
lines_to_read = 50 # Change this to the number of lines you want to read from the log file (last x lines)
restart_server_on_crash = True # Change this to False if you don't want the server to restart automatically
restart_script_path = "restart_server.py" # Change this to the path of your restart script

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

# Function to send a Pushbullet notification
def send_pushbullet_notification(api_key, title, message):
    pb = Pushbullet(api_key)
    push = pb.push_note(title, message)
    print("Pushbullet notification sent successfully.")

while True:
    if is_screen_session_running("simulation_screen"):
        print("The 'simulation_screen' session is running.")
        # Delete the log file
        open(log_path, 'w').close()

    else:
        print("The 'simulation_screen' session is not running. Sending Pushbullet notification...")
        # Get the log file contents
        with open(log_path, "r") as f:
            log_contents = f.readlines()[-lines_to_read:] # Get the last 50 lines of the log file
        # Send a Pushbullet notification with the log file contents
        send_pushbullet_notification(pushbullet_api_key, "Session Not Running", "The 'simulation_screen' session is not running." + "\n\nLog:\n\n" + str(log_contents))

        if restart_server_on_crash:
            try:
                subprocess.run(["python3", restart_script_path], check=True)
                print(f"{restart_script_path} executed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Error executing {restart_script_path}: {e}")
    
    # Wait for the specified interval before checking again
    time.sleep(check_interval)