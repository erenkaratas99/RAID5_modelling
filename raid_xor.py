# -*- coding: utf-8 -*-


#RAID5 Basic Working Principle Modelling

#data : water level of Venezia/Italy w/respect to time

#author : Eren Karataş

#%%


import numpy as np

import pandas as pd

        
df = pd.read_csv(r"C:\Users\KULLANICI\Desktop\RAID5_model\archive\venezia.csv")
df = df.iloc[:int(len(df)/3)] #chopping the dataset
#%% adjusting the dataset 
df.columns = [each.lower() for each in df.columns]
df.columns = [each.split()[0]+"_"+each.split()[1] if(len(each.split())>1) else each for each in df.columns]


#%%converting the datetime to timestamp
df['datetime'] = pd.to_datetime(df['datetime'])
df['timestamp'] = df.datetime.values.astype(np.int64)
df.pop('datetime')
#%%rearranging the values to easily handle
df.timestamp = [each/(11**12) for each in df.timestamp]
df.timestamp = [int(each) for each in df.timestamp]
df.level = [int(abs(each)) for each in df.level]


#%% dropping null values and copying the real dataframe
df = df.dropna()
df_back = df.copy()
#%%creating the sections of the real dataframe with non-binary values
df1back = df_back.iloc[:int(len(df_back)/3)]
df2back = df_back.iloc[int(len(df_back)/3):int(len(df_back)/3)*2]
df3back = df_back.iloc[int(len(df_back)/3)*2::]

#%% converting the values into binary
df.timestamp = [bin(each)[2:].zfill(30) for each in df.timestamp]
df.level = [bin(each)[2:].zfill(8) for each in df.level]

#%% splitting the dataframe
df1 = df.iloc[:int(len(df)/3)]
df2 = df.iloc[int(len(df)/3):int(len(df)/3)*2]
df3 = df.iloc[int(len(df)/3)*2::]

#%%

v_level = []
#Applying XOR to all values of level col.
for each in range(len(df1)):
    temp = int(df1.level[each],2) ^ int(df2.level[len(df1)+each],2)
    temp = bin(temp)[2:].zfill(len(df1.level[each]))
    temp2 = int(temp,2) ^ int(df3.level[2*len(df1)+each],2)
    temp2 = bin(temp2)[2:].zfill(len(df1.level[each]))
    v_level.append(temp2)
#%%
    
v_timestamp = []
#Applying XOR to all values of timestamp col.
for each in range(len(df1)):
    temp = int(df1.timestamp[each],2) ^ int(df2.timestamp[len(df1)+each],2)
    temp = bin(temp)[2:].zfill(30)
    temp2 = int(temp,2) ^ int(df3.timestamp[2*len(df1)+each],2)
    temp2 = bin(temp2)[2:].zfill(30)
    v_timestamp.append(temp2)
    
#%%creating the validation dataframe 
df_lev = pd.DataFrame(v_level)
df_ts = pd.DataFrame(v_timestamp)

validation_df = pd.concat([df_lev , df_ts],axis = 1)
validation_df.columns = ['level','timestamp']
#%% deleting unnecessary parts
del  df_lev, df_ts, v_level, v_timestamp

#%%Imaginary crash test
#lets assume sector 2 crashes (it may be a physical harm like burning etc.)

#copying to check after whether if the new created df2 will match and deleting df2 to test the crash
df2_bin_back = df2.copy()
del df2
#%%for level
temp_li = []
df2level_new = []

