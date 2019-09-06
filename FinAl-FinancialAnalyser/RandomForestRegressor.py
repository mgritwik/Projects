import numpy as np
import pandas as pd
from sklearn import preprocessing,cross_validation
from sklearn.ensemble import RandomForestRegressor
import pickle
# ID,ATM Name,Transaction Date,No Of Withdrawals,No Of CUB Card Withdrawals,No Of Other Card Withdrawals,Total amount Withdrawn,
# Amount withdrawn CUB Card,Amount withdrawn Other Card,averageWithdrawals,Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,
# WorkingDay,H,N,C,M,NH,HWH,HHW,WWH,WHH,HWW,WWW,WHW,HHH,Rounded Amount Withdrawn,class,AvgAmountPerWithdrawal

df=pd.read_csv('ClassificationData.csv')
df=df[df['ATM Name']=='Big Street ATM']
df.drop(['ID','ATM Name','Transaction Date','No Of Withdrawals','No Of CUB Card Withdrawals','No Of Other Card Withdrawals',
		  'class','Amount withdrawn CUB Card','Amount withdrawn Other Card','Rounded Amount Withdrawn'],1,inplace=True)
X=np.array(df.drop('Total amount Withdrawn',1))
X=preprocessing.scale(X)
y=np.array(df['Total amount Withdrawn'])

X_train,X_test,y_train,y_test=cross_validation.train_test_split(X,y,test_size=0.2)
# clf=RandomForestRegressor(n_estimators=5000)	
clf=RandomForestRegressor(max_features=23)	
#these number of trees give us around 25% accuracy and increasing the number of trees doesnt give much change in the accuracy
clf.fit(X_train,y_train)
accuracy=clf.score(X_test,y_test)
print('Accuracy: ',accuracy)

