import pandas as pd
from scipy import stats  

df1 = pd.read_csv('results_round_1.csv')
df2 = pd.read_csv('results_round_2.csv')


# T_tests
original = df1[df1['interface_source']=='original']
round1 = df1[df1['interface_source']=='round1']
round2 = df2[df2['interface_source']=='round2']

print(f'means:\to: {original['is_correct'].mean():.3f}\tr1: {round1['is_correct'].mean():.3f}\tr2: {round2['is_correct'].mean():.3f}')

print(stats.ttest_ind(original['is_correct'], round1['is_correct']))
print(stats.ttest_ind(original['is_correct'], round2['is_correct']))

#print(df.to_string()) 

# for source in df['interface_source'].unique():
#     print(source)
#     for participant in df['participant_id'].unique():
#         relevant_df = df[(df['interface_source'] == source) & (df['participant_id'] == participant)]
#         #print(relevant_df.to_string())
#         print(f'\t{participant}\t\tSamples: {len(relevant_df)}\tAccuracy: {relevant_df['is_correct'].mean():.3f} +/- {relevant_df['is_correct'].std():.3f}\tTime: {relevant_df['time_taken_ms'].mean()*0.001:.2f} +/- {relevant_df['time_taken_ms'].std()*0.001:.2f}')


# for participant in df['participant_id'].unique():
#     print(participant)
#     for color in df['target_color_name'].unique():
#         relevant_df = df[(df['target_color_name'] == color) & (df['participant_id'] == participant)]
#         samples = len(relevant_df)
#         # Original Accuracy 
#         o_acc_mean = relevant_df[relevant_df['interface_source'] == 'round1']['is_correct'].mean()
#         o_acc_std = relevant_df[relevant_df['interface_source'] == 'round1']['is_correct'].std()
#         # Original Time
#         o_time_mean = relevant_df[relevant_df['interface_source'] == 'round1']['time_taken_ms'].mean()*0.001
#         o_time_std = relevant_df[relevant_df['interface_source'] == 'round1']['time_taken_ms'].std()*0.001

#         # round1 Accuracy 
#         r1_acc_mean = relevant_df[relevant_df['interface_source'] == 'round2']['is_correct'].mean()
#         r1_acc_std = relevant_df[relevant_df['interface_source'] == 'round2']['is_correct'].std()
#         # round1 Time
#         r1_time_mean = relevant_df[relevant_df['interface_source'] == 'round2']['time_taken_ms'].mean()*0.001
#         r1_time_std = relevant_df[relevant_df['interface_source'] == 'round2']['time_taken_ms'].std()*0.001

#         #print(relevant_df.to_string())
#         print(f'\t{color}\t{samples}\t{o_acc_mean:.3f} +/- {o_acc_std:.3f}\t\t{o_time_mean:.2f} +/- {o_time_std:.2f}\t\t{r1_acc_mean:.3f} +/- {r1_acc_std:.3f}\t\t{r1_time_mean:.3f} +/- {r1_time_std:.3f}')




