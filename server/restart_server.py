import subprocess

# Define the paths to the start and stop scripts
start_script_path = "./start_server.sh"  # Adjust the path as needed
stop_script_path = "./stop_server.sh"    # Adjust the path as needed

def execute_script(script_path, script_name):
    try:
        subprocess.run([script_path], check=True, shell=True)
        print(f"{script_name} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_name}: {e}")

# Restart the server
execute_script(stop_script_path, "stop_server.sh")
execute_script(start_script_path, "start_server.sh")