for i in range(len(validation_df)):
    for j in range(len(validation_df.level[i])):
        if(validation_df.level[i][j] == '1' and df3.level[2*len(validation_df)+i][j] == '0' and df1.level[i][j] == '1'):
            temp_li.append(0)
        elif(validation_df.level[i][j] == '1' and df3.level[2*len(validation_df) +i][j] == '1' and df1.level[i][j] == '1'):
            temp_li.append(1)
        elif(validation_df.level[i][j] == '0' and df3.level[2*len(validation_df) +i][j] == '0' and df1.level[i][j] == '1'):
            temp_li.append(1)
        elif(validation_df.level[i][j] == '0' and df3.level[2*len(validation_df) +i][j] == '1' and df1.level[i][j] == '1'):
            temp_li.append(0)
        elif(validation_df.level[i][j] == '1' and df3.level[2*len(validation_df) +i][j] == '0' and df1.level[i][j] == '0'):
            temp_li.append(1)
        elif(validation_df.level[i][j] == '1' and df3.level[2*len(validation_df) +i][j] == '1' and df1.level[i][j] == '0'):
            temp_li.append(0)
        elif(validation_df.level[i][j] == '0' and df3.level[2*len(validation_df) +i][j] == '0' and df1.level[i][j] == '0'):
            temp_li.append(0)
        elif(validation_df.level[i][j] == '0' and df3.level[2*len(validation_df) +i][j] == '1' and df1.level[i][j] == '0'):
            temp_li.append(1)
    temp_str = ''.join([str(elem) for elem in temp_li])
    del temp_li
    temp_li = []
    df2level_new.append(temp_str)
    del temp_str
#%%for timestamp
temp_li = []
df2ts_new = []

for i in range(len(validation_df)):
    for j in range(len(validation_df.timestamp[i])):
        
        if(validation_df.timestamp[i][j] == '1' and df3.timestamp[2*len(df1)+i][j] == '0' and df1.timestamp[i][j] == '1'):
            temp_li.append(0)
        elif(validation_df.timestamp[i][j] == '1' and df3.timestamp[2*len(df1) +i][j] == '1' and df1.timestamp[i][j] == '1'):
            temp_li.append(1)
        elif(validation_df.timestamp[i][j] == '0' and df3.timestamp[2*len(df1) +i][j] == '0' and df1.timestamp[i][j] == '1'):
            temp_li.append(1)
        elif(validation_df.timestamp[i][j] == '0' and df3.timestamp[2*len(df1) +i][j] == '1' and df1.timestamp[i][j] == '1'):
            temp_li.append(0)
        elif(validation_df.timestamp[i][j] == '1' and df3.timestamp[2*len(df1) +i][j] == '0' and df1.timestamp[i][j] == '0'):
            temp_li.append(1)
        elif(validation_df.timestamp[i][j] == '1' and df3.timestamp[2*len(df1) +i][j] == '1' and df1.timestamp[i][j] == '0'):
            temp_li.append(0)
        elif(validation_df.timestamp[i][j] == '0' and df3.timestamp[2*len(df1) +i][j] == '0' and df1.timestamp[i][j] == '0'):
            temp_li.append(0)
        elif(validation_df.timestamp[i][j] == '0' and df3.timestamp[2*len(df1) +i][j] == '1' and df1.timestamp[i][j] == '0'):
            temp_li.append(1)
    temp_str = ''.join([str(elem) for elem in temp_li])
    print(i)
    del temp_li
    temp_li = []
    df2ts_new.append(temp_str)
    del temp_str
#%%           
df2ts_new_df = pd.DataFrame(df2ts_new)
df2level_new_df = pd.DataFrame(df2level_new)

df2_bin_back.reset_index(drop=True, inplace = True)

df2_new_bin = pd.concat([df2level_new_df , df2ts_new_df],axis = 1)
df2_new_bin.columns = ['level','timestamp']

df2_new_level = [int(each,2) for each in df2level_new_df[0]]
df2_new_ts = [int(each,2) for each in df2ts_new_df[0]]

df2_new_ts = pd.DataFrame(df2_new_ts)
df2_new_level = pd.DataFrame(df2_new_level)

df2_new = pd.concat([ df2_new_level , df2_new_ts],axis = 1)
df2_new.columns = ['level','timestamp']

df2back.reset_index(drop=True, inplace = True)

'''
df2_new_bin : (binary form) created after crash of real df2, by checking the xor structure
df2_new : created after crash of real df2, by checking the xor structure

df2_bin_back : back-up of df2 (binary form) copied before crashing
df2back : back-up of df2 copied before crashing
'''


print('are the lost df2 is equal to new created one (bin) :',df2_bin_back.equals(df2_new_bin))
print('are the lost df2 is equal to new created one  :',df2back.equals(df2_new))


