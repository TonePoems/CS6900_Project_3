# CS6900_Project_3
# HCI Project 3: Color Test Data Collection

This is a simple web application built with Python and Flask to run a data collection experiment for an HCI project. The app presents users with a target color name and a palette of 7 colors, recording their choice, accuracy, and response time.

## Overview

The application is designed to test two different color palettes ("old" and "new") to measure if the "new" palette improves speed and accuracy for users, potentially including those with color-vision deficiencies.

The app flow is as follows:
1.  A welcome screen prompts the user for a **Participant ID**.(Type a unique name or ID for the participant (e.g., "P1", "Sean", "P2_Operator","Anthony"))
2.  The user is shown a series of 280 trials (by default).
3.  Each trial displays a "Target Color" (e.g., "Red") and 7 colored squares.
4.  The app records which color the user clicks and how long it took (in milliseconds).
5.  All data is saved to a single `results.csv` file, tagged with the Participant ID.
6.  A "Test Complete" screen is shown at the end.

## File Structure
├── app.py # The main Flask server and all backend logic 
├── results.csv # (Auto-generated) The file where all data is saved 
├── templates/ 
│ ├── welcome.html # The starting page with the participant ID form 
│ ├── index.html # The main test interface (target prompt + 7 colors) 
│ └── done.html # The "Test Complete" page 
└── README.md # This file

## Requirements

The only external library required is **Flask**.

You can install it using pip:

```
pip install flask
```

## How to Run

```
python app.py
```

Open your web browser and go to: http://127.0.0.1:5000

## Customizing Test Length
By default, the test runs 20 repetitions for each color/palette combination (total 280 trials). To run a shorter test (e.g., for testing), you can use the -r flag followed by the number of repetitions.

For example, to run the test with only 2 reps per color (28 total trials):

```
python app.py -r 2
```


## Data Output
All results are saved in a file named results.csv. The columns are:
participant_id: The ID entered on the welcome screen.
trial_index: The trial number (1 to 280).
interface_source: old or new (which palette was shown).
target_color_name: The name of the color the user was asked to find (e.g., "Red").
target_hex: The correct hex value for the target color.
clicked_color_name: The name of the color the user actually clicked.
clicked_hex: The hex value of the color the user actually clicked.
time_taken_ms: The user's response time in milliseconds.
is_correct: True or False.