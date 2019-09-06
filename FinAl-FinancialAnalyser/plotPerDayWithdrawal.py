import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')

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


df=pd.read_csv('AggregatedData2.csv')

df=handle_non_numerical_data(df)
print(df.head())
df=df[df['ATM Name']==3]
x_axis=df['Weekday'].values.tolist()
y_axis=df['AvgAmountPerWithdrawal'].values.tolist()

# print('X max: ',x_axis)
# print('x min: ',y_axis)
#  for i in range(len(x_axis)):
#  	plt.plot(x_axis[i], y_axis[i],color='r', markersize=10)
plt.scatter(x_axis, y_axis, marker='x', s=2,linewidths=5)
plt.xlabel('DAY')
plt.ylabel('Average amount withdrwrawn per day')
plt.show()
# xmax=max(x_axis)
# xmin=min(y_axis)
##scatter plot the x and y and see
#print(column_contents)

#dates=matplotlib.dates.date2num(column_contents)
#matplotlib.pyplot.plot_date(dates,values)
#print(column_contents)

