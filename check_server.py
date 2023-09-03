import subprocess
import time
from pushbullet import Pushbullet

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

# Replace with your Pushbullet API key - this file won't be updated further
pushbullet_api_key = "your_pushbullet_api_key"

# Interval in seconds to check if the session is running
check_interval = 60  # Change this to your desired interval

while True:
    if is_screen_session_running("simulation_screen"):
        print("The 'simulation_screen' session is running.")
    else:
        print("The 'simulation_screen' session is not running. Sending Pushbullet notification...")
        send_pushbullet_notification(pushbullet_api_key, "Session Not Running", "The 'simulation_screen' session is not running.")
    
    # Wait for the specified interval before checking again
    time.sleep(check_interval)