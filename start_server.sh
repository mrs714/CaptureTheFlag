#!/bin/bash
echo ""
echo "Looking for updates on the code..."
git pull

echo ""
echo "Launching server."
# Start Flask in a detached screen session
screen -dmS flask_screen bash -c 'flask run --host=0.0.0.0 --port=80'

echo ""
echo "Launching simulation."
# Run the simulation_launch.py script
screen -dmS simulation_screen bash -c 'python3 simulation_launch.py'
echo ""
