#!/bin/bash

# Send the 'quit' command to the screen session named 'my_session_name'
echo ""
echo "Stoping server."
screen -S flask_screen -X quit

echo ""
echo "Stoping simulation checker."
screen -S check_screen -X quit
echo ""

echo ""
echo "Stoping simulation."
screen -S simulation_screen -X quit
echo ""