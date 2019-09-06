import pandas as pd
import numpy as np
from sklearn import preprocessing,cross_validation,svm
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import pickle
avg_confidence=0
#functionto convert non numerical data to numerical data
def handle_non_numerical_data(df):
	columns=df.columns.values		#returns all the names of the columns

	for column in columns:
		text_digit_vals={} #dictinary to store the mappings example {'female':0,'male':1}
		def convert_to_int(val):
			return text_digit_vals[val] 	#this returns the value of the int that val has been mapped to
	
		if df[column].dtype!=np.int64 and df[column].dtype!=np.float64:	#if datatype of column is not int/float then:
			column_contents=df[column].values.tolist()					#get all the column contents(all possible values present in the column and form a list)
			#print(column_contents) #to see what is printed
			unique_elements=set(column_contents)						#to get all the unique elements of the above list
			x=0
			for unique in unique_elements:
				if unique not in text_digit_vals:						#if unique not in text value,i,e: if not predefined in the text_didgit_vals list hen define ot right now
					text_digit_vals[unique]=x
					x+=1

			df[column]=list(map(convert_to_int,df[column]))		#inbuilt map functin in pandas to map the values of df[column] to its corresponding convert_to_int function
			#map(aFunction, aSequence) function applies a passed-in function to each item in an iterable object and returns a list containing all the function call results.
	return df


#df=pd.read_csv('processedCUBdata1.csv')
df=pd.read_csv('ClassificationData.csv')
df_AirportAtm=df[df['ATM Name']=='Airport ATM']
#df_AirportAtm.drop(['ATM Name','No Of Withdrawals','Amount withdrawn CUB Card','Amount withdrawn Other Card',
#					'No Of CUB Card Withdrawals','No Of Other Card Withdrawals','Transaction Date'],1,inplace=True)
df_AirportAtm.drop(['ID','ATM Name','Transaction Date','No Of Withdrawals','No Of CUB Card Withdrawals',
		'No Of Other Card Withdrawals','Total amount Withdrawn','Amount withdrawn CUB Card'
		,'Amount withdrawn Other Card','Rounded Amount Withdrawn','class'],1,inplace=True)
df_AirportAtm.replace('?',-99999,inplace=True)
df_AirportAtm.convert_objects(convert_numeric=True)
df_AirportAtm.fillna(-99999, inplace=True)
#df_AirportAtm['Weekday'].str.lower()
#df_AirportAtm=handle_non_numerical_data(df_AirportAtm)
#print(df_AirportAtm.tail())
forecast_col='AvgAmountPerWithdrawal'
#forecast_out = int(math.ceil(0.01 * len(df_AirportAtm)))
forecast_out=30	#predicting 30 days of work before.
df_AirportAtm['label'] = df_AirportAtm[forecast_col].shift(-forecast_out)

X = np.array(df_AirportAtm.drop(['label'], 1))
#poly = PolynomialFeatures(degree=2)
#X = poly.fit_transform(X)
X = preprocessing.scale(X)
X_lately = X[-forecast_out:]
X = X[:-forecast_out]

df_AirportAtm.dropna(inplace=True)

y = np.array(df_AirportAtm['label'])
for  i in range(50):
	print(i)
	X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)


	#these commented lines are commented after training the classifier once,hence forth it just reads
	#from the saved pickle instead of training data
	clf = LinearRegression(n_jobs=-1)
	#svm_regression_model=svm.SVR(kernel='poly')
	#svm_regression_model.fit(X_train,y_train)
	#clf=svm.SVC()#gives lesser confidence, almost 0 everytime
	clf.fit(X_train, y_train)		#synonymous to training the model

	#comment till here after the first time

	#with open('atmDataPredict.pickle','wb') as f:
	#	pickle.dump(clf, f)


	#pickle_in = open('atmDataPredict.pickle','rb')
	#clf = pickle.load(pickle_in)



	confidence = clf.score(X_test, y_test) 		#synonymous to testing the data
	#confidence = svm_regression_model.score(X_test, y_test) 		#synonymous to testing the data

	avg_confidence+=confidence
	#forecast_set = clf.predict(X_lately)

	print(confidence)
print('Avgerage confidence is: ',avg_confidence/50)

