#!/bin/bash

# Send the 'quit' command to the screen session named 'my_session_name'
screen -S flask_screen -X quit

screen -S simulation_screen -X quit
