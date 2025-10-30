import argparse
from ast import Mult
import random
import csv
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import numpy as np

#Project Setup
app = Flask(__name__)
app.secret_key = '3d5016a1150aeccc3838'

# ORIGINAL PALETTE (From PDF) 
original_colors = {
    "Red": 0xFF0000,
    "Brown": 0x7F6000,
    "Green": 0x9DE951,
    "Orange": 0xFEBC02,
    "Yellow": 0xFFFF00,
    "Blue": 0x002F8E,
    "Purple": 0x7030A0
}

# ROUND 1 PALETTE (From last week's test)
round1_colors = {
    "Red": 0xED1E24,     
    "Brown": 0xD4681B,   
    "Green": 0x92D050,   
    "Orange": 0xFEBC02,  
    "Yellow": 0xFFFF00,  
    "Blue": 0x00B0F0,    
    "Purple": 0x7030A0   
}

# ROUND 2 PALETTE 
round2_colors = {
    "Red": 0xE04747,
    "Brown": 0x5A3507,
    "Green": 0x04F994,
    "Orange": 0xFEBC02,
    "Yellow": 0xFFFF00,
    "Blue": 0x82EEFD,
    "Purple": 0x7030A0
}

#  colorTest Class 
class colorTest:
    def __init__(self, color, hex_val, source):
        self.color = color      
        self.hex = hex_val    
        # source will be 'original', 'round1', or 'round2'
        self.source = source  

# --- Global variables ---
test_trials = []
# This will be your final data file
RESULTS_FILE = 'final_results.csv' 

# Updated setup_trials function
def setup_trials(base_reps=4):
    global test_trials
    test_trials = []
    
    #  60% / 10% / 30% ratio
    reps_r2 = base_reps * 6    # 60% (e.g., 24 reps)
    reps_r1 = base_reps * 1    # 10% (e.g., 4 reps)
    reps_orig = base_reps * 3  # 30% (e.g., 12 reps)
    
    # Add trials for the 'original' palette
    for key, value in original_colors.items():
        for _ in range(reps_orig):
            test_trials.append(colorTest(key, value, 'original'))

    # Add trials for the 'round1' palette
    for key, value in round1_colors.items():
        for _ in range(reps_r1):
            test_trials.append(colorTest(key, value, 'round1'))
            
    # Add trials for the 'round2' palette
    for key, value in round2_colors.items():
        for _ in range(reps_r2):
            test_trials.append(colorTest(key, value, 'round2'))

    # Shuffle the master list to randomize the test order
    random.shuffle(test_trials)
    print(f"--- Trials set up with {reps_orig} original, {reps_r1} round1, {reps_r2} round2 reps per color ---")

def setup_results_file():
    # This checks for the final (Round 2) results file
    if not os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                "participant_id", "trial_index", "interface_source", "target_color_name", 
                "target_hex", "clicked_color_name", "clicked_hex", 
                "time_taken_ms", "is_correct"
            ])

# --- Flask Routes ---

@app.route('/', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        participant_id = request.form['participant_id']
        
        session['participant_id'] = participant_id
        session['current_trial_index'] = 0 
        session['session_results'] = [] 
        
        flash(f"Starting test for: {participant_id}", "info")
        return redirect(url_for('show_trial'))

    return render_template('welcome.html')

@app.route('/test')
def show_trial():
    if 'participant_id' not in session:
        flash("Please enter a Participant ID to begin.", "error")
        return redirect(url_for('welcome'))

    current_trial_index = session.get('current_trial_index', 0)
    
    if current_trial_index >= len(test_trials):
        return redirect(url_for('test_done'))

    trial = test_trials[current_trial_index]
    
    # --- NEW: Logic to pick one of the 3 palettes ---
    if trial.source == 'original':
        palette_to_display = original_colors
    elif trial.source == 'round1':
        palette_to_display = round1_colors
    else: # trial.source == 'round2'
        palette_to_display = round2_colors
        
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
    if 'participant_id' not in session:
        flash("Session expired. Please enter your ID again.", "error")
        return redirect(url_for('welcome'))

    participant_id = session['participant_id']
    current_trial_index = session['current_trial_index']
    
    time_taken = float(request.form['time_taken_ms']) 
    clicked_hex = request.form['clicked_hex']
    clicked_name = request.form['clicked_name']
    
    trial = test_trials[current_trial_index]
    
    clicked_hex_num = int(clicked_hex.lstrip('#'), 16)
    is_correct = (clicked_hex_num == trial.hex)
    
    target_hex_str = f'#{trial.hex:06X}'
    
    # Add this trial's results to the session list
    session['session_results'].append({
        'is_correct': is_correct,
        'time_taken_ms': time_taken
    })
    session.modified = True 
    
    # Save to CSV file
    with open(RESULTS_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            participant_id,
            current_trial_index + 1,
            trial.source, # This now saves 'original', 'round1', or 'round2'
            trial.color,
            target_hex_str,
            clicked_name,
            clicked_hex, 
            time_taken,
            is_correct
        ])
    
    session['current_trial_index'] += 1
    
    return redirect(url_for('show_trial'))

@app.route('/done')
def test_done():
    # Calculate stats before clearing session
    session_results = session.get('session_results', [])
    
    total_trials = len(session_results)
    
    if total_trials > 0:
        total_correct = sum(1 for trial in session_results if trial['is_correct'])
        accuracy = (total_correct / total_trials) * 100
        
        correct_times = [trial['time_taken_ms'] for trial in session_results if trial['is_correct']]
        if correct_times:
            avg_time = np.mean(correct_times)
        else:
            avg_time = 0.0
    else:
        total_correct = 0
        accuracy = 0.0
        avg_time = 0.0
    
    # Now clear the session
    participant = session.pop('participant_id', 'Participant')
    session.pop('current_trial_index', None)
    session.pop('session_results', None)
    
    return render_template(
        'done.html', 
        participant_name=participant,
        total_trials=total_trials,
        total_correct=total_correct,
        accuracy=accuracy,
        avg_time=avg_time
    )

# --- Main execution ---
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r", "--reps", 
        nargs='?', 
        default=4,  # This is the 'base_reps'
        help="Base number of reps. (Default 4) 6:1:3 ratio for R2:R1:Original."
    )
    args = parser.parse_args()
    
    setup_trials(base_reps=int(args.reps))
    setup_results_file() # This sets up final_results.csv
    
    print(f"--- Starting test with {len(test_trials)} total trials ---")
    print("---Multi-palette test (60% R2, 10% R1, 30% Original)---")
    print(f"--- Results will be saved to {RESULTS_FILE} ---")
    print("--- Open http://127.0.0.1:5000 in your browser to begin ---")
    
    app.run(debug=True, port=5000)