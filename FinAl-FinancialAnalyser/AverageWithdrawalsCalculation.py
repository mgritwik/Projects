import pandas as pd
import numpy as np

temp=count=0
indices=[]
day=atm_name=festival_religion=holiday_sequence=working_day={}
df=pd.read_csv('aggregatedDataCopy.csv')
df.drop(['Unnamed: 0','Unnamed: 0.1'],1,inplace=True)
df['averageWithdrawals']=0

day=set(df['Weekday'].values.tolist())
atm_name=set(df['ATM Name'].values.tolist())
festival_religion=set(df['Festival Religion'].values.tolist())
holiday_sequence=set(df['Holiday Sequence'].values.tolist())
working_day=set(df['Working Day'].values.tolist())


for d in day:
	for a in atm_name:
		for f in festival_religion:
			for h in holiday_sequence:
				for w in working_day:
					count+=1
					indices=np.where((df['Weekday']==d)&(df['ATM Name']==a)&(df['Festival Religion']==f)&(df['Holiday Sequence']==h)&(df['Working Day']==w))
					for each in indices:
						#print(indices)
						avg=df.loc[each]['No Of Withdrawals'].tolist()
					if(len(avg)!=0):
						avg1=int(np.ceil(sum(avg)/len(avg)))
					else:
						continue
					for each in indices:
						df.at[each,'averageWithdrawals']=avg1	


df.to_csv('processedCUBdata.csv',sep=',')
print(count)
'''
ID,ATM Name,Transaction Date,No Of Withdrawals,No Of CUB Card Withdrawals,
No Of Other Card Withdrawals,Total amount Withdrawn,
Amount withdrawn CUB Card,Amount withdrawn Other Card,Weekday,Festival Religion,Working Day,Holiday Sequence
'''