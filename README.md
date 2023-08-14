# CompetitionBotUploader

The aim of this project is to create both a python-based server and game.

The server, based on flask, can provide users different capabilities including login, and code and options saving for an arena-type competitive game, which will be periodically and asynchronously run, after which the needed data for improvement will be released.

As for the game, the intention is to create a game-frame from scratch using pygame, upon which we can add all the functionalities needed for the base game, and whatever updates we think of in the future.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

In the following sections you will find out about the features of our project, what you need to set everything up, and how to use everything. 
You can use the project as a baseline for a similar project, take pieces of it for certain purposes (be it the front or back-end) or just setup a server like ours.

## Features

Features of the web-page and server:
- Server: The server is based on flask, and uses a database to store the information.
- Information transfer: The server has multiple functions to fetch and send information to and from both the client and the database.
- Code editor and bot configuration: There's a dedicated page which uses Code Mirror to format and highlight the code, and allows the user to save it to the server, and one that allows the user to configure the bot's options with sliders, always amounting to a set value between the three sliders.
- Responsive design: The web-page, implemented with bootstrap, is designed to be responsive and dynamic and work on both desktop and mobile devices.
- Login system: The server has a login system, which allows users to create accounts, and log in and out of them, with all the needed information saved on the database. This also allows for a robust server system, which can be used to store information about the user, and allow for multiple users to use the server at the same time.

Features of the game:
- Asyncronous execution: The game is run asynchronously, with a set time between each run, displaying the important information (such as position or error logs) to each user.
- Log system: The game has a log system, created from the ground-up, which allows for highly customizable logs of the game to be created, to use as a debugging tool or to get information about the game.
- Game-frame: The game is also created from scratch, using pygame, and is highly customizable, allowing for the addition of new features and functionalities.
- Video recording: The server records the game, and saves it as a video file, which is displayed to the users on the web-page, and can be downloaded by them.
- Safe outside-code execution: The game uses RestrictedPython to execute the code, which allows for the safe execution of code, without the risk of the user's code damaging the server or the game, only giving the user access to the needed functions and variables. Previously to that, the code is only compiled to check for syntax errors, and the user is notified of any errors in the code.

## Getting Started

The following sections list what you need to get a local copy up and running.

### Prerequisites

Software:
    Python dependencies:
    - flask
    - pygame 
    - numpy
    - moviepy
    - restrictedpython

    Database:
    - sqlite3 or similar, if you need to access the database directly

Hardware:
    You can use a computer as a server, any other service that allows you to run python code, or a raspberry pi, which is what we used.

### Installation

- Clone the repository
- Install the dependencies on the previous section on the server you intend to use

## Usage

- Setup the server (more on that in the future)
- Setup the port forwarding on your router, if you want to access the server from outside your network

## Contributing

This is intended to be a personal project. As such, we don't expect any contributions, but feel free to fork the project and use it as a baseline for your own project.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

You are free to use, modify, and distribute this software for any purpose. No warranty is provided, and the software is used at your own risk.

## Contact

Provided in the future.