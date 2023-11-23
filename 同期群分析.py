#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from pynverse import inversefunc
#Import data
path="C:/Users/卢卓/Desktop/实习/data1.txt"
data=pd.read_csv(path,sep='\t')
data.head()
data=data[["user_id","behavior_type","time"]]

#Wrangle data
data.info()#After inspection, there is no missing data
data['time'].value_counts().sort_index()#Since there is only one customer on 12-22, we have chosen to remove this day with an interval of 11-18 to 12-18
day_list=data['time'].drop(data['time'].index[0]).unique()
day_list.sort()
final=pd.DataFrame()

#Calculate retention rate
for i in range(len(day_list)-1):
    temp=[0]*len(day_list)
    temp_list=data.loc[data['time']==day_list[i],:]
    if i==0:
        new_customer=temp_list
    else:
        history_list=data.loc[data['time'].isin(day_list[:i]),:]
        new_customer=temp_list.loc[temp_list['user_id'].isin(history_list['user_id'])==False,:]
    temp[0]=len(new_customer)
    for j,k in zip(range(i+1,len(day_list)),range(1,len(day_list))):
        next_day=data.loc[data['time']==day_list[j],:]
        number=temp_list['user_id'].isin(next_day['user_id']).sum()
        temp[k]=number
    result = pd.DataFrame({day_list[i]:temp}).T
    final=pd.concat([final,result])


#Show results
final.columns = ['users added on the same day','1 day','2 day','3 day','4 day','5 day','6 day','7 day','8 day','9 day','10 day','11 day','12 day','13 day','14 day','15 day','16 day','17 day','18 day','19 day','20 day','21 day','22 day','23 day','24 day','25 day','26 day','27 day','28 day','29 day','30 day']
final_result=final.divide(final['Users added on the same day'],axis=0).iloc[:,1:]
final_result['Users added']=final['Users added on the same day']
final_result.head()

#Calculate LTV value

#Manage data type
path1="C:/Users/卢卓/Desktop/实习/arpu.txt"
data_=pd.read_csv(path1,sep=',')
data_.head()
data1=pd.melt(data,id_vars=['Date'])
data1['x']=data1['variable'].str.split(' ',1,True)[1].astype(int)
data1['y']=data1['value'].str.split('%',1,True)[0].astype(float)/100
data2=pd.melt(data_,id_vars=['Date'])
data2['x']=data2['variable'].str.split(' ',1,True)[1].astype(int)

#Visualize data
plt.scatter(x=data1['x'],y=data1['y'])
plt.scatter(x=data2['x'],y=data2['value'])


#Define my own function for fitting
def fun_r(x, a, b):
    return a**x + b
popt1, pcov1 = curve_fit(fun_r, data1['x'], data1['y'])
y1 = [fun_r(i,popt1[0],popt1[1]) for i in data1['x']]
plt.plot(data1['x'],y1,'r--')

def fun_a(x, a, b, c):
    return a*x*x + b*x+c
popt2, pcov2 = curve_fit(fun_a, data2['x'], data2['value'])
y2 = [fun_a(i,popt2[0],popt2[1],popt2[2]) for i in data2['x']]
plt.plot(data2['x'],y2,'b--')

#Calculate result
s = 0
for i in range(1,14):
    s = s + fun_r(i,popt1[0],popt1[1])*fun_a(i,popt2[0],popt2[1],popt2[2])
print(s)

