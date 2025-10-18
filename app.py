import argparse
import random
import csv
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash

#Project Setup
app = Flask(__name__)

app.secret_key = 'your_random_secret_key_here_12345'

# colors from the project
old_colors = {
    "Red": 0xFF0000,
    "Brown": 0x7F6000,
    "Green": 0x9DE951,
    "Orange": 0xFEBC02,
    "Yellow": 0xFFFF00,
    "Blue": 0x002F8E,
    "Purple": 0x7030A0
}

# colors selected by Sean
new_colors = {
    "Red": 0xED1E24,
    "Brown": 0xD4681B,
    "Green": 0x92D050,
    "Orange": 0xFEBC02,
    "Yellow": 0xFFFF00,
    "Blue": 0x00B0F0,
    "Purple": 0x7030A0
}

# modified code for Flask

class colorTest:
    def __init__(self, color, hex_val, source):
        self.color = color      # Target color name, e.g., "Red"
        self.hex = hex_val    # The *correct* hex value for this trial
        self.source = source  # 'old' or 'new' to tell which palette to use

#Global variables to manage the test
test_trials = []
current_trial_index = 0
RESULTS_FILE = 'results.csv'

def setup_trials(reps_per_color=20):
    global test_trials
    test_trials = []
    
    for key, value in old_colors.items():
        for _ in range(reps_per_color):
            test_trials.append(colorTest(key, value, 'old'))

    for key, value in new_colors.items():
        for _ in range(reps_per_color):
            test_trials.append(colorTest(key, value, 'new'))

    random.shuffle(test_trials)

def setup_results_file():
    if not os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                "participant_id", "trial_index", "interface_source", "target_color_name", 
                "target_hex", "clicked_color_name", "clicked_hex", 
                "time_taken_ms", "is_correct"
            ])


# Flask Routes (The Web Page Logic)

@app.route('/', methods=['GET', 'POST'])
def welcome():
    """
    Shows the welcome message.
    If 'POST', it means the user submitted their ID.
    """
    if request.method == 'POST':
        participant_id = request.form['participant_id']
        
        # Store the participant's ID and starting trial index in their session
        session['participant_id'] = participant_id
        session['current_trial_index'] = 0 # Start them at trial 0
        
        flash(f"Starting test for: {participant_id}", "info")
        return redirect(url_for('show_trial'))

    # If 'GET', just show the welcome page
    return render_template('welcome.html')

@app.route('/test')
def show_trial():
    """
    This is the main test page. It shows the current test trial.
    """
    #Check if a participant ID exists. If not, send them back to the welcome page.
    if 'participant_id' not in session:
        flash("Please enter a Participant ID to begin.", "error")
        return redirect(url_for('welcome'))

    # Get the user's current trial index from their session
    current_trial_index = session.get('current_trial_index', 0)
    
    if current_trial_index >= len(test_trials):
        return redirect(url_for('test_done'))

    trial = test_trials[current_trial_index]
    
    if trial.source == 'old':
        palette_to_display = old_colors
    else:
        palette_to_display = new_colors
        
    shuffled_palette_items = list(palette_to_display.items())
    random.shuffle(shuffled_palette_items)
    
    palette_for_html = []
    for name, hex_val in shuffled_palette_items:
        hex_str = f'#{hex_val:06X}'
        palette_for_html.append({'name': name, 'hex': hex_str})

    return render_template(
        'index.html',
        target_color=trial.color,
        palette=palette_for_html,
        trial_num=current_trial_index + 1,
        total_trials=len(test_trials)
    )

@app.route('/record', methods=['POST'])
def record_result():
    """
    Records the data from the user's click and redirects
    back to '/test' for the next trial.
    """
    #Check for participant ID again, just in case.
    if 'participant_id' not in session:
        flash("Session expired. Please enter your ID again.", "error")
        return redirect(url_for('welcome'))

    # Get data from the session
    participant_id = session['participant_id']
    current_trial_index = session['current_trial_index']
    
    # Get data from the form
    time_taken = request.form['time_taken_ms']
    clicked_hex = request.form['clicked_hex']
    clicked_name = request.form['clicked_name']
    
    trial = test_trials[current_trial_index]
    
    clicked_hex_num = int(clicked_hex.lstrip('#'), 16)
    is_correct = (clicked_hex_num == trial.hex)
    
    target_hex_str = f'#{trial.hex:06X}'
    
    with open(RESULTS_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        # Write the participant_id to the CSV
        writer.writerow([
            participant_id,
            current_trial_index + 1,
            trial.source,
            trial.color,
            target_hex_str,
            clicked_name,
            clicked_hex,
            time_taken,
            is_correct
        ])
    
    # Increment the trial index *in the session*
    session['current_trial_index'] += 1
    
    return redirect(url_for('show_trial'))

@app.route('/done')
def test_done():
    # Clear the session so the next person can start fresh
    participant = session.pop('participant_id', 'Participant')
    session.pop('current_trial_index', None)
    
    return render_template('done.html', participant_name=participant)

# Main execution
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--reps", nargs='?', default=20,
                        help="number of reps per color option. Default 20")
    args = parser.parse_args()
    
    setup_trials(reps_per_color=int(args.reps))
    setup_results_file()
    
    print(f"--- Starting test with {len(test_trials)} total trials ---")
    print(f"--- Results will be saved to {RESULTS_FILE} ---")
    print("--- Open http://127.0.0.1:5000 in your browser to begin ---")
    
    app.run(debug=True, port=5000)