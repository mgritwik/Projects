import os
import re
import sys
import datetime
import warnings
import itertools
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
from statsmodels.tsa.stattools import adfuller

#function to convert Non-numerical data to interger,
def convert_to_integer(df):
    
    m_map={'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12}
    columns=df.columns.values       #returns all the names of the columns

    for column in columns:
        if(column!='Month' and column!='date'):
            mappings={} #dictinary to store the mappings example {'female':0,'male':1}
            def mapper(val):
                return mappings[val]    #this returns the value of the int that val has been mapped to
        
            if df[column].dtype!=np.int64 and df[column].dtype!=np.float64: #if datatype of column is not int/float then:
                column_values=set((df[column].values.tolist()))             #get all the column contentime_series(all possible values present in the column and form a list)
                column_values=sorted(column_values)                     
                x=0
                for each in column_values:
                    if each not in mappings:                        #if unique not in text value,i,e: if not predefined in the text_didgit_vals list hen define ot right now
                        mappings[each]=x
                        x+=1

                df[column]=list(map(mapper,df[column]))     # to map the values of df[column] to itime_series corresponding convert_to_int function
        elif column=='Month':
            for i in df.index:
                val=m_map[df.loc[i][column]]
                df.at[i,column]=val
    return df,m_map


df=pd.read_csv('apmc_data_1.csv')



#removal of outliers using box blot

# q1=df['modal_price'].quantile(0.25)
# q3=df['modal_price'].quantile(0.75)
# iqr=q3-q1
# low=q1-1.5*iqr
# high=q3+1.5*iqr
# df=df.loc[(df['modal_price']>low) & (df['modal_price']<high)]

#has to be done initially
# df,month_map=convert_to_integer(df)
# df=df.sort_values(by=['date','Year','Month'],ascending=True)
# df.to_csv('apmc_sorted_dates.csv',sep=',')          #generating a csv file with sorted data awith respect to date column

warnings.filterwarnings("ignore")
#function to check the stationarity of the data
def stationary_check(timeseries):
    
    #Determing rolling statistics
    rolling_smean = timeseries.rolling(12).mean()
    rolling_stddev = timeseries.rolling(12).std()

    #Plot rolling statistics:
    orig = plt.plot(timeseries, color='blue',label='Raw_data')
    mean = plt.plot(rolling_smean, color='green', label='Rolling Mean')
    std = plt.plot(rolling_stddev, color='red', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Standdev and Rolling Mean')
    plt.show()
    
    #Perform Dickey-Fuller test:
    print('Dickey-Fuller Test stats:')
    DFullerTest = adfuller(timeseries, autolag='AIC')
    DFullerOutput = pd.Series(DFullerTest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in DFullerTest[4].items():
        DFullerOutput['Critical Value (%s)'%key] = value
    print(DFullerOutput)


rcParams['figure.figsize'] = 15, 6
data = pd.read_csv('apmc_sorted_dates.csv',)

#For a particular APMC and Commodity
apmc=4  
comm=172
data=data[data['Commodity']==comm]
data=data[data['APMC']==apmc]
data=data[['date','modal_price']]
data.to_csv('apmc_date_price.csv',',')
dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d')
data = pd.read_csv('apmc_date_price.csv', parse_dates=['date'], index_col='date',date_parser=dateparse)
data.drop(['Unnamed: 0'],1,inplace=True)
time_series = data['modal_price']

stationary_check(time_series)

#to remove trends from the data using Exponentially weighted moving average method
time_series_log = np.log(time_series)
moving_avg = time_series_log.rolling(12).mean()	#moving average
plt.plot(time_series_log)
plt.plot(moving_avg, color='red')
plt.show()
time_series_log_moving_avg_diff = time_series_log - moving_avg
time_series_log_moving_avg_diff.head(12)
time_series_log_moving_avg_diff.dropna(inplace=True)
stationary_check(time_series_log_moving_avg_diff)
expwighted_avg = time_series_log.ewm(halflife=12).mean()
plt.plot(time_series_log)
plt.plot(expwighted_avg, color='red')
time_series_log_ewma_diff = time_series_log - expwighted_avg
stationary_check(time_series_log_ewma_diff)
time_series_log_diff = time_series_log - time_series_log.shift()
time_series_log_diff.dropna(inplace=True)
stationary_check(time_series_log_diff)
plt.plot(time_series_log_diff)
plt.show()


#Remove the seasonality from the data
from statsmodels.tsa.seasonal import seasonal_decompose
decomposition = seasonal_decompose(time_series_log,freq=1)
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

trend_list=trend.copy(deep=False)
seasonal_list=seasonal.copy(deep=False)
residual_list=residual.copy(deep=False)
a=np.corrcoef(trend_list.values,seasonal_list.values)
b=np.corrcoef(trend_list.values,residual_list.values)
print('correlation coefficient is: ',np.corrcoef(trend_list.values,seasonal_list.values))
print('correlation coefficient is: ',np.corrcoef(trend_list.values,residual_list.values))

if(a[0][0]!=0 and b[0][0]!=0):          #seasonality is multuplicative if seasonal and residual are dependent on trend
    mod_type='multiplicative'
else:
    mod_type='additive'                 #seasonality is additive if seasonal and residual are independent of trend
print('model type:',mod_type)

#redefining the model with type
decomposition = seasonal_decompose(time_series_log,freq=1,model=mod_type)
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid
plt.subplot(411)
plt.plot(time_series_log, label='Original')
plt.legend(loc='best')
plt.subplot(412)
plt.plot(trend, label='Trend')
plt.legend(loc='best')
plt.subplot(413)
plt.plot(seasonal,label='Seasonality')
plt.legend(loc='best')
plt.subplot(414)
plt.plot(residual, label='Residuals')
plt.legend(loc='best')
plt.tight_layout()
time_series_log_decompose = residual
time_series_log_decompose.dropna(inplace=True)

stationary_check(time_series_log_decompose)
#test the type of Seasonality



#plotting ACF and PACF plots to determine the p,d and q parameters
from statsmodels.tsa.stattools import acf, pacf

lag_acf = acf(time_series_log_diff, nlags=20)
lag_pacf = pacf(time_series_log_diff, nlags=20, method='ols')

#Plot ACF: 
plt.subplot(121) 
plt.plot(lag_acf)
plt.axhline(y=0,linestyle='--',color='gray')
plt.axhline(y=-1.96/np.sqrt(len(time_series_log_diff)),linestyle='--',color='gray')
plt.axhline(y=1.96/np.sqrt(len(time_series_log_diff)),linestyle='--',color='gray')
plt.title('Autocorrelation Function')
#Plot PACF:
plt.subplot(122)
plt.plot(lag_pacf)
plt.axhline(y=0,linestyle='--',color='gray')
plt.axhline(y=-1.96/np.sqrt(len(time_series_log_diff)),linestyle='--',color='gray')
plt.axhline(y=1.96/np.sqrt(len(time_series_log_diff)),linestyle='--',color='gray')
plt.title('Partial Autocorrelation Function')
plt.tight_layout()
plt.show()

p=1
q=1	#by looking at the graph of ACF and PACF for this particular commodity and APMC

#arima model
from statsmodels.tsa.arima_model import ARIMA

p=q=d=range(0,3)
pdq=list(itertools.product(p,d,q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

best_aic = np.inf
best_pdq = None
best_seasonal_pdq = None
tmp_model = None
best_mdl = None
 

 #for verifying the optimality of p,d,q parameters by minimising the AIC from all possible parameters
for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            tmp_mdl = sm.time_seriesa.statespace.SARIMAX(time_series_log,
                                                order = param,
                                                seasonal_order = param_seasonal,
                                                enforce_stationarity=True,
                                                enforce_invertibility=True)
            res = tmp_mdl.fit()
            if res.aic < best_aic:
                best_aic = res.aic
                best_pdq = param
                best_seasonal_pdq = param_seasonal
                best_mdl = tmp_mdl
        except:
            print("Unexpected error:", sys.exc_info()[0])
            continue
print("Best SARIMAX{}x{}12 model - AIC:{}".format(best_pdq, best_seasonal_pdq, best_aic))

# best given by the parametes 0,1,2


mdl = sm.tsa.statespace.SARIMAX(time_series_log,
                                order=(1, 0, 1),
                                seasonal_order=(0, 0, 0, 12),
                                enforce_stationarity=True,
                                enforce_invertibility=True)
# res = mdl.fit()
# # print statistics
# print(res.aic)
# print(res.summary())


# fit model to data
# res = sm.time_seriesa.statespace.SARIMAX(time_series_log,
#                                 order=(1, 1, 0),
#                                 seasonal_order=(1, 2, 1, 12),
#                                 enforce_stationarity=True,
#                                 enforce_invertibility=True).fit()

# # in-sample-prediction and confidence bounds
# pred = res.get_prediction(start=pd.to_datetime('2016-12-01'), 
#                           end=pd.to_datetime('2017-02-01'),
#                           dynamic=True)
# pred_ci = pred.conf_int()

# # plot in-sample-prediction
# ax = time_series_log['2014':].plot(label='Observed',color='#006699');
# pred.predicted_mean.plot(ax=ax, label='One-step Ahead Prediction', alpha=.7, color='#ff0066');

# # draw confidence bound (gray)
# ax.fill_between(pred_ci.index, 
#                 pred_ci.iloc[:, 0], 
#                 pred_ci.iloc[:, 1], color='#ff0066', alpha=.25);

# # style the plot
# ax.fill_betweenx(ax.get_ylim(), pd.to_datetime('2104-09-01'), time_series_log.index[-1], alpha=.15, zorder=-1, color='grey');
# ax.set_xlabel('Date');
# ax.set_ylabel('Passengers');
# plt.legend(loc='upper left');
# plt.savefig('./img/in_sample_pred.png')
# plt.show()


#Arima model wiht the determined parameters. 
model = ARIMA(time_series_log, order=(1, 0, 1))  
resultime_series_ARIMA = model.fit(disp=0)  
plt.plot(time_series_log_diff)
plt.plot(resultime_series_ARIMA.fittedvalues, color='red')
plt.title('RSS: %.4f'% sum((resultime_series_ARIMA.fittedvalues-time_series_log_diff)**2))
plt.show()



#for scaling up the fitted values to the original scale
predictions_ARIMA_diff = pd.Series(resultime_series_ARIMA.fittedvalues, copy=True)
# print(predictions_ARIMA_diff.head())

predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()
# print(predictions_ARIMA_diff_cumsum.head())

predictions_ARIMA_log = pd.Series(time_series_log.ix[0], index=time_series_log.index)
predictions_ARIMA_log = predictions_ARIMA_log.add(predictions_ARIMA_diff_cumsum,fill_value=-0.1)
# print('predictions round off check: ',predictions_ARIMA_log)


predictions_ARIMA = np.exp(predictions_ARIMA_log)
plt.plot(time_series)
print(predictions_ARIMA)
plt.plot(predictions_ARIMA)
plt.title('RMSE: %.4f'% np.sqrt(sum((predictions_ARIMA-time_series)**2)/len(time_series)))
plt.show()



#for forecasting the values of next 3 months		
predictions=list()
history=[x for x in time_series_log]



#fitting the values thrice and adding the values to histoty to forecast the next value
for i in range(0,3):
	model=ARIMA(history,order=(0,1,2))
	resultime_series=model.fit(disp=0)
	output=resultime_series.forecast()
	op=output[0]
	predictions.append(op)
	history.append(op)
print('predictions are: ',predictions)


plt.plot(predictions,color='red')
plt.show()



#scaling up the forecasted values to the original scale
flag=0
predictions_ARIMA_diff = pd.Series(predictions, copy=True)
predictions=pd.Series(predictions)
predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()
predictions_ARIMA_log = pd.Series(time_series_log.ix[0], index=time_series_log.index)
predictions_ARIMA_log = predictions_ARIMA_log.add(predictions_ARIMA_diff_cumsum,fill_value=0)
print('predictions round off check: ',predictions_ARIMA_log)
predictions_scaled_up=list()
for each in predictions_ARIMA_log:
	if(flag<3):
		temp=np.exp(each)
		predictions_scaled_up.append(temp)
		flag+=1
	else:
		break

print('Final prediction(Without scaling up) are: ',predictions)
print('Final predictions(After scaling them): ',predictions_scaled_up)