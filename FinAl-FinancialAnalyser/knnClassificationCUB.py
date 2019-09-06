import numpy as np
from sklearn import preprocessing, cross_validation, neighbors,svm
import pandas as pd
import pickle

avgAccuracy=0
df=pd.read_csv('ClassificationData.csv')
df=df[df['ATM Name']=='Airport ATM']
df.replace('?', -99999, inplace=True)
df.drop(['ID','ATM Name','Transaction Date','No Of Withdrawals','No Of CUB Card Withdrawals',
					'No Of Other Card Withdrawals','Total amount Withdrawn','Amount withdrawn CUB Card',
					'Amount withdrawn Other Card','Rounded Amount Withdrawn'],1,inplace=True)	#removing such unwanted columns is very necessary as they make a
#huge impact on the accuracy of the code as these doent determine the decision of the result

'''
ID,ATM Name,Transaction Date,No Of Withdrawals,No Of CUB Card Withdrawals,No Of Other Card Withdrawals,
Total amount Withdrawn,Amount withdrawn CUB Card,Amount withdrawn Other Card,averageWithdrawals,
Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,WorkingDay,H,N,C,M,NH,HWH,HHW,WWH,WHH,HWW,WWW,WHW,HHH,
Rounded Amount Withdrawn,class
'''

X=np.array(df.drop(['class'],1))
X = preprocessing.scale(X)
y=np.array(df['class'])


X_train,X_test,y_train,y_test=cross_validation.train_test_split(X,y,test_size=0.2)

#a good practise would be to pickle the trained classifer to avoid re training it again and again,
#these are commented out after running for the first time


clf=neighbors.KNeighborsClassifier()
#print(X)
#clf=svm.SVC()
clf.fit(X_train,y_train)




with open('kneighbors.pickle','wb') as f:
	pickle.dump(clf,f)


for i in range(50):
	pickle_in= open('kneighbors.pickle','rb')
	clf=pickle.load(pickle_in)

	accuracy=clf.score(X_test, y_test)
	avgAccuracy+=accuracy
print('Average Accuracy is: ',avgAccuracy/50)


#prediction
'''
test_feature=np.array([[4,2,1,1,1,2,3,2,1],[4,2,2,2,2,2,3,2,1]])
#before the test feature is given for testingit should be rershaped according to size of the test_feature
test_feature=test_feature.reshape(len(test_feature),-1)
prediction=clf.predict(test_feature)
print(prediction)
'''

