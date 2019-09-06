import pandas as pd
import numpy as np


df=pd.read_csv('AggregatedData2.csv')
df['AvgAmountPerWithdrawal']=0

for i in df.index:
	df.at[i,df.iloc[i]['AvgAmountPerWithdrawal']]=int(df.iloc[i]['Total amount Withdrawn']/df.iloc[i]['No Of Withdrawals'])


df.to_csv('AggregatedData2.csv',sep=',')

'''
temp=count=0
indices=[]
day=atm_name=festival_religion=holiday_sequence=working_day={}
df=pd.read_csv('newClassesData.csv')
#f.drop(['Unnamed: 0','Unnamed: 0.1'],1,inplace=True)
df['averageAmountWithdrawn']=0

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
						avg=df.loc[each]['Total amount Withdrawn'].tolist()
					if(len(avg)!=0):
						avg1=int(np.ceil(sum(avg)/len(avg)))
					else:
						continue
					for each in indices:
						df.at[each,'averageAmountWithdrawn']=avg1	


df.to_csv('newClassesData.csv',sep=',')
print(count)

ID,ATM Name,Transaction Date,No Of Withdrawals,No Of CUB Card Withdrawals,
No Of Other Card Withdrawals,Total amount Withdrawn,
Amount withdrawn CUB Card,Amount withdrawn Other Card,Weekday,Festival Religion,Working Day,Holiday Sequence


#for converting the categorical data into one-hot encoding

import numpy as np
import pandas as pd
#from titlecase import titlecase

	

df1= pd.read_csv('processedCUBdata1.csv')
df2=pd.read_csv('AggregatedData.csv')
#df.drop(['Unnamed: 0.1.1','Festival Religion'],1,inplace=True)



df1['Sunday']=0
df1['Monday']=0
df1['Tuesday']=0
df1['Wednesday']=0
df1['Thursday']=0
df1['Friday']=0
df1['Saturday']=0
#print(df1.head(10))


for i in df1.index:
	df1.at[i,df1.iloc[i]['Weekday'].title()]=1

df1.to_csv('processedCUBdata1.csv',sep=',')


df['WorkingDay']=1
for i in df.index:
	if df.iloc[i]['Working Day']=='H':
		df.at[i,'Working Day']=0


df.to_csv('processedCUBdata1.csv',sep=',')

xlist=set(df['Festival Religion'].tolist())
for each in xlist:
	df[each]=0
#print(xlist)
for i in df.index:
	df.at[i,df.iloc[i]['Festival Religion']]=1

df.to_csv('processedCUBdata1.csv',sep=',')



xlist=set(df['Holiday Sequence'].tolist())
for each in xlist:
	df[each]=0

for i in df.index:
	df.at[i,df.iloc[i]['Holiday Sequence']]=1

df.drop(['Holiday Sequence'],1,inplace=True)

df.to_csv('processedCUBdata1.csv',sep=',')


xlist=np.where(df2['Working Day']=='H')
for i in xlist:
	df1.at[i,'WorkingDay']=0

df1.to_csv('processedCUBdata1.csv',sep=',')


#checking if all the elemnts have been correctly assinged during the conversion
xlist=np.sort(np.array(np.where(df2['Working Day']=='H')))
ylist=np.sort(np.array(np.where(df1['WorkingDay']==0)))
#print(size(xlist))

for i in range(len(xlist[0])):
	if xlist[0][i]!=ylist[0][i]:
		print(xlist[i],ylist[j])
	else:
		print('Equal')



#adding a new feature: Rounding off to the nearest ceil of 50000

import numpy as np
import pandas as pd

df=pd.read_csv('processedCUBdata1.csv')
#df.drop(['Transaction Date'],1,inplace=True)
for i in df.index:
	tmp=df.iloc[i]['Total amount Withdrawn']
	if tmp%50000==0:
		roundedtmp=tmp
	else:
		roundedtmp=tmp+50000
		tmp=roundedtmp%50000
		roundedtmp-=tmp
	df.at[i,'Rounded Amount Withdrawn']=roundedtmp

df.to_csv('processedCUBdata1.csv',sep=',')


#for building up the classes for converitng the regression problem into a classification problem\\import pandas as pd
import numpy as np


df=pd.read_csv('processedCUBdata1.csv')

xlist=list(set(df['Rounded Amount Withdrawn'].values.tolist()))
xlist.sort()


df['class']=0
for i in df.index:
	df.at[i,'class']=xlist.index(df.iloc[i]['Rounded Amount Withdrawn'])+1

df.to_csv('ClassificationData.csv', sep=',')
'''


