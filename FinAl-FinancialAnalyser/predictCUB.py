import pandas as pd
import numpy as np
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


if day not in holidays:
	working_day=1

df1=pd.read_csv('AggregatedData2.csv')
# print(df.head())


# print(df1.head())
atm_name_list=set((df1['ATM Name'].tolist()))
day_list=set((df1['Weekday'].tolist()))
festival_religion_list=set((df1['Festival Religion'].tolist()))
holiday_sequence_list=set((df1['Holiday Sequence'].tolist()))
list_of_lists=[atm_name_list,day_list,festival_religion_list,holiday_sequence_list]
# print(list_of_lists)

predict_query=np.zeros(shape=(1,22))
# print(day_list)


#prediction error
# Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,
# WorkingDay,H,N,C,M,NH,HWH,HHW,WWH,WHH,HWW,WWW,WHW,HHH,averageWithdrawals,AvgAmountPerWithdrawal
#for christ college atm: 
#5,Christ College ATM,2011-1-1,74,25,49,287700,148200,139500,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,74,3887,300000,6
#5,Christ College ATM,2011-1-1,74,25,49,287700,148200,139500,saturday,C,H,WHH,3887



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


# print('predict_query: ',predict_query)
# # print('df: ', df.head(1))
# arr=np.array(df.head(1))
# print('**'*20)
# print(arr)

# 1,Big Street ATM,2011-1-1,50,20,30,123800,41700,82100,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,73,2476,150000,3
df=df[df['ATM Name']==atm_name]
print('predict_query: ',predict_query)
print("@"*20)
arr=np.array(df.head(10))
print('df.head: ',arr)
print("@"*20)
# print('df.index: ',df.index)
# print(predict_query.shape[1])
#search the df.index till the matched string is found


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


# for i in df.index:
# 	df_index=1
# 	predict_query_index=0
# 	bool_value=True
# 	while predict_query_index<21 and bool_value==True:
# 		bool_value=False
# 		# print(df_index,predict_query_index)
# 		# print('df.iloc[i][df_index]: ',df.iloc[i][df_index])
# 		# print('#'*30)
# 		# print('predict_query[0,predict_query_index]: ',predict_query[0,predict_query_index])
# 		# if int(df.iloc[i][df_index])==int(predict_query[0,predict_query_index]):
# 		# 	df_index+=1
# 		# 	print('*'*30)
# 		# 	print('df_index: ',df_index)
# 		# 	print('!'*30)
# 		# 	predict_query_index+=1
# 		# 	print('predict_query_index: ',predict_query_index)
# 			# bool_value=True

# 		#testing
# 		print('predict_query: ',predict_query[0,predict_query_index])
# 		print('df: ',df.iloc[i][df_index])
# 		predict_query_index+=1
# 		df_index+=1


	# if predict_query_index==21:
	# 	print('hellllllloooooooooooooooooooooo')
	# 	print(df_index,predict_query_index)
	# 	predict_query[0,21]=int(df.iloc[df_index])
	# 	predict_query[0,(22)]=int(df.iloc[(df_index+1)])

		# break

# print(predict_query)