import numpy as np
import pandas as pd
from sklearn import preprocessing,cross_validation
from sklearn.ensemble import GradientBoostingClassifier,BaggingClassifier
import pickle
temp=0

# ID,ATM Name,Transaction Date,No Of Withdrawals,No Of CUB Card Withdrawals,No Of Other Card Withdrawals,Total amount Withdrawn,
# Amount withdrawn CUB Card,Amount withdrawn Other Card,averageWithdrawals,Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,
# WorkingDay,H,N,C,M,NH,HWH,HHW,WWH,WHH,HWW,WWW,WHW,HHH,Rounded Amount Withdrawn,class,AvgAmountPerWithdrawal

df=pd.read_csv('ClassificationData.csv')
df=df[df['ATM Name']=='Airport ATM']
df.drop(['ID','ATM Name','Transaction Date','No Of Withdrawals','No Of CUB Card Withdrawals','No Of Other Card Withdrawals',
		  'Total amount Withdrawn','Amount withdrawn CUB Card','Amount withdrawn Other Card','Rounded Amount Withdrawn'],1,inplace=True)
X=np.array(df.drop('class',1))
X=preprocessing.scale(X)
y=np.array(df['class'])

X_train,X_test,y_train,y_test=cross_validation.train_test_split(X,y,test_size=0.2)


clf=GradientBoostingClassifier()
# clf=BaggingClassifier(n_estimators=100)
clf.fit(X_train,y_train)
with open('gradientBoosting.pickle','wb') as f:
	pickle.dump(clf,f)

for i in range(50):
	pickle_in=open('gradientBoosting.pickle','rb')
	clf=pickle.load(pickle_in)
	accuracy=clf.score(X_test,y_test)
	temp+=accuracy
print("Average Accuracy is: ",temp*2)


