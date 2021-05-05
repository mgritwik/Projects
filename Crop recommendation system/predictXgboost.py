import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from xgboost import XGBRegressor
from sklearn import preprocessing,cross_validation
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import GradientBoostingRegressor,RandomForestRegressor

#for conversion of non numerical categorical data into numerical data
def convert_to_integer(df):
	
	m_map={'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12}
	columns=df.columns.values		#returns all the names of the columns

	for column in columns:
		if(column!='Month'):
			mappings={} #dictinary to store the mappings example {'female':0,'male':1}
			def mapper(val):
				return mappings[val] 	#this returns the value of the int that val has been mapped to
		
			if df[column].dtype!=np.int64 and df[column].dtype!=np.float64:	#if datatype of column is not int/float then:
				column_values=set((df[column].values.tolist()))				#get all the column contents(all possible values present in the column and form a list)
				column_values=sorted(column_values)						
				x=0
				for each in column_values:
					if each not in mappings:						#if unique not in text value,i,e: if not predefined in the text_didgit_vals list hen define ot right now
						mappings[each]=x
						x+=1

				df[column]=list(map(mapper,df[column]))		#inbuilt map functin in pandas to map the values of df[column] to its corresponding convert_to_int function
				#map(aFunction, aSequence) function applies a passed-in function to each item in an iterable object and returns a list containing all the function call results.

			if column=='APMC':
				apmc_mappings=mappings
				print('*'*100)
				print('APMC Mappings are: ',apmc_mappings)
				print('*'*100)
			elif column=='Commodity':
				commo_mappings=mappings
				print('*'*100)
				print('Commodities Mappings are: ',commo_mappings)
				print('*'*100)
		else:
			for i in df.index:
				val=m_map[df.loc[i][column]]
				df.at[i,column]=val
	return df,m_map
warnings.filterwarnings("ignore")


#for a particular Commodity
df=pd.read_csv('apmc_data_1.csv')
#df=df[df['Commodity']==comm.lower()]  #for conversion of all commoditiey names to uniform(here lowerCase) format
# print(df.head())



# #removal of outliers
q1=df['modal_price'].quantile(0.25)
q3=df['modal_price'].quantile(0.75)
iqr=q3-q1
low=q1-1.5*iqr
high=q3+1.5*iqr
df=df.loc[(df['modal_price']>low) & (df['modal_price']<high)]
df,month_map=convert_to_integer(df)
y=np.array(df['modal_price'])		#set lablels
df.drop(['min_price','max_price','modal_price','state_name','arrivals_in_qtl'],1,inplace=True)
x=np.array(df)  #remove the output and state_name column for target features
x=preprocessing.scale(x)	#preprocessing to scale all the feature values to uniform scale
accuracy=0
features=df.columns
n_features=len(features)

#to ge the average of 10 train attempts with increasing estimators
estimators=100		#gradual increment to see the increment
for i in range(0,10):
	x_train,x_test,y_train,y_test=cross_validation.train_test_split(x,y,test_size=0.2,random_state=3)
	clf=XGBRegressor(n_estimators=estimators,max_depth=9,min_samples_split=2,learning_rate=0.5,booster='gbtree')
	# clf=RandomForestRegressor(n_estimators=estimators,max_depth=None,max_features=n_features,min_samples_split=2)
	clf.fit(x_train,y_train)
	temp=clf.score(x_test,y_test)
	print(i,estimators,temp)	#for each iteration observing the accuracy
	accuracy+=temp
	estimators+=100
print('Accuracy is',accuracy/10)	#average accuracy of 10 iterations

#best accuracy is observed at n_estimators =200


#cross_validation_score
# cv_acc=cross_val_score(clf,x,y,cv=5)
# print('Cross validation score is: ',cv_acc)
#for prediction of the future values

#make an input query
pred_array=np.zeros((3,6)) #for 3months with 6 input values
df=df.sort_values(by=['date','Year','Month'],ascending=True)

apmc=input('Enter the APMC code corresponding to name to get the prediction values: ')
pred_array[:,0]=apmc#set apmc

commo=input('Enter the commo code corresponding to name to get the prediction values: ')
pred_array[:,1]=commo#set apmc
mon_map={1:'January',2:'February',3:'March'}

temp=df.iloc[-1]['Month']
# print('Month is :   ',df.iloc[-1])
if temp+1>12:
	pred_array[0,3]=month_map[mon_map[1]]#set month
	pred_array[0,2]=df.iloc[-1]['Year']+1	#set year
else:
	pred_array[0,3]=df.iloc[-1]['Month']+1#set month
	pred_array[0,2]=df.iloc[-1]['Year']#set year

if temp+2>12:
	pred_array[1,3]=month_map[mon_map[(temp+2)%12]]#set month
	pred_array[1,2]=df.iloc[-1]['Year']+1	#set year
else:
	pred_array[1,3]=df.iloc[-1]['Month']+2#set month
	pred_array[1,2]=df.iloc[-1]['Year']#set year


if temp+3>12:
	pred_array[2,3]=month_map[mon_map[(temp+3)%12]]#set month
	pred_array[2,2]=df.iloc[-1]['Year']+1	#set year
else:
	pred_array[2,3]=df.iloc[-1]['Month']+3#set month
	pred_array[2,2]=df.iloc[-1]['Year']#set year

pred_array[0,4]=df.iloc[-1]['date']+1#set date
pred_array[1,4]=df.iloc[-1]['date']+2
pred_array[2,4]=df.iloc[-1]['date']+3


df1=df[df['APMC']==int(apmc)]		#to get the district name
dname=df1.iloc[0]['district_name']
pred_array[:,5]=dname
op=np.array([[0,0,0,0,0,0]])

for i in range(0,3):
	op[0]=pred_array[i]
	# y=y.reshape(-1,len(x))
	print('Input for prediction: ',np.array(op))
	result_array=clf.predict(np.array(op))
	print('Output for prediction for future ',i, ' month: ',result_array)

print(clf.get_params())