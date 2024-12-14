# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 22:06:14 2024

@author: 91960
"""
#%%
import numpy as np
import pandas as pd
exercise = 35

select_internal_external = 'e'

borg_scale_eval = np.load('C:/Users/91960/Dissertation/borg_scale.npy', allow_pickle=True).item()

data_repetitions_35e_updated = np.load(f'C:/Users/91960/Dissertation/{exercise}{select_internal_external}_repetitions_updated.npy', allow_pickle=True).item()

data_features_35e_updated = np.load(f'C:/Users/91960/Dissertation/{exercise}{select_internal_external}_features_updated.npy', allow_pickle=True).item()

#print(type(data_features_35))
#print(data_features_35.keys())
#print(type(data_features_35e['subject_1']['emg_data']['emg_deltoideus_anterior'][0][0]))
#flattened=data_features_35e['subject_1']['emg_data']['emg_deltoideus_anterior'][0][0].to_numpy().flatten().tolist()

select_internal_external = 'i'

data_repetitions_35i_updated = np.load(f'C:/Users/91960/Dissertation/{exercise}{select_internal_external}_repetitions_updated.npy', allow_pickle=True).item()

data_features_35i_updated = np.load(f'C:/Users/91960/Dissertation/{exercise}{select_internal_external}_features_updated.npy', allow_pickle=True).item()

#%% Interpolating 35e
import numpy as np
from scipy.interpolate import interp1d

borg_scale_subject_wise_list=[]
for index in borg_scale_eval['35e'].index:
    borg_scale_list=[]
    time_var=0
    for col in borg_scale_eval['35e'].keys():
        #print(borg_scale_eval['35e'].iloc[index][col])
        #print(col)
        if not np.isnan(borg_scale_eval['35e'].iloc[index][col]):
            borg_scale_list.append(borg_scale_eval['35e'].iloc[index][col])
            time_var+=1
            
    #print(list(range(0, time_var+1, 10)),borg_scale_list)
    borg_scale_list.insert(0,6.0)
    borg_scale_subject_wise_list.append((time_var,borg_scale_list))
print(borg_scale_subject_wise_list)
#%% Interpolating 35e
import scipy.interpolate as sc

import matplotlib as mt
def f_from_data(xs,ys):
    print(xs)
    print(ys)
    if len(xs)==len(ys):
        print(xs)
        print(ys)
        mt.pyplot.clf()
        mt.pyplot.scatter(xs, ys, color='red', label='Original Data')
        return sc.interp1d(xs, ys)
    else:
        print("Error")



import math

cnt=0
error_msgs=[]
new_data = []
for subject in data_repetitions_35e_updated.keys():
    print(subject)
    time_sum=0
    subject_wise_borg_list=[]
    x_list=list(range(0, (borg_scale_subject_wise_list[cnt][0]+1) *10, 10))
    y_list=borg_scale_subject_wise_list[cnt][1]
    #print(x_list,y_list)
    f=f_from_data(x_list, y_list)
    for sensor in data_repetitions_35e_updated[subject].keys():
        #print(sensor)
        if sensor=='emg_data':
            for muscle in data_repetitions_35e_updated[subject][sensor].keys():
                #print(muscle)
                if muscle=='emg_pectoralis_major':
                    for index in range(len(data_repetitions_35e_updated[subject][sensor][muscle])):
                        #print(len(data_repetitions_35e_updated[subject][sensor][muscle][index]))
                        try:
                            time_sum+=len(data_repetitions_35e_updated[subject][sensor][muscle][index])/1000
                            print(time_sum,float(f(time_sum)))                          
                            subject_wise_borg_list.append(float(f(time_sum)))
                        except ValueError as e:
                            error_msgs.append((subject,e))
    #print(subject_wise_borg_list)
    #subject_wise_borg_list[0]=6
    subject_wise_borg_list.insert(0,6)
    subject_wise_borg_list[-1]=20
    new_data.append(subject_wise_borg_list)
    cnt+=1
new_borg_scale_35e=pd.DataFrame(new_data)


#%%
final_df=[]
#Update Dataframe with borg scale data for data_repetitions_35e_updated
subject_no=0
for subject in data_features_35e_updated.keys():

    for sensor in data_features_35e_updated[subject].keys():
        #print("Sensor",sensor)
        #sensor='emg_data'
        if sensor=='emg_data':
            for muscle in data_features_35e_updated[subject][sensor].keys():
                for ind in range(1,len(data_features_35e_updated[subject][sensor][muscle])+1):
                    print(f'{subject} {sensor} {muscle} {ind} {new_borg_scale_35e.iloc[subject_no,ind]} {subject_no}')
                    
                    ##### Updating borg_scale_interpolated_35e with new_borg_scale_35e
                    # data_features_35e_updated[subject][sensor][muscle][ind-1][0]["borg_scale"]=borg_scale_interpolated_35e.iloc[subject_no,ind]
                    data_features_35e_updated[subject][sensor][muscle][ind-1][0]["borg_scale"]=new_borg_scale_35e.iloc[subject_no,ind]
                    
                    
                    #new_df[subject][muscle]=
                    #print(ind,len(data_features_35e_updated[subject][sensor][muscle])+1)
                    # if (ind==len(data_features_35e_updated[subject][sensor][muscle])):
                    #     if borg_scale_interpolated_35e.iloc[subject_no,ind]!=20:
                    #         print(subject)
        elif sensor=='imu_data':
            for part in data_features_35e_updated[subject][sensor].keys():
                
                for part_sensor in data_features_35e_updated[subject][sensor][part].keys():
                    
                    if len(data_features_35e_updated[subject][sensor][part][part_sensor])>0:
                        
                        for ind in range(1,len(data_features_35e_updated[subject][sensor][part][part_sensor])+1):
                            #print(f'{subject} {sensor} {part} {part_sensor} {ind} {borg_scale_interpolated_35e.iloc[subject_no,ind]}')
                            #print(type(data_features_35e_updated[subject][sensor][part][part_sensor][ind][0]))
                            print(f'{subject} {sensor} {muscle} {ind} {new_borg_scale_35e.iloc[subject_no,ind]} {subject_no}')
                            ##### Updating borg_scale_interpolated_35e with new_borg_scale_35e
                            data_features_35e_updated[subject][sensor][part][part_sensor][ind-1][0]["borg_scale"]=new_borg_scale_35e.iloc[subject_no,ind]
                            data_features_35e_updated[subject][sensor][part][part_sensor][ind-1][1]["borg_scale"]=new_borg_scale_35e.iloc[subject_no,ind]
                            data_features_35e_updated[subject][sensor][part][part_sensor][ind-1][2]["borg_scale"]=new_borg_scale_35e.iloc[subject_no,ind]
    subject_no+=1


#%%  Final df for emg
subject_no=0
columns_list=['subject','repetition', 'emg_pectoralis_major_0_Fundamental frequency', 'emg_pectoralis_major_0_Human range energy', 'emg_pectoralis_major_0_Max power spectrum', 'emg_pectoralis_major_0_Maximum frequency', 'emg_pectoralis_major_0_Median frequency', 'emg_pectoralis_major_0_Power bandwidth', 'emg_pectoralis_major_0_Spectral centroid', 'emg_pectoralis_major_0_Spectral decrease', 'emg_pectoralis_major_0_Spectral distance', 'emg_pectoralis_major_0_Spectral entropy', 'emg_pectoralis_major_0_Spectral kurtosis', 'emg_pectoralis_major_0_Spectral positive turning points', 'emg_pectoralis_major_0_Spectral roll-off', 'emg_pectoralis_major_0_Spectral roll-on', 'emg_pectoralis_major_0_Spectral skewness', 'emg_pectoralis_major_0_Spectral slope', 'emg_pectoralis_major_0_Spectral spread', 'emg_pectoralis_major_0_Spectral variation', 'emg_pectoralis_major_0_Wavelet absolute mean_0', 'emg_pectoralis_major_0_Wavelet absolute mean_1', 'emg_pectoralis_major_0_Wavelet absolute mean_2', 'emg_pectoralis_major_0_Wavelet energy_0', 'emg_pectoralis_major_0_Wavelet energy_1', 'emg_pectoralis_major_0_Wavelet energy_2', 'emg_pectoralis_major_0_Wavelet entropy', 'emg_pectoralis_major_0_Wavelet standard deviation_0', 'emg_pectoralis_major_0_Wavelet standard deviation_1', 'emg_pectoralis_major_0_Wavelet standard deviation_2', 'emg_pectoralis_major_0_Wavelet variance_0', 'emg_pectoralis_major_0_Wavelet variance_1', 'emg_pectoralis_major_0_Wavelet variance_2', 'emg_pectoralis_major_0_Absolute energy', 'emg_pectoralis_major_0_Average power', 'emg_pectoralis_major_0_ECDF Percentile_0', 'emg_pectoralis_major_0_ECDF Percentile_1', 'emg_pectoralis_major_0_ECDF Percentile Count_0', 'emg_pectoralis_major_0_ECDF Percentile Count_1', 'emg_pectoralis_major_0_Entropy', 'emg_pectoralis_major_0_Histogram_0', 'emg_pectoralis_major_0_Histogram_1', 'emg_pectoralis_major_0_Histogram_2', 'emg_pectoralis_major_0_Histogram_3', 'emg_pectoralis_major_0_Histogram_4', 'emg_pectoralis_major_0_Histogram_5', 'emg_pectoralis_major_0_Histogram_6', 'emg_pectoralis_major_0_Histogram_7', 'emg_pectoralis_major_0_Histogram_8', 'emg_pectoralis_major_0_Histogram_9', 'emg_pectoralis_major_0_Interquartile range', 'emg_pectoralis_major_0_Kurtosis', 'emg_pectoralis_major_0_Max', 'emg_pectoralis_major_0_Mean', 'emg_pectoralis_major_0_Mean absolute deviation', 'emg_pectoralis_major_0_Median', 'emg_pectoralis_major_0_Median absolute deviation', 'emg_pectoralis_major_0_Min', 'emg_pectoralis_major_0_Peak to peak distance', 'emg_pectoralis_major_0_Root mean square', 'emg_pectoralis_major_0_Skewness', 'emg_pectoralis_major_0_Standard deviation', 'emg_pectoralis_major_0_Variance', 'emg_pectoralis_major_0_Area under the curve', 'emg_pectoralis_major_0_Autocorrelation', 'emg_pectoralis_major_0_Centroid', 'emg_pectoralis_major_0_Mean absolute diff', 'emg_pectoralis_major_0_Mean diff', 'emg_pectoralis_major_0_Median absolute diff', 'emg_pectoralis_major_0_Median diff', 'emg_pectoralis_major_0_Negative turning points', 'emg_pectoralis_major_0_Neighbourhood peaks', 'emg_pectoralis_major_0_Positive turning points', 'emg_pectoralis_major_0_Signal distance', 'emg_pectoralis_major_0_Slope', 'emg_pectoralis_major_0_Sum absolute diff', 'emg_pectoralis_major_0_Zero crossing rate', 'emg_pectoralis_major_borg_scale', 'emg_deltoideus_anterior_0_Fundamental frequency', 'emg_deltoideus_anterior_0_Human range energy', 'emg_deltoideus_anterior_0_Max power spectrum', 'emg_deltoideus_anterior_0_Maximum frequency', 'emg_deltoideus_anterior_0_Median frequency', 'emg_deltoideus_anterior_0_Power bandwidth', 'emg_deltoideus_anterior_0_Spectral centroid', 'emg_deltoideus_anterior_0_Spectral decrease', 'emg_deltoideus_anterior_0_Spectral distance', 'emg_deltoideus_anterior_0_Spectral entropy', 'emg_deltoideus_anterior_0_Spectral kurtosis', 'emg_deltoideus_anterior_0_Spectral positive turning points', 'emg_deltoideus_anterior_0_Spectral roll-off', 'emg_deltoideus_anterior_0_Spectral roll-on', 'emg_deltoideus_anterior_0_Spectral skewness', 'emg_deltoideus_anterior_0_Spectral slope', 'emg_deltoideus_anterior_0_Spectral spread', 'emg_deltoideus_anterior_0_Spectral variation', 'emg_deltoideus_anterior_0_Wavelet absolute mean_0', 'emg_deltoideus_anterior_0_Wavelet absolute mean_1', 'emg_deltoideus_anterior_0_Wavelet absolute mean_2', 'emg_deltoideus_anterior_0_Wavelet energy_0', 'emg_deltoideus_anterior_0_Wavelet energy_1', 'emg_deltoideus_anterior_0_Wavelet energy_2', 'emg_deltoideus_anterior_0_Wavelet entropy', 'emg_deltoideus_anterior_0_Wavelet standard deviation_0', 'emg_deltoideus_anterior_0_Wavelet standard deviation_1', 'emg_deltoideus_anterior_0_Wavelet standard deviation_2', 'emg_deltoideus_anterior_0_Wavelet variance_0', 'emg_deltoideus_anterior_0_Wavelet variance_1', 'emg_deltoideus_anterior_0_Wavelet variance_2', 'emg_deltoideus_anterior_0_Absolute energy', 'emg_deltoideus_anterior_0_Average power', 'emg_deltoideus_anterior_0_ECDF Percentile_0', 'emg_deltoideus_anterior_0_ECDF Percentile_1', 'emg_deltoideus_anterior_0_ECDF Percentile Count_0', 'emg_deltoideus_anterior_0_ECDF Percentile Count_1', 'emg_deltoideus_anterior_0_Entropy', 'emg_deltoideus_anterior_0_Histogram_0', 'emg_deltoideus_anterior_0_Histogram_1', 'emg_deltoideus_anterior_0_Histogram_2', 'emg_deltoideus_anterior_0_Histogram_3', 'emg_deltoideus_anterior_0_Histogram_4', 'emg_deltoideus_anterior_0_Histogram_5', 'emg_deltoideus_anterior_0_Histogram_6', 'emg_deltoideus_anterior_0_Histogram_7', 'emg_deltoideus_anterior_0_Histogram_8', 'emg_deltoideus_anterior_0_Histogram_9', 'emg_deltoideus_anterior_0_Interquartile range', 'emg_deltoideus_anterior_0_Kurtosis', 'emg_deltoideus_anterior_0_Max', 'emg_deltoideus_anterior_0_Mean', 'emg_deltoideus_anterior_0_Mean absolute deviation', 'emg_deltoideus_anterior_0_Median', 'emg_deltoideus_anterior_0_Median absolute deviation', 'emg_deltoideus_anterior_0_Min', 'emg_deltoideus_anterior_0_Peak to peak distance', 'emg_deltoideus_anterior_0_Root mean square', 'emg_deltoideus_anterior_0_Skewness', 'emg_deltoideus_anterior_0_Standard deviation', 'emg_deltoideus_anterior_0_Variance', 'emg_deltoideus_anterior_0_Area under the curve', 'emg_deltoideus_anterior_0_Autocorrelation', 'emg_deltoideus_anterior_0_Centroid', 'emg_deltoideus_anterior_0_Mean absolute diff', 'emg_deltoideus_anterior_0_Mean diff', 'emg_deltoideus_anterior_0_Median absolute diff', 'emg_deltoideus_anterior_0_Median diff', 'emg_deltoideus_anterior_0_Negative turning points', 'emg_deltoideus_anterior_0_Neighbourhood peaks', 'emg_deltoideus_anterior_0_Positive turning points', 'emg_deltoideus_anterior_0_Signal distance', 'emg_deltoideus_anterior_0_Slope', 'emg_deltoideus_anterior_0_Sum absolute diff', 'emg_deltoideus_anterior_0_Zero crossing rate', 'emg_deltoideus_anterior_borg_scale', 'emg_infraspinatus_0_Fundamental frequency', 'emg_infraspinatus_0_Human range energy', 'emg_infraspinatus_0_Max power spectrum', 'emg_infraspinatus_0_Maximum frequency', 'emg_infraspinatus_0_Median frequency', 'emg_infraspinatus_0_Power bandwidth', 'emg_infraspinatus_0_Spectral centroid', 'emg_infraspinatus_0_Spectral decrease', 'emg_infraspinatus_0_Spectral distance', 'emg_infraspinatus_0_Spectral entropy', 'emg_infraspinatus_0_Spectral kurtosis', 'emg_infraspinatus_0_Spectral positive turning points', 'emg_infraspinatus_0_Spectral roll-off', 'emg_infraspinatus_0_Spectral roll-on', 'emg_infraspinatus_0_Spectral skewness', 'emg_infraspinatus_0_Spectral slope', 'emg_infraspinatus_0_Spectral spread', 'emg_infraspinatus_0_Spectral variation', 'emg_infraspinatus_0_Wavelet absolute mean_0', 'emg_infraspinatus_0_Wavelet absolute mean_1', 'emg_infraspinatus_0_Wavelet absolute mean_2', 'emg_infraspinatus_0_Wavelet energy_0', 'emg_infraspinatus_0_Wavelet energy_1', 'emg_infraspinatus_0_Wavelet energy_2', 'emg_infraspinatus_0_Wavelet entropy', 'emg_infraspinatus_0_Wavelet standard deviation_0', 'emg_infraspinatus_0_Wavelet standard deviation_1', 'emg_infraspinatus_0_Wavelet standard deviation_2', 'emg_infraspinatus_0_Wavelet variance_0', 'emg_infraspinatus_0_Wavelet variance_1', 'emg_infraspinatus_0_Wavelet variance_2', 'emg_infraspinatus_0_Absolute energy', 'emg_infraspinatus_0_Average power', 'emg_infraspinatus_0_ECDF Percentile_0', 'emg_infraspinatus_0_ECDF Percentile_1', 'emg_infraspinatus_0_ECDF Percentile Count_0', 'emg_infraspinatus_0_ECDF Percentile Count_1', 'emg_infraspinatus_0_Entropy', 'emg_infraspinatus_0_Histogram_0', 'emg_infraspinatus_0_Histogram_1', 'emg_infraspinatus_0_Histogram_2', 'emg_infraspinatus_0_Histogram_3', 'emg_infraspinatus_0_Histogram_4', 'emg_infraspinatus_0_Histogram_5', 'emg_infraspinatus_0_Histogram_6', 'emg_infraspinatus_0_Histogram_7', 'emg_infraspinatus_0_Histogram_8', 'emg_infraspinatus_0_Histogram_9', 'emg_infraspinatus_0_Interquartile range', 'emg_infraspinatus_0_Kurtosis', 'emg_infraspinatus_0_Max', 'emg_infraspinatus_0_Mean', 'emg_infraspinatus_0_Mean absolute deviation', 'emg_infraspinatus_0_Median', 'emg_infraspinatus_0_Median absolute deviation', 'emg_infraspinatus_0_Min', 'emg_infraspinatus_0_Peak to peak distance', 'emg_infraspinatus_0_Root mean square', 'emg_infraspinatus_0_Skewness', 'emg_infraspinatus_0_Standard deviation', 'emg_infraspinatus_0_Variance', 'emg_infraspinatus_0_Area under the curve', 'emg_infraspinatus_0_Autocorrelation', 'emg_infraspinatus_0_Centroid', 'emg_infraspinatus_0_Mean absolute diff', 'emg_infraspinatus_0_Mean diff', 'emg_infraspinatus_0_Median absolute diff', 'emg_infraspinatus_0_Median diff', 'emg_infraspinatus_0_Negative turning points', 'emg_infraspinatus_0_Neighbourhood peaks', 'emg_infraspinatus_0_Positive turning points', 'emg_infraspinatus_0_Signal distance', 'emg_infraspinatus_0_Slope', 'emg_infraspinatus_0_Sum absolute diff', 'emg_infraspinatus_0_Zero crossing rate', 'emg_infraspinatus_borg_scale', 'emg_deltoideus_posterior_0_Fundamental frequency', 'emg_deltoideus_posterior_0_Human range energy', 'emg_deltoideus_posterior_0_Max power spectrum', 'emg_deltoideus_posterior_0_Maximum frequency', 'emg_deltoideus_posterior_0_Median frequency', 'emg_deltoideus_posterior_0_Power bandwidth', 'emg_deltoideus_posterior_0_Spectral centroid', 'emg_deltoideus_posterior_0_Spectral decrease', 'emg_deltoideus_posterior_0_Spectral distance', 'emg_deltoideus_posterior_0_Spectral entropy', 'emg_deltoideus_posterior_0_Spectral kurtosis', 'emg_deltoideus_posterior_0_Spectral positive turning points', 'emg_deltoideus_posterior_0_Spectral roll-off', 'emg_deltoideus_posterior_0_Spectral roll-on', 'emg_deltoideus_posterior_0_Spectral skewness', 'emg_deltoideus_posterior_0_Spectral slope', 'emg_deltoideus_posterior_0_Spectral spread', 'emg_deltoideus_posterior_0_Spectral variation', 'emg_deltoideus_posterior_0_Wavelet absolute mean_0', 'emg_deltoideus_posterior_0_Wavelet absolute mean_1', 'emg_deltoideus_posterior_0_Wavelet absolute mean_2', 'emg_deltoideus_posterior_0_Wavelet energy_0', 'emg_deltoideus_posterior_0_Wavelet energy_1', 'emg_deltoideus_posterior_0_Wavelet energy_2', 'emg_deltoideus_posterior_0_Wavelet entropy', 'emg_deltoideus_posterior_0_Wavelet standard deviation_0', 'emg_deltoideus_posterior_0_Wavelet standard deviation_1', 'emg_deltoideus_posterior_0_Wavelet standard deviation_2', 'emg_deltoideus_posterior_0_Wavelet variance_0', 'emg_deltoideus_posterior_0_Wavelet variance_1', 'emg_deltoideus_posterior_0_Wavelet variance_2', 'emg_deltoideus_posterior_0_Absolute energy', 'emg_deltoideus_posterior_0_Average power', 'emg_deltoideus_posterior_0_ECDF Percentile_0', 'emg_deltoideus_posterior_0_ECDF Percentile_1', 'emg_deltoideus_posterior_0_ECDF Percentile Count_0', 'emg_deltoideus_posterior_0_ECDF Percentile Count_1', 'emg_deltoideus_posterior_0_Entropy', 'emg_deltoideus_posterior_0_Histogram_0', 'emg_deltoideus_posterior_0_Histogram_1', 'emg_deltoideus_posterior_0_Histogram_2', 'emg_deltoideus_posterior_0_Histogram_3', 'emg_deltoideus_posterior_0_Histogram_4', 'emg_deltoideus_posterior_0_Histogram_5', 'emg_deltoideus_posterior_0_Histogram_6', 'emg_deltoideus_posterior_0_Histogram_7', 'emg_deltoideus_posterior_0_Histogram_8', 'emg_deltoideus_posterior_0_Histogram_9', 'emg_deltoideus_posterior_0_Interquartile range', 'emg_deltoideus_posterior_0_Kurtosis', 'emg_deltoideus_posterior_0_Max', 'emg_deltoideus_posterior_0_Mean', 'emg_deltoideus_posterior_0_Mean absolute deviation', 'emg_deltoideus_posterior_0_Median', 'emg_deltoideus_posterior_0_Median absolute deviation', 'emg_deltoideus_posterior_0_Min', 'emg_deltoideus_posterior_0_Peak to peak distance', 'emg_deltoideus_posterior_0_Root mean square', 'emg_deltoideus_posterior_0_Skewness', 'emg_deltoideus_posterior_0_Standard deviation', 'emg_deltoideus_posterior_0_Variance', 'emg_deltoideus_posterior_0_Area under the curve', 'emg_deltoideus_posterior_0_Autocorrelation', 'emg_deltoideus_posterior_0_Centroid', 'emg_deltoideus_posterior_0_Mean absolute diff', 'emg_deltoideus_posterior_0_Mean diff', 'emg_deltoideus_posterior_0_Median absolute diff', 'emg_deltoideus_posterior_0_Median diff', 'emg_deltoideus_posterior_0_Negative turning points', 'emg_deltoideus_posterior_0_Neighbourhood peaks', 'emg_deltoideus_posterior_0_Positive turning points', 'emg_deltoideus_posterior_0_Signal distance', 'emg_deltoideus_posterior_0_Slope', 'emg_deltoideus_posterior_0_Sum absolute diff', 'emg_deltoideus_posterior_0_Zero crossing rate', 'emg_deltoideus_posterior_borg_scale', 'emg_trapezius_ascendens_0_Fundamental frequency', 'emg_trapezius_ascendens_0_Human range energy', 'emg_trapezius_ascendens_0_Max power spectrum', 'emg_trapezius_ascendens_0_Maximum frequency', 'emg_trapezius_ascendens_0_Median frequency', 'emg_trapezius_ascendens_0_Power bandwidth', 'emg_trapezius_ascendens_0_Spectral centroid', 'emg_trapezius_ascendens_0_Spectral decrease', 'emg_trapezius_ascendens_0_Spectral distance', 'emg_trapezius_ascendens_0_Spectral entropy', 'emg_trapezius_ascendens_0_Spectral kurtosis', 'emg_trapezius_ascendens_0_Spectral positive turning points', 'emg_trapezius_ascendens_0_Spectral roll-off', 'emg_trapezius_ascendens_0_Spectral roll-on', 'emg_trapezius_ascendens_0_Spectral skewness', 'emg_trapezius_ascendens_0_Spectral slope', 'emg_trapezius_ascendens_0_Spectral spread', 'emg_trapezius_ascendens_0_Spectral variation', 'emg_trapezius_ascendens_0_Wavelet absolute mean_0', 'emg_trapezius_ascendens_0_Wavelet absolute mean_1', 'emg_trapezius_ascendens_0_Wavelet absolute mean_2', 'emg_trapezius_ascendens_0_Wavelet energy_0', 'emg_trapezius_ascendens_0_Wavelet energy_1', 'emg_trapezius_ascendens_0_Wavelet energy_2', 'emg_trapezius_ascendens_0_Wavelet entropy', 'emg_trapezius_ascendens_0_Wavelet standard deviation_0', 'emg_trapezius_ascendens_0_Wavelet standard deviation_1', 'emg_trapezius_ascendens_0_Wavelet standard deviation_2', 'emg_trapezius_ascendens_0_Wavelet variance_0', 'emg_trapezius_ascendens_0_Wavelet variance_1', 'emg_trapezius_ascendens_0_Wavelet variance_2', 'emg_trapezius_ascendens_0_Absolute energy', 'emg_trapezius_ascendens_0_Average power', 'emg_trapezius_ascendens_0_ECDF Percentile_0', 'emg_trapezius_ascendens_0_ECDF Percentile_1', 'emg_trapezius_ascendens_0_ECDF Percentile Count_0', 'emg_trapezius_ascendens_0_ECDF Percentile Count_1', 'emg_trapezius_ascendens_0_Entropy', 'emg_trapezius_ascendens_0_Histogram_0', 'emg_trapezius_ascendens_0_Histogram_1', 'emg_trapezius_ascendens_0_Histogram_2', 'emg_trapezius_ascendens_0_Histogram_3', 'emg_trapezius_ascendens_0_Histogram_4', 'emg_trapezius_ascendens_0_Histogram_5', 'emg_trapezius_ascendens_0_Histogram_6', 'emg_trapezius_ascendens_0_Histogram_7', 'emg_trapezius_ascendens_0_Histogram_8', 'emg_trapezius_ascendens_0_Histogram_9', 'emg_trapezius_ascendens_0_Interquartile range', 'emg_trapezius_ascendens_0_Kurtosis', 'emg_trapezius_ascendens_0_Max', 'emg_trapezius_ascendens_0_Mean', 'emg_trapezius_ascendens_0_Mean absolute deviation', 'emg_trapezius_ascendens_0_Median', 'emg_trapezius_ascendens_0_Median absolute deviation', 'emg_trapezius_ascendens_0_Min', 'emg_trapezius_ascendens_0_Peak to peak distance', 'emg_trapezius_ascendens_0_Root mean square', 'emg_trapezius_ascendens_0_Skewness', 'emg_trapezius_ascendens_0_Standard deviation', 'emg_trapezius_ascendens_0_Variance', 'emg_trapezius_ascendens_0_Area under the curve', 'emg_trapezius_ascendens_0_Autocorrelation', 'emg_trapezius_ascendens_0_Centroid', 'emg_trapezius_ascendens_0_Mean absolute diff', 'emg_trapezius_ascendens_0_Mean diff', 'emg_trapezius_ascendens_0_Median absolute diff', 'emg_trapezius_ascendens_0_Median diff', 'emg_trapezius_ascendens_0_Negative turning points', 'emg_trapezius_ascendens_0_Neighbourhood peaks', 'emg_trapezius_ascendens_0_Positive turning points', 'emg_trapezius_ascendens_0_Signal distance', 'emg_trapezius_ascendens_0_Slope', 'emg_trapezius_ascendens_0_Sum absolute diff', 'emg_trapezius_ascendens_0_Zero crossing rate', 'emg_trapezius_ascendens_borg_scale', 'emg_latissimus_dorsi_0_Fundamental frequency', 'emg_latissimus_dorsi_0_Human range energy', 'emg_latissimus_dorsi_0_Max power spectrum', 'emg_latissimus_dorsi_0_Maximum frequency', 'emg_latissimus_dorsi_0_Median frequency', 'emg_latissimus_dorsi_0_Power bandwidth', 'emg_latissimus_dorsi_0_Spectral centroid', 'emg_latissimus_dorsi_0_Spectral decrease', 'emg_latissimus_dorsi_0_Spectral distance', 'emg_latissimus_dorsi_0_Spectral entropy', 'emg_latissimus_dorsi_0_Spectral kurtosis', 'emg_latissimus_dorsi_0_Spectral positive turning points', 'emg_latissimus_dorsi_0_Spectral roll-off', 'emg_latissimus_dorsi_0_Spectral roll-on', 'emg_latissimus_dorsi_0_Spectral skewness', 'emg_latissimus_dorsi_0_Spectral slope', 'emg_latissimus_dorsi_0_Spectral spread', 'emg_latissimus_dorsi_0_Spectral variation', 'emg_latissimus_dorsi_0_Wavelet absolute mean_0', 'emg_latissimus_dorsi_0_Wavelet absolute mean_1', 'emg_latissimus_dorsi_0_Wavelet absolute mean_2', 'emg_latissimus_dorsi_0_Wavelet energy_0', 'emg_latissimus_dorsi_0_Wavelet energy_1', 'emg_latissimus_dorsi_0_Wavelet energy_2', 'emg_latissimus_dorsi_0_Wavelet entropy', 'emg_latissimus_dorsi_0_Wavelet standard deviation_0', 'emg_latissimus_dorsi_0_Wavelet standard deviation_1', 'emg_latissimus_dorsi_0_Wavelet standard deviation_2', 'emg_latissimus_dorsi_0_Wavelet variance_0', 'emg_latissimus_dorsi_0_Wavelet variance_1', 'emg_latissimus_dorsi_0_Wavelet variance_2', 'emg_latissimus_dorsi_0_Absolute energy', 'emg_latissimus_dorsi_0_Average power', 'emg_latissimus_dorsi_0_ECDF Percentile_0', 'emg_latissimus_dorsi_0_ECDF Percentile_1', 'emg_latissimus_dorsi_0_ECDF Percentile Count_0', 'emg_latissimus_dorsi_0_ECDF Percentile Count_1', 'emg_latissimus_dorsi_0_Entropy', 'emg_latissimus_dorsi_0_Histogram_0', 'emg_latissimus_dorsi_0_Histogram_1', 'emg_latissimus_dorsi_0_Histogram_2', 'emg_latissimus_dorsi_0_Histogram_3', 'emg_latissimus_dorsi_0_Histogram_4', 'emg_latissimus_dorsi_0_Histogram_5', 'emg_latissimus_dorsi_0_Histogram_6', 'emg_latissimus_dorsi_0_Histogram_7', 'emg_latissimus_dorsi_0_Histogram_8', 'emg_latissimus_dorsi_0_Histogram_9', 'emg_latissimus_dorsi_0_Interquartile range', 'emg_latissimus_dorsi_0_Kurtosis', 'emg_latissimus_dorsi_0_Max', 'emg_latissimus_dorsi_0_Mean', 'emg_latissimus_dorsi_0_Mean absolute deviation', 'emg_latissimus_dorsi_0_Median', 'emg_latissimus_dorsi_0_Median absolute deviation', 'emg_latissimus_dorsi_0_Min', 'emg_latissimus_dorsi_0_Peak to peak distance', 'emg_latissimus_dorsi_0_Root mean square', 'emg_latissimus_dorsi_0_Skewness', 'emg_latissimus_dorsi_0_Standard deviation', 'emg_latissimus_dorsi_0_Variance', 'emg_latissimus_dorsi_0_Area under the curve', 'emg_latissimus_dorsi_0_Autocorrelation', 'emg_latissimus_dorsi_0_Centroid', 'emg_latissimus_dorsi_0_Mean absolute diff', 'emg_latissimus_dorsi_0_Mean diff', 'emg_latissimus_dorsi_0_Median absolute diff', 'emg_latissimus_dorsi_0_Median diff', 'emg_latissimus_dorsi_0_Negative turning points', 'emg_latissimus_dorsi_0_Neighbourhood peaks', 'emg_latissimus_dorsi_0_Positive turning points', 'emg_latissimus_dorsi_0_Signal distance', 'emg_latissimus_dorsi_0_Slope', 'emg_latissimus_dorsi_0_Sum absolute diff', 'emg_latissimus_dorsi_0_Zero crossing rate', 'emg_latissimus_dorsi_borg_scale']
final_df=pd.DataFrame(columns=columns_list).set_index(['subject','repetition'])
result_df_emg=pd.DataFrame()
outer_join=pd.DataFrame()

for subject in data_features_35e_updated.keys():
    
    print(subject)
    column_list=[]
    for sensor in data_features_35e_updated[subject].keys():

        if sensor=='emg_data':
            for muscle in data_features_35e_updated[subject][sensor].keys():
                print(muscle)
                new_data=[]
                for ind in range(1,len(data_features_35e_updated[subject][sensor][muscle])+1):
                    print("Ind:",ind)
                    new_row={}
                    #print(subject)
                    new_row['subject']=subject
                    new_row['repetition']=ind
                    #print(subject,ind,len(data_features_35e_updated[subject][sensor][muscle])+1,data_features_35e_updated[subject][sensor][muscle][ind-1][0].shape[1])
                    for col_names in list(data_features_35e_updated[subject][sensor][muscle][ind-1][0]):
                        #print(col_names,data_features_35e_updated[subject][sensor][muscle][ind-1][0][col_names])
                        if col_names!='borg_scale':
                            new_col_name=muscle+"_"+col_names
                        else:
                            new_col_name=col_names
                        #print(data_features_35e_updated[subject][sensor][muscle][ind-1][0].iloc[0][col_names])
                        new_row[new_col_name]=data_features_35e_updated[subject][sensor][muscle][ind-1][0].iloc[0][col_names]
                    column_list.append(list(new_row.keys()))
                    new_data.append(new_row)
                mid_df=pd.DataFrame(new_data).set_index(['subject','repetition'])
                if outer_join.empty:
                    outer_join=mid_df
                else:
                    mid_df = mid_df.drop(columns=['borg_scale'])
                    outer_join = pd.merge(outer_join, mid_df, on=['subject','repetition'])
                result_join=outer_join
            if result_df_emg.empty:
                result_df_emg=result_join
            else:
                result_df_emg= pd.concat([result_df_emg, result_join], ignore_index=False)
    subject_no+=1
    outer_join = outer_join[0:0] 


#%%  Final df for imu
subject_no=0
columns_list=['subject','repetition', 'emg_pectoralis_major_0_Fundamental frequency', 'emg_pectoralis_major_0_Human range energy', 'emg_pectoralis_major_0_Max power spectrum', 'emg_pectoralis_major_0_Maximum frequency', 'emg_pectoralis_major_0_Median frequency', 'emg_pectoralis_major_0_Power bandwidth', 'emg_pectoralis_major_0_Spectral centroid', 'emg_pectoralis_major_0_Spectral decrease', 'emg_pectoralis_major_0_Spectral distance', 'emg_pectoralis_major_0_Spectral entropy', 'emg_pectoralis_major_0_Spectral kurtosis', 'emg_pectoralis_major_0_Spectral positive turning points', 'emg_pectoralis_major_0_Spectral roll-off', 'emg_pectoralis_major_0_Spectral roll-on', 'emg_pectoralis_major_0_Spectral skewness', 'emg_pectoralis_major_0_Spectral slope', 'emg_pectoralis_major_0_Spectral spread', 'emg_pectoralis_major_0_Spectral variation', 'emg_pectoralis_major_0_Wavelet absolute mean_0', 'emg_pectoralis_major_0_Wavelet absolute mean_1', 'emg_pectoralis_major_0_Wavelet absolute mean_2', 'emg_pectoralis_major_0_Wavelet energy_0', 'emg_pectoralis_major_0_Wavelet energy_1', 'emg_pectoralis_major_0_Wavelet energy_2', 'emg_pectoralis_major_0_Wavelet entropy', 'emg_pectoralis_major_0_Wavelet standard deviation_0', 'emg_pectoralis_major_0_Wavelet standard deviation_1', 'emg_pectoralis_major_0_Wavelet standard deviation_2', 'emg_pectoralis_major_0_Wavelet variance_0', 'emg_pectoralis_major_0_Wavelet variance_1', 'emg_pectoralis_major_0_Wavelet variance_2', 'emg_pectoralis_major_0_Absolute energy', 'emg_pectoralis_major_0_Average power', 'emg_pectoralis_major_0_ECDF Percentile_0', 'emg_pectoralis_major_0_ECDF Percentile_1', 'emg_pectoralis_major_0_ECDF Percentile Count_0', 'emg_pectoralis_major_0_ECDF Percentile Count_1', 'emg_pectoralis_major_0_Entropy', 'emg_pectoralis_major_0_Histogram_0', 'emg_pectoralis_major_0_Histogram_1', 'emg_pectoralis_major_0_Histogram_2', 'emg_pectoralis_major_0_Histogram_3', 'emg_pectoralis_major_0_Histogram_4', 'emg_pectoralis_major_0_Histogram_5', 'emg_pectoralis_major_0_Histogram_6', 'emg_pectoralis_major_0_Histogram_7', 'emg_pectoralis_major_0_Histogram_8', 'emg_pectoralis_major_0_Histogram_9', 'emg_pectoralis_major_0_Interquartile range', 'emg_pectoralis_major_0_Kurtosis', 'emg_pectoralis_major_0_Max', 'emg_pectoralis_major_0_Mean', 'emg_pectoralis_major_0_Mean absolute deviation', 'emg_pectoralis_major_0_Median', 'emg_pectoralis_major_0_Median absolute deviation', 'emg_pectoralis_major_0_Min', 'emg_pectoralis_major_0_Peak to peak distance', 'emg_pectoralis_major_0_Root mean square', 'emg_pectoralis_major_0_Skewness', 'emg_pectoralis_major_0_Standard deviation', 'emg_pectoralis_major_0_Variance', 'emg_pectoralis_major_0_Area under the curve', 'emg_pectoralis_major_0_Autocorrelation', 'emg_pectoralis_major_0_Centroid', 'emg_pectoralis_major_0_Mean absolute diff', 'emg_pectoralis_major_0_Mean diff', 'emg_pectoralis_major_0_Median absolute diff', 'emg_pectoralis_major_0_Median diff', 'emg_pectoralis_major_0_Negative turning points', 'emg_pectoralis_major_0_Neighbourhood peaks', 'emg_pectoralis_major_0_Positive turning points', 'emg_pectoralis_major_0_Signal distance', 'emg_pectoralis_major_0_Slope', 'emg_pectoralis_major_0_Sum absolute diff', 'emg_pectoralis_major_0_Zero crossing rate', 'emg_pectoralis_major_borg_scale', 'emg_deltoideus_anterior_0_Fundamental frequency', 'emg_deltoideus_anterior_0_Human range energy', 'emg_deltoideus_anterior_0_Max power spectrum', 'emg_deltoideus_anterior_0_Maximum frequency', 'emg_deltoideus_anterior_0_Median frequency', 'emg_deltoideus_anterior_0_Power bandwidth', 'emg_deltoideus_anterior_0_Spectral centroid', 'emg_deltoideus_anterior_0_Spectral decrease', 'emg_deltoideus_anterior_0_Spectral distance', 'emg_deltoideus_anterior_0_Spectral entropy', 'emg_deltoideus_anterior_0_Spectral kurtosis', 'emg_deltoideus_anterior_0_Spectral positive turning points', 'emg_deltoideus_anterior_0_Spectral roll-off', 'emg_deltoideus_anterior_0_Spectral roll-on', 'emg_deltoideus_anterior_0_Spectral skewness', 'emg_deltoideus_anterior_0_Spectral slope', 'emg_deltoideus_anterior_0_Spectral spread', 'emg_deltoideus_anterior_0_Spectral variation', 'emg_deltoideus_anterior_0_Wavelet absolute mean_0', 'emg_deltoideus_anterior_0_Wavelet absolute mean_1', 'emg_deltoideus_anterior_0_Wavelet absolute mean_2', 'emg_deltoideus_anterior_0_Wavelet energy_0', 'emg_deltoideus_anterior_0_Wavelet energy_1', 'emg_deltoideus_anterior_0_Wavelet energy_2', 'emg_deltoideus_anterior_0_Wavelet entropy', 'emg_deltoideus_anterior_0_Wavelet standard deviation_0', 'emg_deltoideus_anterior_0_Wavelet standard deviation_1', 'emg_deltoideus_anterior_0_Wavelet standard deviation_2', 'emg_deltoideus_anterior_0_Wavelet variance_0', 'emg_deltoideus_anterior_0_Wavelet variance_1', 'emg_deltoideus_anterior_0_Wavelet variance_2', 'emg_deltoideus_anterior_0_Absolute energy', 'emg_deltoideus_anterior_0_Average power', 'emg_deltoideus_anterior_0_ECDF Percentile_0', 'emg_deltoideus_anterior_0_ECDF Percentile_1', 'emg_deltoideus_anterior_0_ECDF Percentile Count_0', 'emg_deltoideus_anterior_0_ECDF Percentile Count_1', 'emg_deltoideus_anterior_0_Entropy', 'emg_deltoideus_anterior_0_Histogram_0', 'emg_deltoideus_anterior_0_Histogram_1', 'emg_deltoideus_anterior_0_Histogram_2', 'emg_deltoideus_anterior_0_Histogram_3', 'emg_deltoideus_anterior_0_Histogram_4', 'emg_deltoideus_anterior_0_Histogram_5', 'emg_deltoideus_anterior_0_Histogram_6', 'emg_deltoideus_anterior_0_Histogram_7', 'emg_deltoideus_anterior_0_Histogram_8', 'emg_deltoideus_anterior_0_Histogram_9', 'emg_deltoideus_anterior_0_Interquartile range', 'emg_deltoideus_anterior_0_Kurtosis', 'emg_deltoideus_anterior_0_Max', 'emg_deltoideus_anterior_0_Mean', 'emg_deltoideus_anterior_0_Mean absolute deviation', 'emg_deltoideus_anterior_0_Median', 'emg_deltoideus_anterior_0_Median absolute deviation', 'emg_deltoideus_anterior_0_Min', 'emg_deltoideus_anterior_0_Peak to peak distance', 'emg_deltoideus_anterior_0_Root mean square', 'emg_deltoideus_anterior_0_Skewness', 'emg_deltoideus_anterior_0_Standard deviation', 'emg_deltoideus_anterior_0_Variance', 'emg_deltoideus_anterior_0_Area under the curve', 'emg_deltoideus_anterior_0_Autocorrelation', 'emg_deltoideus_anterior_0_Centroid', 'emg_deltoideus_anterior_0_Mean absolute diff', 'emg_deltoideus_anterior_0_Mean diff', 'emg_deltoideus_anterior_0_Median absolute diff', 'emg_deltoideus_anterior_0_Median diff', 'emg_deltoideus_anterior_0_Negative turning points', 'emg_deltoideus_anterior_0_Neighbourhood peaks', 'emg_deltoideus_anterior_0_Positive turning points', 'emg_deltoideus_anterior_0_Signal distance', 'emg_deltoideus_anterior_0_Slope', 'emg_deltoideus_anterior_0_Sum absolute diff', 'emg_deltoideus_anterior_0_Zero crossing rate', 'emg_deltoideus_anterior_borg_scale', 'emg_infraspinatus_0_Fundamental frequency', 'emg_infraspinatus_0_Human range energy', 'emg_infraspinatus_0_Max power spectrum', 'emg_infraspinatus_0_Maximum frequency', 'emg_infraspinatus_0_Median frequency', 'emg_infraspinatus_0_Power bandwidth', 'emg_infraspinatus_0_Spectral centroid', 'emg_infraspinatus_0_Spectral decrease', 'emg_infraspinatus_0_Spectral distance', 'emg_infraspinatus_0_Spectral entropy', 'emg_infraspinatus_0_Spectral kurtosis', 'emg_infraspinatus_0_Spectral positive turning points', 'emg_infraspinatus_0_Spectral roll-off', 'emg_infraspinatus_0_Spectral roll-on', 'emg_infraspinatus_0_Spectral skewness', 'emg_infraspinatus_0_Spectral slope', 'emg_infraspinatus_0_Spectral spread', 'emg_infraspinatus_0_Spectral variation', 'emg_infraspinatus_0_Wavelet absolute mean_0', 'emg_infraspinatus_0_Wavelet absolute mean_1', 'emg_infraspinatus_0_Wavelet absolute mean_2', 'emg_infraspinatus_0_Wavelet energy_0', 'emg_infraspinatus_0_Wavelet energy_1', 'emg_infraspinatus_0_Wavelet energy_2', 'emg_infraspinatus_0_Wavelet entropy', 'emg_infraspinatus_0_Wavelet standard deviation_0', 'emg_infraspinatus_0_Wavelet standard deviation_1', 'emg_infraspinatus_0_Wavelet standard deviation_2', 'emg_infraspinatus_0_Wavelet variance_0', 'emg_infraspinatus_0_Wavelet variance_1', 'emg_infraspinatus_0_Wavelet variance_2', 'emg_infraspinatus_0_Absolute energy', 'emg_infraspinatus_0_Average power', 'emg_infraspinatus_0_ECDF Percentile_0', 'emg_infraspinatus_0_ECDF Percentile_1', 'emg_infraspinatus_0_ECDF Percentile Count_0', 'emg_infraspinatus_0_ECDF Percentile Count_1', 'emg_infraspinatus_0_Entropy', 'emg_infraspinatus_0_Histogram_0', 'emg_infraspinatus_0_Histogram_1', 'emg_infraspinatus_0_Histogram_2', 'emg_infraspinatus_0_Histogram_3', 'emg_infraspinatus_0_Histogram_4', 'emg_infraspinatus_0_Histogram_5', 'emg_infraspinatus_0_Histogram_6', 'emg_infraspinatus_0_Histogram_7', 'emg_infraspinatus_0_Histogram_8', 'emg_infraspinatus_0_Histogram_9', 'emg_infraspinatus_0_Interquartile range', 'emg_infraspinatus_0_Kurtosis', 'emg_infraspinatus_0_Max', 'emg_infraspinatus_0_Mean', 'emg_infraspinatus_0_Mean absolute deviation', 'emg_infraspinatus_0_Median', 'emg_infraspinatus_0_Median absolute deviation', 'emg_infraspinatus_0_Min', 'emg_infraspinatus_0_Peak to peak distance', 'emg_infraspinatus_0_Root mean square', 'emg_infraspinatus_0_Skewness', 'emg_infraspinatus_0_Standard deviation', 'emg_infraspinatus_0_Variance', 'emg_infraspinatus_0_Area under the curve', 'emg_infraspinatus_0_Autocorrelation', 'emg_infraspinatus_0_Centroid', 'emg_infraspinatus_0_Mean absolute diff', 'emg_infraspinatus_0_Mean diff', 'emg_infraspinatus_0_Median absolute diff', 'emg_infraspinatus_0_Median diff', 'emg_infraspinatus_0_Negative turning points', 'emg_infraspinatus_0_Neighbourhood peaks', 'emg_infraspinatus_0_Positive turning points', 'emg_infraspinatus_0_Signal distance', 'emg_infraspinatus_0_Slope', 'emg_infraspinatus_0_Sum absolute diff', 'emg_infraspinatus_0_Zero crossing rate', 'emg_infraspinatus_borg_scale', 'emg_deltoideus_posterior_0_Fundamental frequency', 'emg_deltoideus_posterior_0_Human range energy', 'emg_deltoideus_posterior_0_Max power spectrum', 'emg_deltoideus_posterior_0_Maximum frequency', 'emg_deltoideus_posterior_0_Median frequency', 'emg_deltoideus_posterior_0_Power bandwidth', 'emg_deltoideus_posterior_0_Spectral centroid', 'emg_deltoideus_posterior_0_Spectral decrease', 'emg_deltoideus_posterior_0_Spectral distance', 'emg_deltoideus_posterior_0_Spectral entropy', 'emg_deltoideus_posterior_0_Spectral kurtosis', 'emg_deltoideus_posterior_0_Spectral positive turning points', 'emg_deltoideus_posterior_0_Spectral roll-off', 'emg_deltoideus_posterior_0_Spectral roll-on', 'emg_deltoideus_posterior_0_Spectral skewness', 'emg_deltoideus_posterior_0_Spectral slope', 'emg_deltoideus_posterior_0_Spectral spread', 'emg_deltoideus_posterior_0_Spectral variation', 'emg_deltoideus_posterior_0_Wavelet absolute mean_0', 'emg_deltoideus_posterior_0_Wavelet absolute mean_1', 'emg_deltoideus_posterior_0_Wavelet absolute mean_2', 'emg_deltoideus_posterior_0_Wavelet energy_0', 'emg_deltoideus_posterior_0_Wavelet energy_1', 'emg_deltoideus_posterior_0_Wavelet energy_2', 'emg_deltoideus_posterior_0_Wavelet entropy', 'emg_deltoideus_posterior_0_Wavelet standard deviation_0', 'emg_deltoideus_posterior_0_Wavelet standard deviation_1', 'emg_deltoideus_posterior_0_Wavelet standard deviation_2', 'emg_deltoideus_posterior_0_Wavelet variance_0', 'emg_deltoideus_posterior_0_Wavelet variance_1', 'emg_deltoideus_posterior_0_Wavelet variance_2', 'emg_deltoideus_posterior_0_Absolute energy', 'emg_deltoideus_posterior_0_Average power', 'emg_deltoideus_posterior_0_ECDF Percentile_0', 'emg_deltoideus_posterior_0_ECDF Percentile_1', 'emg_deltoideus_posterior_0_ECDF Percentile Count_0', 'emg_deltoideus_posterior_0_ECDF Percentile Count_1', 'emg_deltoideus_posterior_0_Entropy', 'emg_deltoideus_posterior_0_Histogram_0', 'emg_deltoideus_posterior_0_Histogram_1', 'emg_deltoideus_posterior_0_Histogram_2', 'emg_deltoideus_posterior_0_Histogram_3', 'emg_deltoideus_posterior_0_Histogram_4', 'emg_deltoideus_posterior_0_Histogram_5', 'emg_deltoideus_posterior_0_Histogram_6', 'emg_deltoideus_posterior_0_Histogram_7', 'emg_deltoideus_posterior_0_Histogram_8', 'emg_deltoideus_posterior_0_Histogram_9', 'emg_deltoideus_posterior_0_Interquartile range', 'emg_deltoideus_posterior_0_Kurtosis', 'emg_deltoideus_posterior_0_Max', 'emg_deltoideus_posterior_0_Mean', 'emg_deltoideus_posterior_0_Mean absolute deviation', 'emg_deltoideus_posterior_0_Median', 'emg_deltoideus_posterior_0_Median absolute deviation', 'emg_deltoideus_posterior_0_Min', 'emg_deltoideus_posterior_0_Peak to peak distance', 'emg_deltoideus_posterior_0_Root mean square', 'emg_deltoideus_posterior_0_Skewness', 'emg_deltoideus_posterior_0_Standard deviation', 'emg_deltoideus_posterior_0_Variance', 'emg_deltoideus_posterior_0_Area under the curve', 'emg_deltoideus_posterior_0_Autocorrelation', 'emg_deltoideus_posterior_0_Centroid', 'emg_deltoideus_posterior_0_Mean absolute diff', 'emg_deltoideus_posterior_0_Mean diff', 'emg_deltoideus_posterior_0_Median absolute diff', 'emg_deltoideus_posterior_0_Median diff', 'emg_deltoideus_posterior_0_Negative turning points', 'emg_deltoideus_posterior_0_Neighbourhood peaks', 'emg_deltoideus_posterior_0_Positive turning points', 'emg_deltoideus_posterior_0_Signal distance', 'emg_deltoideus_posterior_0_Slope', 'emg_deltoideus_posterior_0_Sum absolute diff', 'emg_deltoideus_posterior_0_Zero crossing rate', 'emg_deltoideus_posterior_borg_scale', 'emg_trapezius_ascendens_0_Fundamental frequency', 'emg_trapezius_ascendens_0_Human range energy', 'emg_trapezius_ascendens_0_Max power spectrum', 'emg_trapezius_ascendens_0_Maximum frequency', 'emg_trapezius_ascendens_0_Median frequency', 'emg_trapezius_ascendens_0_Power bandwidth', 'emg_trapezius_ascendens_0_Spectral centroid', 'emg_trapezius_ascendens_0_Spectral decrease', 'emg_trapezius_ascendens_0_Spectral distance', 'emg_trapezius_ascendens_0_Spectral entropy', 'emg_trapezius_ascendens_0_Spectral kurtosis', 'emg_trapezius_ascendens_0_Spectral positive turning points', 'emg_trapezius_ascendens_0_Spectral roll-off', 'emg_trapezius_ascendens_0_Spectral roll-on', 'emg_trapezius_ascendens_0_Spectral skewness', 'emg_trapezius_ascendens_0_Spectral slope', 'emg_trapezius_ascendens_0_Spectral spread', 'emg_trapezius_ascendens_0_Spectral variation', 'emg_trapezius_ascendens_0_Wavelet absolute mean_0', 'emg_trapezius_ascendens_0_Wavelet absolute mean_1', 'emg_trapezius_ascendens_0_Wavelet absolute mean_2', 'emg_trapezius_ascendens_0_Wavelet energy_0', 'emg_trapezius_ascendens_0_Wavelet energy_1', 'emg_trapezius_ascendens_0_Wavelet energy_2', 'emg_trapezius_ascendens_0_Wavelet entropy', 'emg_trapezius_ascendens_0_Wavelet standard deviation_0', 'emg_trapezius_ascendens_0_Wavelet standard deviation_1', 'emg_trapezius_ascendens_0_Wavelet standard deviation_2', 'emg_trapezius_ascendens_0_Wavelet variance_0', 'emg_trapezius_ascendens_0_Wavelet variance_1', 'emg_trapezius_ascendens_0_Wavelet variance_2', 'emg_trapezius_ascendens_0_Absolute energy', 'emg_trapezius_ascendens_0_Average power', 'emg_trapezius_ascendens_0_ECDF Percentile_0', 'emg_trapezius_ascendens_0_ECDF Percentile_1', 'emg_trapezius_ascendens_0_ECDF Percentile Count_0', 'emg_trapezius_ascendens_0_ECDF Percentile Count_1', 'emg_trapezius_ascendens_0_Entropy', 'emg_trapezius_ascendens_0_Histogram_0', 'emg_trapezius_ascendens_0_Histogram_1', 'emg_trapezius_ascendens_0_Histogram_2', 'emg_trapezius_ascendens_0_Histogram_3', 'emg_trapezius_ascendens_0_Histogram_4', 'emg_trapezius_ascendens_0_Histogram_5', 'emg_trapezius_ascendens_0_Histogram_6', 'emg_trapezius_ascendens_0_Histogram_7', 'emg_trapezius_ascendens_0_Histogram_8', 'emg_trapezius_ascendens_0_Histogram_9', 'emg_trapezius_ascendens_0_Interquartile range', 'emg_trapezius_ascendens_0_Kurtosis', 'emg_trapezius_ascendens_0_Max', 'emg_trapezius_ascendens_0_Mean', 'emg_trapezius_ascendens_0_Mean absolute deviation', 'emg_trapezius_ascendens_0_Median', 'emg_trapezius_ascendens_0_Median absolute deviation', 'emg_trapezius_ascendens_0_Min', 'emg_trapezius_ascendens_0_Peak to peak distance', 'emg_trapezius_ascendens_0_Root mean square', 'emg_trapezius_ascendens_0_Skewness', 'emg_trapezius_ascendens_0_Standard deviation', 'emg_trapezius_ascendens_0_Variance', 'emg_trapezius_ascendens_0_Area under the curve', 'emg_trapezius_ascendens_0_Autocorrelation', 'emg_trapezius_ascendens_0_Centroid', 'emg_trapezius_ascendens_0_Mean absolute diff', 'emg_trapezius_ascendens_0_Mean diff', 'emg_trapezius_ascendens_0_Median absolute diff', 'emg_trapezius_ascendens_0_Median diff', 'emg_trapezius_ascendens_0_Negative turning points', 'emg_trapezius_ascendens_0_Neighbourhood peaks', 'emg_trapezius_ascendens_0_Positive turning points', 'emg_trapezius_ascendens_0_Signal distance', 'emg_trapezius_ascendens_0_Slope', 'emg_trapezius_ascendens_0_Sum absolute diff', 'emg_trapezius_ascendens_0_Zero crossing rate', 'emg_trapezius_ascendens_borg_scale', 'emg_latissimus_dorsi_0_Fundamental frequency', 'emg_latissimus_dorsi_0_Human range energy', 'emg_latissimus_dorsi_0_Max power spectrum', 'emg_latissimus_dorsi_0_Maximum frequency', 'emg_latissimus_dorsi_0_Median frequency', 'emg_latissimus_dorsi_0_Power bandwidth', 'emg_latissimus_dorsi_0_Spectral centroid', 'emg_latissimus_dorsi_0_Spectral decrease', 'emg_latissimus_dorsi_0_Spectral distance', 'emg_latissimus_dorsi_0_Spectral entropy', 'emg_latissimus_dorsi_0_Spectral kurtosis', 'emg_latissimus_dorsi_0_Spectral positive turning points', 'emg_latissimus_dorsi_0_Spectral roll-off', 'emg_latissimus_dorsi_0_Spectral roll-on', 'emg_latissimus_dorsi_0_Spectral skewness', 'emg_latissimus_dorsi_0_Spectral slope', 'emg_latissimus_dorsi_0_Spectral spread', 'emg_latissimus_dorsi_0_Spectral variation', 'emg_latissimus_dorsi_0_Wavelet absolute mean_0', 'emg_latissimus_dorsi_0_Wavelet absolute mean_1', 'emg_latissimus_dorsi_0_Wavelet absolute mean_2', 'emg_latissimus_dorsi_0_Wavelet energy_0', 'emg_latissimus_dorsi_0_Wavelet energy_1', 'emg_latissimus_dorsi_0_Wavelet energy_2', 'emg_latissimus_dorsi_0_Wavelet entropy', 'emg_latissimus_dorsi_0_Wavelet standard deviation_0', 'emg_latissimus_dorsi_0_Wavelet standard deviation_1', 'emg_latissimus_dorsi_0_Wavelet standard deviation_2', 'emg_latissimus_dorsi_0_Wavelet variance_0', 'emg_latissimus_dorsi_0_Wavelet variance_1', 'emg_latissimus_dorsi_0_Wavelet variance_2', 'emg_latissimus_dorsi_0_Absolute energy', 'emg_latissimus_dorsi_0_Average power', 'emg_latissimus_dorsi_0_ECDF Percentile_0', 'emg_latissimus_dorsi_0_ECDF Percentile_1', 'emg_latissimus_dorsi_0_ECDF Percentile Count_0', 'emg_latissimus_dorsi_0_ECDF Percentile Count_1', 'emg_latissimus_dorsi_0_Entropy', 'emg_latissimus_dorsi_0_Histogram_0', 'emg_latissimus_dorsi_0_Histogram_1', 'emg_latissimus_dorsi_0_Histogram_2', 'emg_latissimus_dorsi_0_Histogram_3', 'emg_latissimus_dorsi_0_Histogram_4', 'emg_latissimus_dorsi_0_Histogram_5', 'emg_latissimus_dorsi_0_Histogram_6', 'emg_latissimus_dorsi_0_Histogram_7', 'emg_latissimus_dorsi_0_Histogram_8', 'emg_latissimus_dorsi_0_Histogram_9', 'emg_latissimus_dorsi_0_Interquartile range', 'emg_latissimus_dorsi_0_Kurtosis', 'emg_latissimus_dorsi_0_Max', 'emg_latissimus_dorsi_0_Mean', 'emg_latissimus_dorsi_0_Mean absolute deviation', 'emg_latissimus_dorsi_0_Median', 'emg_latissimus_dorsi_0_Median absolute deviation', 'emg_latissimus_dorsi_0_Min', 'emg_latissimus_dorsi_0_Peak to peak distance', 'emg_latissimus_dorsi_0_Root mean square', 'emg_latissimus_dorsi_0_Skewness', 'emg_latissimus_dorsi_0_Standard deviation', 'emg_latissimus_dorsi_0_Variance', 'emg_latissimus_dorsi_0_Area under the curve', 'emg_latissimus_dorsi_0_Autocorrelation', 'emg_latissimus_dorsi_0_Centroid', 'emg_latissimus_dorsi_0_Mean absolute diff', 'emg_latissimus_dorsi_0_Mean diff', 'emg_latissimus_dorsi_0_Median absolute diff', 'emg_latissimus_dorsi_0_Median diff', 'emg_latissimus_dorsi_0_Negative turning points', 'emg_latissimus_dorsi_0_Neighbourhood peaks', 'emg_latissimus_dorsi_0_Positive turning points', 'emg_latissimus_dorsi_0_Signal distance', 'emg_latissimus_dorsi_0_Slope', 'emg_latissimus_dorsi_0_Sum absolute diff', 'emg_latissimus_dorsi_0_Zero crossing rate', 'emg_latissimus_dorsi_borg_scale']
final_df=pd.DataFrame(columns=columns_list).set_index(['subject','repetition'])
result_df_imu=pd.DataFrame()
outer_join=pd.DataFrame()

for subject in data_features_35e_updated.keys():

    #print(subject)
    column_list=[]
    for sensor in data_features_35e_updated[subject].keys():
        
        if sensor=='imu_data':
            for part in data_features_35e_updated[subject][sensor].keys():
                
                for part_sensor in data_features_35e_updated[subject][sensor][part].keys():
                    
                    if len(data_features_35e_updated[subject][sensor][part][part_sensor])>0:
                        new_data=[]
                        cnt=0
                        #ind here stands for the repetitions
                        for ind in range(len(data_features_35e_updated[subject][sensor][part][part_sensor])):
                            #print(f'{subject} {sensor} {part} {part_sensor} {ind} {borg_scale_interpolated_35i.iloc[subject_no,ind]}')
                            new_row={}
                            #print(subject)
                            new_row['subject']=subject
                            new_row['repetition']=ind+1
                            
                            for xyz in range(len(data_features_35e_updated[subject][sensor][part][part_sensor][ind])):
                                #print(xyz)
                                #print(f'{subject} {sensor} {part} {part_sensor} {ind} {xyz}')
                                
                                for col_names in list(data_features_35e_updated[subject][sensor][part][part_sensor][ind][xyz]):
                                    #print(col_names,data_features_35e_updated[subject][sensor][muscle][ind-1][0][col_names])
                                    if col_names!='borg_scale':
                                        if xyz==0:
                                            new_col_name='imu'+"_"+part_sensor+"_"+col_names+"_x"
                                        elif xyz==1:
                                            new_col_name='imu'+"_"+part_sensor+"_"+col_names+"_y"
                                        elif xyz==2:
                                            new_col_name='imu'+"_"+part_sensor+"_"+col_names+"_z"  
 
                                        #print(new_col_name,data_features_35i_updated[subject][sensor][part][part_sensor][ind][xyz].iloc[0][col_names])
                                        new_row[new_col_name]=data_features_35i_updated[subject][sensor][part][part_sensor][ind][xyz].iloc[0][col_names]
                            #print(cnt)
                            cnt+=1
                            new_data.append(new_row)
                        mid_df_imu=pd.DataFrame(new_data).set_index(['subject','repetition'])
                        if outer_join.empty:
                            outer_join=mid_df_imu
                        else:
                            outer_join = pd.merge(outer_join, mid_df_imu, on=['subject','repetition'])
                        result_join=outer_join
            if result_df_imu.empty:
                result_df_imu=result_join
                print("if")
                print(subject)
            else:
                result_df_imu= pd.concat([result_df_imu, result_join], ignore_index=False) 
                print("else")
                print(subject)
    outer_join = outer_join[0:0]                        
    subject_no+=1
     

#%% Combining together
df=pd.merge(result_df_emg, result_df_imu, on=['subject','repetition'])

#%% Baseline Model
import pandas as pd
import numpy as np
from sklearn.model_selection import GroupKFold, GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import RFE
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import cross_val_predict
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge

# Load the dataset
data_frame_final=df

data_frame_final=data_frame_final.reset_index()
data_frame_final=data_frame_final.drop([76, 77])    #### Check with Andrea
data_frame_final=data_frame_final.reset_index().drop(index=457)
data_frame_final=data_frame_final.reset_index()
# Separate features and target variable
X = data_frame_final.drop(columns=['borg_scale', 'subject', 'repetition'])
y = data_frame_final['borg_scale']

# Create subject and repetition groups
subjects = data_frame_final['subject']



pipeline = Pipeline([('scaler', MinMaxScaler()),
                     #('pca', PCA()),
                     #('rfe', RFE(estimator=Ridge())),
                     ('regressor', Ridge())
])

param_grid = {
    #'pca__n_components': [15,20],'rfe__n_features_to_select': [10, 15],'regressor__alpha': [0.1],
}

group_kfold = GroupKFold(n_splits=34) 

grid_search = GridSearchCV(pipeline, param_grid, cv=group_kfold.split(X, y, groups=subjects), 
                           n_jobs=-1, verbose=2, scoring='neg_mean_squared_error')

grid_search.fit(X, y)

best_params = grid_search.best_params_
best_score = grid_search.best_score_

print("Best Parameters:", best_params)
'''
Fitting 34 folds for each of 4 candidates, totalling 136 fits
Best Parameters: {'pca__n_components': 20, 'rfe__n_features_to_select': 15}
Best Score: -8.634047395259065
Best Model: Pipeline(steps=[('scaler', MinMaxScaler()), ('pca', PCA(n_components=20)),
                ('rfe', RFE(estimator=Ridge(), n_features_to_select=15)),
                ('regressor', Ridge())])

'''

print("Best Score:", best_score)

predictions=cross_val_predict(grid_search.best_estimator_, X,y,cv=group_kfold.split(X, y, groups=subjects))


best_model = grid_search.best_estimator_
print("Best Model:",best_model)
y_pred=predictions
# Plot actual vs predicted values
plt.figure(figsize=(10, 6))
plt.scatter(y, y_pred, alpha=0.6)
plt.plot([y.min(), y.max()], [y.min(), y.max()], color='red', linestyle='--', linewidth=2)
plt.xlabel('Actual Borg Scale')
plt.ylabel('Predicted Borg Scale')
plt.title('Actual vs Predicted Borg Scale Ratings - with Ridge')
plt.grid(True)
plt.show()


#%% Hyperuned Model - Ridge

import pandas as pd
import numpy as np
from sklearn.model_selection import GroupKFold, GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import RFE
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import cross_val_predict
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
import sklearn
import numpy as np

# Load the dataset
data_frame_final=df

data_frame_final=data_frame_final.reset_index()
data_frame_final=data_frame_final.drop([76, 77])    #### Check with Andrea
data_frame_final=data_frame_final.reset_index().drop(index=457)
data_frame_final=data_frame_final.reset_index()
# Separate features and target variable
X = data_frame_final.drop(columns=['borg_scale', 'subject', 'repetition'])
y = data_frame_final['borg_scale']

# Create subject and repetition groups
subjects = data_frame_final['subject']



pipeline = Pipeline([('scaler', MinMaxScaler()),('pca', PCA()),
                     ('rfe', RFE(estimator=Ridge())),
                     ('regressor', Ridge())
])

param_grid = {'pca__n_components': [15,20],'rfe__n_features_to_select': [10, 15],
              'regressor__alpha':[0.1,0.01]

}

group_kfold = GroupKFold(n_splits=34) 

grid_search = GridSearchCV(pipeline, param_grid, cv=group_kfold.split(X, y, groups=subjects), 
                           n_jobs=-1, verbose=2, scoring='neg_mean_squared_error')

grid_search.fit(X, y)

best_params = grid_search.best_params_
best_score = grid_search.best_score_

print("Best Parameters:", best_params)
'''
Fitting 34 folds for each of 4 candidates, totalling 136 fits
Best Parameters: {'pca__n_components': 20, 'rfe__n_features_to_select': 15}
Best Score: -8.634047395259065
Best Model: Pipeline(steps=[('scaler', MinMaxScaler()), ('pca', PCA(n_components=20)),
                ('rfe', RFE(estimator=Ridge(), n_features_to_select=15)),
                ('regressor', Ridge())])

'''

print("Best Score:", best_score)

predictions=cross_val_predict(grid_search.best_estimator_, X,y,cv=group_kfold.split(X, y, groups=subjects))


best_model = grid_search.best_estimator_
print("Best Model:",best_model)
y_pred=predictions
# Plot actual vs predicted values
plt.figure(figsize=(10, 6))
plt.scatter(y, y_pred, alpha=0.6)
plt.plot([y.min(), y.max()], [y.min(), y.max()], color='red', linestyle='--', linewidth=2)
plt.xlabel('Actual Borg Scale')
plt.ylabel('Predicted Borg Scale')
plt.title('Actual vs Predicted Borg Scale Ratings - with Ridge')
plt.grid(True)
plt.show()

print("Best Parameters:", best_params)
print("Best Model:",best_model)
print("Best Score:", best_score)

print("MAE:",sklearn.metrics.mean_absolute_error(predictions,y))
print("MSE:",sklearn.metrics.mean_squared_error(predictions,y))
print("Mean Absolute Percentage Error (MAPE):",sklearn.metrics.mean_absolute_percentage_error(predictions, y))
print("Root Mean Squared Error (RMSE):", np.sqrt(sklearn.metrics.mean_squared_error(predictions,y)))

#%% Hyperuned Model - Lasso

import pandas as pd
import numpy as np
from sklearn.model_selection import GroupKFold, GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import RFE
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import cross_val_predict
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge,Lasso, ElasticNet
import sklearn
import numpy as np

# Load the dataset
data_frame_final=df

data_frame_final=data_frame_final.reset_index()
data_frame_final=data_frame_final.drop([76, 77])    #### Check with Andrea
data_frame_final=data_frame_final.reset_index().drop(index=457)
data_frame_final=data_frame_final.reset_index()
# Separate features and target variable
X = data_frame_final.drop(columns=['borg_scale', 'subject', 'repetition'])
y = data_frame_final['borg_scale']

# Create subject and repetition groups
subjects = data_frame_final['subject']



pipeline = Pipeline([('scaler', MinMaxScaler()),('pca', PCA()),
                     ('rfe', RFE(estimator=Lasso())),
                     ('regressor', Lasso())
])

param_grid = {'pca__n_components': [15,20],'rfe__n_features_to_select': [10, 15],
              'regressor__alpha': [0.1],
}

group_kfold = GroupKFold(n_splits=34) 

grid_search = GridSearchCV(pipeline, param_grid, cv=group_kfold.split(X, y, groups=subjects), 
                           n_jobs=-1, verbose=2, scoring='neg_mean_squared_error')

grid_search.fit(X, y)

best_params = grid_search.best_params_
best_score = grid_search.best_score_

print("Best Parameters:", best_params)
'''
Fitting 34 folds for each of 4 candidates, totalling 136 fits
Best Parameters: {'pca__n_components': 20, 'rfe__n_features_to_select': 15}
Best Score: -8.634047395259065
Best Model: Pipeline(steps=[('scaler', MinMaxScaler()), ('pca', PCA(n_components=20)),
                ('rfe', RFE(estimator=Ridge(), n_features_to_select=15)),
                ('regressor', Ridge())])

'''

print("Best Score:", best_score)

predictions=cross_val_predict(grid_search.best_estimator_, X,y,cv=group_kfold.split(X, y, groups=subjects))


best_model = grid_search.best_estimator_
print("Best Model:",best_model)
y_pred=predictions
# Plot actual vs predicted values
plt.figure(figsize=(10, 6))
plt.scatter(y, y_pred, alpha=0.6)
plt.plot([y.min(), y.max()], [y.min(), y.max()], color='red', linestyle='--', linewidth=2)
plt.xlabel('Actual Borg Scale')
plt.ylabel('Predicted Borg Scale')
plt.title('Actual vs Predicted Borg Scale Ratings - with Ridge')
plt.grid(True)
plt.show()

print("Best Parameters:", best_params)
print("Best Model:",best_model)
print("Best Score:", best_score)

print("MAE:",sklearn.metrics.mean_absolute_error(predictions,y))
print("MSE:",sklearn.metrics.mean_squared_error(predictions,y))
print("Mean Absolute Percentage Error (MAPE):",sklearn.metrics.mean_absolute_percentage_error(predictions, y))
print("Root Mean Squared Error (RMSE):", np.sqrt(sklearn.metrics.mean_squared_error(predictions,y)))
#%% Hyperuned Model - ElasticNet

import pandas as pd
import numpy as np
from sklearn.model_selection import GroupKFold, GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import RFE
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import cross_val_predict
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge,Lasso, ElasticNet
import sklearn
import numpy as np

# Load the dataset
data_frame_final=df

data_frame_final=data_frame_final.reset_index()
data_frame_final=data_frame_final.drop([76, 77])    #### Check with Andrea
data_frame_final=data_frame_final.reset_index().drop(index=457)
data_frame_final=data_frame_final.reset_index()
# Separate features and target variable
X = data_frame_final.drop(columns=['borg_scale', 'subject', 'repetition'])
y = data_frame_final['borg_scale']

# Create subject and repetition groups
subjects = data_frame_final['subject']



pipeline = Pipeline([('scaler', MinMaxScaler()),('pca', PCA()),
                     ('rfe', RFE(estimator=ElasticNet())),
                     ('regressor', ElasticNet())
])

param_grid = {'pca__n_components': [15,20],'rfe__n_features_to_select': [10, 15],
              'regressor__alpha': [0.1],
}

group_kfold = GroupKFold(n_splits=34) 

grid_search = GridSearchCV(pipeline, param_grid, cv=group_kfold.split(X, y, groups=subjects), 
                           n_jobs=-1, verbose=2, scoring='neg_mean_squared_error')

grid_search.fit(X, y)

best_params = grid_search.best_params_
best_score = grid_search.best_score_

print("Best Parameters:", best_params)
'''
Fitting 34 folds for each of 4 candidates, totalling 136 fits
Best Parameters: {'pca__n_components': 20, 'rfe__n_features_to_select': 15}
Best Score: -8.634047395259065
Best Model: Pipeline(steps=[('scaler', MinMaxScaler()), ('pca', PCA(n_components=20)),
                ('rfe', RFE(estimator=Ridge(), n_features_to_select=15)),
                ('regressor', Ridge())])

'''

print("Best Score:", best_score)

predictions=cross_val_predict(grid_search.best_estimator_, X,y,cv=group_kfold.split(X, y, groups=subjects))


best_model = grid_search.best_estimator_
print("Best Model:",best_model)
y_pred=predictions
# Plot actual vs predicted values
plt.figure(figsize=(10, 6))
plt.scatter(y, y_pred, alpha=0.6)
plt.plot([y.min(), y.max()], [y.min(), y.max()], color='red', linestyle='--', linewidth=2)
plt.xlabel('Actual Borg Scale')
plt.ylabel('Predicted Borg Scale')
plt.title('Actual vs Predicted Borg Scale Ratings - with ElasticNet')
plt.grid(True)
plt.show()

print("Best Parameters:", best_params)
print("Best Model:",best_model)
print("Best Score:", best_score)

print("MAE:",sklearn.metrics.mean_absolute_error(predictions,y))
print("MSE:",sklearn.metrics.mean_squared_error(predictions,y))
print("Mean Absolute Percentage Error (MAPE):",sklearn.metrics.mean_absolute_percentage_error(predictions, y))
print("Root Mean Squared Error (RMSE):", np.sqrt(sklearn.metrics.mean_squared_error(predictions,y)))

#%% Hyperuned Model - LinearRegression

import pandas as pd
import numpy as np
from sklearn.model_selection import GroupKFold, GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import RFE
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import cross_val_predict
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge,Lasso, ElasticNet,LinearRegression

import sklearn
import numpy as np

# Load the dataset
data_frame_final=df

data_frame_final=data_frame_final.reset_index()
data_frame_final=data_frame_final.drop([76, 77])    #### Check with Andrea
data_frame_final=data_frame_final.reset_index().drop(index=457)
data_frame_final=data_frame_final.reset_index()
# Separate features and target variable
X = data_frame_final.drop(columns=['borg_scale', 'subject', 'repetition'])
y = data_frame_final['borg_scale']

# Create subject and repetition groups
subjects = data_frame_final['subject']



pipeline = Pipeline([('scaler', MinMaxScaler()),('pca', PCA()),
                     ('rfe', RFE(estimator=LinearRegression())),
                     ('regressor', LinearRegression())
])

param_grid = {'pca__n_components': [15,20],'rfe__n_features_to_select': [10, 15],
              #'regressor__alpha': [0.1],
}

group_kfold = GroupKFold(n_splits=34) 

grid_search = GridSearchCV(pipeline, param_grid, cv=group_kfold.split(X, y, groups=subjects), 
                           n_jobs=-1, verbose=2, scoring='neg_mean_squared_error')

grid_search.fit(X, y)

best_params = grid_search.best_params_
best_score = grid_search.best_score_

print("Best Parameters:", best_params)

print("Best Score:", best_score)

predictions=cross_val_predict(grid_search.best_estimator_, X,y,cv=group_kfold.split(X, y, groups=subjects))


best_model = grid_search.best_estimator_
print("Best Model:",best_model)
y_pred=predictions
# Plot actual vs predicted values
plt.figure(figsize=(10, 6))
plt.scatter(y, y_pred, alpha=0.6)
plt.plot([y.min(), y.max()], [y.min(), y.max()], color='red', linestyle='--', linewidth=2)
plt.xlabel('Actual Borg Scale')
plt.ylabel('Predicted Borg Scale')
plt.title('Actual vs Predicted Borg Scale Ratings - with ElasticNet')
plt.grid(True)
plt.show()

print("Best Parameters:", best_params)
print("Best Model:",best_model)
print("Best Score:", best_score)

print("MAE:",sklearn.metrics.mean_absolute_error(predictions,y))
print("MSE:",sklearn.metrics.mean_squared_error(predictions,y))
print("Mean Absolute Percentage Error (MAPE):",sklearn.metrics.mean_absolute_percentage_error(predictions, y))
print("Root Mean Squared Error (RMSE):", np.sqrt(sklearn.metrics.mean_squared_error(predictions,y)))

#%% Hyperuned Model - RandomForestRegressor

import pandas as pd
import numpy as np
from sklearn.model_selection import GroupKFold, GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import RFE
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import cross_val_predict
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge,Lasso, ElasticNet,LinearRegression

import sklearn
import numpy as np

# Load the dataset
data_frame_final=df

data_frame_final=data_frame_final.reset_index()
data_frame_final=data_frame_final.drop([76, 77])    #### Check with Andrea
data_frame_final=data_frame_final.reset_index().drop(index=457)
data_frame_final=data_frame_final.reset_index()
# Separate features and target variable
X = data_frame_final.drop(columns=['borg_scale', 'subject', 'repetition'])
y = data_frame_final['borg_scale']

# Create subject and repetition groups
subjects = data_frame_final['subject']



pipeline = Pipeline([('scaler', MinMaxScaler()),('pca', PCA()),
                     ('rfe', RFE(estimator=RandomForestRegressor())),
                     ('regressor', RandomForestRegressor())
])

# param_grid = {'pca__n_components': [15,20],'rfe__n_features_to_select': [10, 15],
#               #'regressor__alpha': [0.1],
# }
param_grid = {'pca__n_components': [15,20 ],'regressor__n_estimators': [200,300],
    'regressor__max_depth': [15,20,25],'regressor__min_samples_split': [5,6],
    'rfe__n_features_to_select': [10, 15],
}

group_kfold = GroupKFold(n_splits=34) 

grid_search = GridSearchCV(pipeline, param_grid, cv=group_kfold.split(X, y, groups=subjects), 
                           n_jobs=-1, verbose=2, scoring='neg_mean_squared_error')

grid_search.fit(X, y)

best_params = grid_search.best_params_
best_score = grid_search.best_score_

print("Best Parameters:", best_params)

print("Best Score:", best_score)

predictions=cross_val_predict(grid_search.best_estimator_, X,y,cv=group_kfold.split(X, y, groups=subjects))


best_model = grid_search.best_estimator_
print("Best Model:",best_model)
y_pred=predictions
# Plot actual vs predicted values
plt.figure(figsize=(10, 6))
plt.scatter(y, y_pred, alpha=0.6)
plt.plot([y.min(), y.max()], [y.min(), y.max()], color='red', linestyle='--', linewidth=2)
plt.xlabel('Actual Borg Scale')
plt.ylabel('Predicted Borg Scale')
plt.title('Actual vs Predicted Borg Scale Ratings - with RandomForestRegressor')
plt.grid(True)
plt.show()

print("Best Parameters:", best_params)
print("Best Model:",best_model)
print("Best Score:", best_score)

print("MAE:",sklearn.metrics.mean_absolute_error(predictions,y))
print("MSE:",sklearn.metrics.mean_squared_error(predictions,y))
print("Mean Absolute Percentage Error (MAPE):",sklearn.metrics.mean_absolute_percentage_error(predictions, y))
print("Root Mean Squared Error (RMSE):", np.sqrt(sklearn.metrics.mean_squared_error(predictions,y)))

#%% Only IMU sensors - with Ridge Regression

import pandas as pd
import numpy as np
from sklearn.model_selection import GroupKFold, GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import RFE
from sklearn.linear_model import ElasticNet, Ridge, Lasso, LinearRegression
from sklearn.model_selection import cross_val_predict
import matplotlib.pyplot as plt
import sklearn

data_frame_final=df[[col for col in df.columns if 'emg' not in col]]

data_frame_final = data_frame_final.reset_index()
data_frame_final = data_frame_final.drop([76, 77])    #### Check with Andrea
data_frame_final = data_frame_final.reset_index().drop(index=457)
data_frame_final = data_frame_final.reset_index()

# Separate features and target variable
X = data_frame_final.drop(columns=['borg_scale', 'subject', 'repetition'])
y = data_frame_final['borg_scale']


subjects = data_frame_final['subject']


regression_models = {
    'elasticnet': ElasticNet(),
    'ridge': Ridge(),
    'lasso': Lasso(),
    'linear': LinearRegression()
}


# param_grid = {
#     'pca__n_components': [7,10,12],
#     'rfe__n_features_to_select': [7,10, 15,20],
#     'regressor': list(regression_models.values())
# }

param_grid = {
    #'regressor__alpha': [ 0.1],
    'pca__n_components': [5, 15, 20],
    'rfe__n_features_to_select': [2, 5, 10, 15],
    'regressor__alpha':[0.1,0.01]
    #'regressor__l1_ratio': [0.5]
}

model =Ridge()

pipeline = Pipeline([
        ('scaler', MinMaxScaler()),
        ('pca', PCA()),
        ('rfe', RFE(estimator=Ridge())),
        ('regressor', model)
])


group_kfold = GroupKFold(n_splits=34) 


grid_search = GridSearchCV(pipeline, param_grid, 
                           cv=group_kfold.split(X, y, groups=subjects), 
                           n_jobs=-1, verbose=-1, scoring='neg_mean_squared_error')

grid_search.fit(X, y)


best_params = grid_search.best_params_
best_score = grid_search.best_score_
best_estimator = grid_search.best_estimator_

print("Best Parameters:", best_params)
print("Best Score:", best_score)
print("Best Estimator:", best_estimator)
predictions=cross_val_predict(grid_search.best_estimator_, X,y,cv=group_kfold.split(X, y, groups=subjects))


best_model = grid_search.best_estimator_
print("Best Model:",best_model)
y_pred=predictions
print("MAE:",sklearn.metrics.mean_absolute_error(predictions,y))
print("MSE:",sklearn.metrics.mean_squared_error(predictions,y))
# Plot actual vs predicted values
plt.figure(figsize=(10, 6))
plt.scatter(y, y_pred, alpha=0.6)
plt.plot([y.min(), y.max()], [y.min(), y.max()], color='red', linestyle='--', linewidth=2)
plt.xlabel('Actual Borg Scale')
plt.ylabel('Predicted Borg Scale')
plt.title(f"Actual vs Predicted Borg Scale Ratings- {model} - only imu sensors")
plt.grid(True)
plt.show()
print(best_estimator)

print("Best Parameters:", best_params)
print("Best Model:",best_model)
print("Best Score:", best_score)

print("MAE:",sklearn.metrics.mean_absolute_error(predictions,y))
print("MSE:",sklearn.metrics.mean_squared_error(predictions,y))
print("Mean Absolute Percentage Error (MAPE):",sklearn.metrics.mean_absolute_percentage_error(predictions, y))
print("Root Mean Squared Error (RMSE):", np.sqrt(sklearn.metrics.mean_squared_error(predictions,y)))

#%% Only EMG sensors - with Ridge Regression

import pandas as pd
import numpy as np
from sklearn.model_selection import GroupKFold, GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import RFE
from sklearn.linear_model import ElasticNet, Ridge, Lasso, LinearRegression
from sklearn.model_selection import cross_val_predict
import matplotlib.pyplot as plt
import sklearn

data_frame_final=df[[col for col in df.columns if 'imu' not in col]]

data_frame_final = data_frame_final.reset_index()
data_frame_final = data_frame_final.drop([76, 77])    #### Check with Andrea
data_frame_final = data_frame_final.reset_index().drop(index=457)
data_frame_final = data_frame_final.reset_index()

# Separate features and target variable
X = data_frame_final.drop(columns=['borg_scale', 'subject', 'repetition'])
y = data_frame_final['borg_scale']


subjects = data_frame_final['subject']


regression_models = {
    'elasticnet': ElasticNet(),
    'ridge': Ridge(),
    'lasso': Lasso(),
    'linear': LinearRegression()
}


# param_grid = {
#     'pca__n_components': [7,10,12],
#     'rfe__n_features_to_select': [7,10, 15,20],
#     'regressor': list(regression_models.values())
# }

param_grid = {
    #'regressor__alpha': [ 0.1],
    'pca__n_components': [5, 15, 20],
    'rfe__n_features_to_select': [2, 5, 10, 15],
    'regressor__alpha':[0.1,0.01]
    #'regressor__l1_ratio': [0.5]
}

model =Ridge()

pipeline = Pipeline([
        ('scaler', MinMaxScaler()),
        ('pca', PCA()),
        ('rfe', RFE(estimator=Ridge())),
        ('regressor', model)
])


group_kfold = GroupKFold(n_splits=34) 


grid_search = GridSearchCV(pipeline, param_grid, 
                           cv=group_kfold.split(X, y, groups=subjects), 
                           n_jobs=-1, verbose=-1, scoring='neg_mean_squared_error')

grid_search.fit(X, y)


best_params = grid_search.best_params_
best_score = grid_search.best_score_
best_estimator = grid_search.best_estimator_

print("Best Parameters:", best_params)
print("Best Score:", best_score)
print("Best Estimator:", best_estimator)
predictions=cross_val_predict(grid_search.best_estimator_, X,y,cv=group_kfold.split(X, y, groups=subjects))


best_model = grid_search.best_estimator_
print("Best Model:",best_model)
y_pred=predictions
print("MAE:",sklearn.metrics.mean_absolute_error(predictions,y))
print("MSE:",sklearn.metrics.mean_squared_error(predictions,y))
# Plot actual vs predicted values
plt.figure(figsize=(10, 6))
plt.scatter(y, y_pred, alpha=0.6)
plt.plot([y.min(), y.max()], [y.min(), y.max()], color='red', linestyle='--', linewidth=2)
plt.xlabel('Actual Borg Scale')
plt.ylabel('Predicted Borg Scale')
plt.title(f"Actual vs Predicted Borg Scale Ratings- {model} - only emg sensors")
plt.grid(True)
plt.show()
print(best_estimator)

print("Best Parameters:", best_params)
print("Best Model:",best_model)
print("Best Score:", best_score)

print("MAE:",sklearn.metrics.mean_absolute_error(predictions,y))
print("MSE:",sklearn.metrics.mean_squared_error(predictions,y))
print("Mean Absolute Percentage Error (MAPE):",sklearn.metrics.mean_absolute_percentage_error(predictions, y))
print("Root Mean Squared Error (RMSE):", np.sqrt(sklearn.metrics.mean_squared_error(predictions,y)))


#%% BACKWARD SENSOR ELIMINATION
import pandas as pd
import numpy as np
from sklearn.model_selection import GroupKFold, GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.feature_selection import RFE
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

mse_result_dict = {}
all_predictions = []
sensor_list=['emg_deltoideus_anterior'
,'emg_deltoideus_posterior'
,'emg_infraspinatus'
,'emg_latissimus_dorsi'
,'emg_pectoralis_major'
,'emg_trapezius_ascendens'
,'forearm'
,'palm'
,'pelvis'
,'shoulder'
,'torso'
,'upper_arm']    #for full df

sensors_to_be_removed_list=[]
sensor_to_be_removed=''
graph_dict=[]

while len(sensor_list)>0:
    # sensor=''
    # data_frame_final = df[[col for col in df.columns if sensor in col]]
    data_frame_final = df[[col for col in df.columns if not any(s in col for s in sensors_to_be_removed_list)]]
    data_frame_final['borg_scale'] = df['borg_scale'].to_numpy()
    data_frame_final = data_frame_final.reset_index()
    data_frame_final = data_frame_final.drop([76, 77])  # Check with Andrea
    data_frame_final = data_frame_final.reset_index().drop(index=457)
    data_frame_final = data_frame_final.reset_index()
    X = data_frame_final.drop(columns=['borg_scale', 'subject', 'repetition', 'level_0', 'index'])
    y = data_frame_final['borg_scale']
    
    
    subjects = data_frame_final['subject']
    
    # print(f"Running grid search for Ridge regression on {sensor}")
    
    pipeline = Pipeline([
        ('scaler', MinMaxScaler()),
        ('pca', PCA()),
        ('rfe', RFE(estimator=Ridge())),
        ('regressor', Ridge())
    ])
    
    param_grid = {
        'pca__n_components': [20],
        'rfe__n_features_to_select': [ 15],
        'regressor__alpha': [ 100]
    }
    
    group_kfold = GroupKFold(n_splits=34)
    
    grid_search = GridSearchCV(
        pipeline, param_grid, 
        cv=group_kfold.split(X, y, groups=subjects), 
        n_jobs=-1, verbose=-1, scoring='neg_mean_squared_error'
    )
    
    grid_search.fit(X, y)
    
    best_params = grid_search.best_params_
    best_score = grid_search.best_score_
    
    print("Best Parameters:", best_params)
    print("Best Score:", best_score)
    
    predictions = cross_val_predict(grid_search.best_estimator_, X, y, cv=group_kfold.split(X, y, groups=subjects))
    
    best_model = grid_search.best_estimator_
    print("Best Model:", best_model)
    # all_predictions.append(predictions)
    
    # mse_result_dict[sensor] = best_score
    
    # final_predictions = np.mean(all_predictions, axis=0)
    
    # final_mse = mean_squared_error(y, final_predictions)
    # print(f"Final MSE: {final_mse}")
    new_mse=best_score
    individual_sensor_removal_list={}
    graph_dict.append((len(sensor_list),best_score,sensor_to_be_removed))
    for individual_sensor in sensor_list:
        data_frame_final = df[[col for col in df.columns if not any(s in col for s in sensor)]]
        
        data_frame_final['borg_scale'] = df['borg_scale'].to_numpy()
        data_frame_final = data_frame_final.reset_index()
        data_frame_final = data_frame_final.drop([76, 77])  # Check with Andrea
        data_frame_final = data_frame_final.reset_index().drop(index=457)
        data_frame_final = data_frame_final.reset_index()
        X = data_frame_final.drop(columns=['borg_scale', 'subject', 'repetition', 'level_0', 'index'])
        y = data_frame_final['borg_scale']
    
    
        subjects = data_frame_final['subject']
    
        print(f"Running grid search for Ridge regression on {sensor}")
    
        pipeline = Pipeline([
            ('scaler', MinMaxScaler()),
            ('pca', PCA()),
            ('rfe', RFE(estimator=Ridge())),
            ('regressor', Ridge())
        ])
    
        param_grid = {
            'pca__n_components': [20],
            'rfe__n_features_to_select': [ 15],
            'regressor__alpha': [100]
        }
    
        group_kfold = GroupKFold(n_splits=34)
    
        grid_search = GridSearchCV(
            pipeline, param_grid, 
            cv=group_kfold.split(X, y, groups=subjects), 
            n_jobs=-1, verbose=-1, scoring='neg_mean_squared_error'
        )
    
        grid_search.fit(X, y)
    
        best_params = grid_search.best_params_
        best_score = grid_search.best_score_
    
        print("Best Parameters:", best_params)
        print("Best Score:", best_score)
    
        predictions = cross_val_predict(grid_search.best_estimator_, X, y, cv=group_kfold.split(X, y, groups=subjects))
    
        best_model = grid_search.best_estimator_
        print("Best Model:", best_model)
        individual_sensor_removal_list[individual_sensor]=best_score
    sensor_to_be_removed=min(individual_sensor_removal_list, key=individual_sensor_removal_list.get)
    sensors_to_be_removed_list.append(sensor_to_be_removed)
    sensor_list.remove(sensor_to_be_removed)
