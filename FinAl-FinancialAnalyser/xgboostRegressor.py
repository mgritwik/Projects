import numpy as np
import pandas as pd
from sklearn import preprocessing,cross_validation
from sklearn.ensemble import GradientBoostingRegressor
import pickle
from xgboost import XGBRegressor
temp=0
# ID,ATM Name,Transaction Date,No Of Withdrawals,No Of CUB Card Withdrawals,No Of Other Card Withdrawals,Total amount Withdrawn,
# Amount withdrawn CUB Card,Amount withdrawn Other Card,averageWithdrawals,Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,
# WorkingDay,H,N,C,M,NH,HWH,HHW,WWH,WHH,HWW,WWW,WHW,HHH,Rounded Amount Withdrawn,class,AvgAmountPerWithdrawal

df=pd.read_csv('ClassificationData.csv')
df=df[df['ATM Name']=='Christ College ATM']
df.drop(['ID','ATM Name','Transaction Date','No Of Withdrawals','No Of CUB Card Withdrawals','No Of Other Card Withdrawals',
		  'class','Amount withdrawn CUB Card','Amount withdrawn Other Card','Rounded Amount Withdrawn','AvgAmountPerWithdrawal'],1,inplace=True)
X=np.array(df.drop(['Total amount Withdrawn'],1))
print(X[0,:])
X=preprocessing.scale(X)
y=np.array(df['Total amount Withdrawn'])


# Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,
# WorkingDay,H,N,C,M,NH,HWH,HHW,WWH,WHH,HWW,WWW,WHW,HHH,averageWithdrawals,AvgAmountPerWithdrawal

# for i in range(50): #for finding the average accuracy over 50 iterations
X_train,X_test,y_train,y_test=cross_validation.train_test_split(X,y,test_size=0.2)
# clf=XGBRegressor(n_estimators=80,max_depth=7)
clf=XGBRegressor(n_estimators=80,max_depth=3,learning_rate=0.1,warm_start=True)
clf.fit(X_train,y_train)
# with open('gradientBoosting.pickle','wb') as f:
# 	pickle.dump(clf,f)

# for i in range(50):
# pickle_in=open('gradientBoosting.pickle','rb')
# clf=pickle.load(pickle_in)
accuracy=clf.score(X_test,y_test)
print('Accuracy is:',accuracy)
# 	temp+=accuracy

# print('Average accuracy is:',temp*2)


#Predict the value of the amount to be deposited

working_day=0
holidays=['Saturday','Sunday']
np.set_printoptions(suppress=True)


df=pd.read_csv('ClassificationData.csv')
df.drop(['ID','Transaction Date','No Of Withdrawals','No Of CUB Card Withdrawals','No Of Other Card Withdrawals',
		  'class','Amount withdrawn CUB Card','Amount withdrawn Other Card','Rounded Amount Withdrawn','Total amount Withdrawn'],1,inplace=True)

atm_name=(input('Enter atm name: ').title()+' ATM')
if atm_name=='Kk Nagar ATM':
	atm_name='KK Nagar ATM'
day=input('Name of the day: ').title()
working_day=int(input('Working day(yes-1/no-0): '))
festival_religion=input('Holiday-religion(H/N/C/M/NH): ').upper()
holiday_sequence=input('Working Day Sequence(HHH/WWW... )').upper()

predict_query=np.zeros(shape=(1,22))

#day vector
if day=='Sunday':
	predict_query[0,0]=1
	# holiday_sequence='HHW'
elif day=='Monday':
	predict_query[0,1]=1
	# holiday_sequence='HWW'
elif day=='Tuesday':
	predict_query[0,2]=1
	# holiday_sequence='WWW'
elif day=='Wednesday':
	predict_query[0,3]=1
	# holiday_sequence='WWW'
elif day=='Thursday':
	predict_query[0,4]=1
	# holiday_sequence='WWW'
elif day=='Friday':
	predict_query[0,5]=1
	# holiday_sequence='WWH'
elif day=='Saturday':
	predict_query[0,6]=1
	# holiday_sequence='WHH'

#working day vector
if working_day:
	predict_query[0,7]=1

#festival religion vector
if festival_religion=='H':
	predict_query[0,8]=1
elif festival_religion=='N':
	predict_query[0,9]=1
elif festival_religion=='C':
	predict_query[0,10]=1
elif festival_religion=='M':
	predict_query[0,11]=1
elif festival_religion=='NH':
	predict_query[0,12]=1


#holiday sequence vector
if holiday_sequence=='HWH':
	predict_query[0,13]=1
elif holiday_sequence=='HHW':
	predict_query[0,14]=1
elif holiday_sequence=='WWH':
	predict_query[0,15]=1
elif holiday_sequence=='WHH':
	predict_query[0,16]=1
elif holiday_sequence=='HWW':
	predict_query[0,17]=1
elif holiday_sequence=='WWW':
	predict_query[0,18]=1
elif holiday_sequence=='WHW':
	predict_query[0,19]=1
elif holiday_sequence=='HHH':
	predict_query[0,20]=1

df=df[df['ATM Name']==atm_name]

#comment_out
for df_index in range(len(df.index)):
	print('First df.index: ',df_index)
	for i in range((predict_query.shape[1]-1)):
		print(int(predict_query[0,i]))
		print(df.iloc[df_index][i+1])
		print('@'*20)
		if int(predict_query[0,i])==int(df.iloc[df_index][i+1]):
			print('Equal at: ',i)
		else:
			break
	if i==20:
		break

if i==20:
	print('Equal vector found..')
	predict_query[0,21]=int(df.iloc[df_index][22])
	# predict_query[0,22]=int(df.iloc[df_index][23])
	predict_query.astype(int)
	print(predict_query)

prediction=clf.predict(predict_query)

print('Prediction of the input vector is: ',prediction)
