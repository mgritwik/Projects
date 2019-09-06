import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
from xgboost import plot_tree
from sklearn.ensemble import BaggingClassifier
import pandas as pd
import pickle
temp=0
#data=loadtxt('pima-indians-diabetes.data.csv',delimiter=',')
df=pd.read_csv('ClassificationData.csv')
df = df.fillna(method='ffill')
df=df[df['ATM Name']=='Big Street ATM']
y=np.array(df['class'])
df.drop(['ID','ATM Name','Transaction Date','No Of Withdrawals','No Of CUB Card Withdrawals',
		'No Of Other Card Withdrawals','Total amount Withdrawn','Amount withdrawn CUB Card'
		,'Amount withdrawn Other Card','Rounded Amount Withdrawn','class'],1,inplace=True)


X=np.array(df)
X=preprocessing.scale(X)
print('x is: ',X)
#X=preprocessing.scale(X)
#X=data[:,0:8]
#y=data[:,8]

seed=5
test_size=0.33
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=test_size,random_state=seed)

clf=XGBClassifier()
# clf=BaggingClassifier()
clf.fit(X_train,y_train)
with open('xgboostTry.pickle','wb') as f:
	pickle.dump(clf,f)

for i in range(50):
	pickle_in=open('xgboostTry.pickle','rb')
	clf=pickle.load(pickle_in)
	y_pred=clf.predict(X_test)
	predictions=[round(value) for value in y_pred]
	accuracy=accuracy_score(y_test,predictions)
	print(accuracy)
	temp+=accuracy
print('Accuracy is: ',temp*2)	#for 50 training examples * 100 for examples