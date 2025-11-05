import pandas as pd

df = pd.read_csv('results_round_1.csv')

#print(df.to_string()) 

for source in df['interface_source'].unique():
    print(source)
    for participant in df['participant_id'].unique():
        relevant_df = df[(df['interface_source'] == source) & (df['participant_id'] == participant)]
        #print(relevant_df.to_string())
        print(f'\t{participant}\t\tSamples: {len(relevant_df)}\tAccuracy: {relevant_df['is_correct'].mean():.3f} +/- {relevant_df['is_correct'].std():.3f}\tTime: {relevant_df['time_taken_ms'].mean()*0.001:.2f} +/- {relevant_df['time_taken_ms'].std()*0.001:.2f}')


for participant in df['participant_id'].unique():
    print(participant)
    for color in df['target_color_name'].unique():
        relevant_df = df[(df['target_color_name'] == color) & (df['participant_id'] == participant)]
        samples = len(relevant_df)
        # Original Accuracy 
        o_acc_mean = relevant_df[relevant_df['interface_source'] == 'original']['is_correct'].mean()
        o_acc_std = relevant_df[relevant_df['interface_source'] == 'original']['is_correct'].std()
        # Original Time
        o_time_mean = relevant_df[relevant_df['interface_source'] == 'original']['time_taken_ms'].mean()*0.001
        o_time_std = relevant_df[relevant_df['interface_source'] == 'original']['time_taken_ms'].std()*0.001

        # round1 Accuracy 
        r1_acc_mean = relevant_df[relevant_df['interface_source'] == 'round1']['is_correct'].mean()
        r1_acc_std = relevant_df[relevant_df['interface_source'] == 'round1']['is_correct'].std()
        # round1 Time
        r1_time_mean = relevant_df[relevant_df['interface_source'] == 'round1']['time_taken_ms'].mean()*0.001
        r1_time_std = relevant_df[relevant_df['interface_source'] == 'round1']['time_taken_ms'].std()*0.001

        #print(relevant_df.to_string())
        print(f'\t{color}\t{samples}\t{o_acc_mean:.3f} +/- {o_acc_std:.3f}\t\t{o_time_mean:.2f} +/- {o_time_std:.2f}\t\t{r1_acc_mean:.3f} +/- {r1_acc_std:.3f}\t\t{r1_time_mean:.3f} +/- {r1_time_std:.3f}')




