#!/bin/bash

echo ""
echo "Looking for updates on the code..."
git pull

echo ""
echo "Launching server."
# Start Flask in a detached screen session
screen -dmS flask_screen bash -c 'flask run --host=0.0.0.0 --port=80'

# Check if any command-line arguments are provided
if [[ $# -gt 0 ]]; then
    # Parse command-line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --map-width)
                MAP_WIDTH="$2"
                shift 2
                ;;
            --map-height)
                MAP_HEIGHT="$2"
                shift 2
                ;;
            --duration)
                DURATION="$2"
                shift 2
                ;;
            *)
                echo "Unknown option: $1"
                exit 1
                ;;
        esac
    done

    echo ""
    echo "Launching simulation."
    # Call the Python script with the provided arguments
    screen -dmS flask_screen bash -c 'python simulation.py --map-width "$MAP_WIDTH" --map-height "$MAP_HEIGHT" --duration "$DURATION"'
    echo ""
fi

echo ""
echo "Launching simulation."
# Run the simulation_launch.py script
screen -dmS simulation_screen bash -c 'python3 simulation_launch.py > server/simulation.log 2>&1'
echo ""
echo "Launching simulation checker."
# Run the check_server.py script
screen -dmS check_screen bash -c 'python3 server/check_server.py'
echo ""

