# Track-Surf

This repository contains the prototype for the "Track-Surf" game, developed within the Software Engineering Project
Management module to fulfil the requirements set by our clients (Team 2).

## Requirements

During the Unit 6 assignment, our clients, Team 2, had set us a series of 10 total requirements to be implemented in
this project.

As part of the prototype development, we aimed to meet a **minimum of 5** requirements. A full breakdown of the
requirements has been included below:

| Requirement Number | Requirement Name                                                 | Requirement Met? |
|--------------------|------------------------------------------------------------------|------------------|
| 1                  | The device should be controllable by Keyboard/Mouse or Touch.    | Yes              |
| 2                  | The UI should be usable with one hand.                           | Yes              |
| 3                  | The device should be safe for use by children.                   | Yes              |
| 4                  | A player should be able to create a user profile.                | Yes              |
| 5                  | Sounds are to be muted with a single key/button press.           | Yes              |
| 6                  | Additional language(s) should be available.                      | No               |
| 7                  | The game should keep a young child entertained.                  | Yes              |
| 8                  | The game should have limited, controlled access to the internet. | Yes              |
| 9                  | The game should be simple/intuitive to use.                      | Yes              |
| 10                 | Data should be stored in an efficient manner.                    | Partially Met    |

## Screenshots

### Game

![Game Screenshot](https://i.gyazo.com/4459d56fa4bf342bee5f8bbe5a027cfb.png)

### Profile Selection

![Profile Selection Screenshot](https://i.gyazo.com/d511ba81c582f5f4eaefcd476eea42f3.png)

### High Scores

![High Score Screenshot](https://i.gyazo.com/e18761659cde52d10db6574d433d5353.png)

### Car Selection

![Car Selection Screenshot](https://i.gyazo.com/1017b1773cab5805743d6698c3d3cfe3.png)

### Track Selection

![Track Selection Screenshot](https://i.gyazo.com/b2f0f78731c524a3d829ae2b11ce6e3f.png)

## Installation/Setup

This code has been developed and tested using all major releases of Python 3.x. In order to run a copy on your local
machine, please execute the following commands in a terminal session.

### Clone the GitHub Repository

```bash
git clone git@github.com:AlexGeorgeLain/sepm-development.git
cd sepm-development
```

### Enter Virtual Environment

```bash
python -m venv venv
.\venv\Scripts\activate
```

Once you have executed the above commands, the command cursor in your terminal session should be prefixed with the
virtual environment name (venv), similar to the example below.

```bash
(venv) C:\sepm-development>
```

### Install Dependencies

This project requires a series of external packages (Such as PyGame, PyYaml and PeeWee) in order to assist with specific
tasks within the game. In order to install the projects dependencies, we have bundled the requirements into a **requirements.txt** file in the root directory. These can be installed within the venv by executing the below command:

```bash
pip install -r requirements.txt
```

### Launch Game

In order to launch the Track-Surf game, execute the below command within your existing terminal session:

```bash
python app.py
```

## Code Styling

In order to ensure code committed adheres to a common standard, we have chosen to implement the Python PEP8 style guide
using a series of GitHub actions using the Black and iSort modules.

When a Push or Pull Request is raised against the main branch,
the [fix-styling.yml](https://github.com/AlexGeorgeLain/sepm-development/actions/workflows/fix-styling.yml) GitHub
Action is executed. When non-conformant code is detected, this is rectified with an additional push to the repository
ensuring that non-conforming code will never be part of the main repository branch.

## Testing

For static and database-driven methods, a series of automated tests have been developed in order to ensure that broken
code is never committed to the repository. A full breakdown of the tests conducted and their status has been included
below:

### Tests Conducted

A live trace of the test status can be viewed within
the [GitHub actions page](https://github.com/AlexGeorgeLain/sepm-development/actions/workflows/run-python-tests.yml) for
this repository. For completeness, a full breakdown has been included below.

| Test Name                              | Test Description                                                                                                                            | Current Status |
|----------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|----------------|
| test_if_track_files_exist_database     | Tests to confirm all tracks in the database have static images available in the required directories.                                       | Passing        |
| test_if_car_files_exist_database       | Tests to confirm all cars in the database have static images available in the required directories.                                         | Passing        |
| test_if_track_files_exist              | Tests to confirm that /assets/images/tracks/track-* folders contain the required items (For example, track-01.png and track-01-border.png). | Passing        |
| test_if_background_files_exist         | Tests to confirm that the background images exist within the required directories.                                                          | Passing        |
| test_if_car_files_exist                | Tests to confirm that the car images exist within the required directories.                                                                 | Passing        |
| test_if_audio_files_exist              | Tests to confirm that the two required audio files exist within the required directories.                                                   | Passing        |
| test_if_ui_assets_exist                | Tests to confirm that all static UI elements (Including Buttons, Icons etc) exist within the required directories.                          | Passing        |
| test_if_censors_static_input_correctly | Tests that the Censorship functionality correctly obscures swear words.                                                                     | Passing        |
| test_database_seeder_files             | Tests that Database seeder files located in /database/*.yml contain only allowed model values.                                              | Passing        |

### How to run tests

Tests can be run by executing the below command in a terminal session within the Python Virtual Environment:

```bash
python -m unittest -v
```

## Authors

- [Alexander George Lain](https://github.com/AlexGeorgeLain)
- [Antonios Kalaitzakis](https://github.com/kalaitzakisant)
- [Kieron Holmes](https://github.com/KieronHolmes)
- [Kikelomo Obayemi](https://github.com/kikeobayemi)
- [Sergio Rafael Zavarce Caldera](https://github.com/serzav)
- [Suresh Melvin Sigera](https://github.com/sureshmelvinsigera)
- [Victor Javier Martinez Hernandez](https://github.com/apuleyo3)

## Attributions

This project uses a series of open-sourced assets to form the design and audio of the Track-Surf game. Links to the original sources have been included below:

- Game Icons: [KennyNL Game Icons](https://www.kenney.nl/assets/game-icons)
- Game Backgrounds/Vehicles: [KennyNL Racing Pack](https://www.kenney.nl/assets/racing-pack)
