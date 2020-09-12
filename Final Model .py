#!/usr/bin/env python
# coding: utf-8

# Feature Engineering 

# In[31]:


#setting up connection 
import psycopg2
#import pandas as pd
import os
#from config import Config
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import seaborn as sns
from matplotlib import pyplot


# In[2]:


# declare a new PostgreSQL connection object
conn = psycopg2.connect("host=covid19.c9opif8xcrgf.us-east-1.rds.amazonaws.com dbname=covid19 user=covid19 password=covid2019")
folder = os.path.join(os.getcwd(), 'data','COVID19')
print('The Folder is: ' +folder)


# In[5]:


df_state = pd.read_sql('SELECT * FROM csse_covid_19_data_us', conn) #established the connection 


# In[6]:



df_state['Date'], df_state['Time'] = df_state['last_update'].dt.normalize(), df_state['last_update'].dt.time
df_state = df_state.set_index('last_update') #set date index 


# In[ ]:





# In[7]:


start = "2020-01-21" #US pandemic start date 
df_state['BeginPan'] = df_state['Date'] - pd.to_datetime(start)


# In[8]:


df_state['MonthSince'] = df_state['BeginPan'] / 30 #months since andemic started 


# In[9]:


df_state['WeekSince'] = df_state['BeginPan'] /7 #weeks pandemic started 


# In[10]:


dt = pd.to_timedelta(df_state['WeekSince'])
df_state['WeekSince']=df_state['WeekSince'].dt.days
df_state['WeekSince'].value_counts()


# In[11]:


df_state['dailyavgcases'] = df_state.groupby(['WeekSince'])['confirmed'].mean() #created some new features 
df_state['dailyavgdeaths'] = df_state.groupby(['WeekSince'])['deaths'].mean()


# In[12]:


df_state['weeklyavgcases'] = df_state.groupby(['WeekSince'])['confirmed'].mean()
df_state['weeklyavgdeaths'] = df_state.groupby(['WeekSince'])['deaths'].mean()


# In[116]:


df_state['deaths']


# In[13]:


dt = pd.to_timedelta(df_state['MonthSince'])
df_state['MonthSince']=df_state['MonthSince'].dt.days
df_state['MonthSince'].value_counts()


# In[103]:


df_state['monthlyavgcases'] = df_state.groupby(['MonthSince'])['confirmed'].mean()
df_state['monthlyavgdeaths'] = df_state.groupby(['MonthSince'])['deaths'].mean()


# In[15]:


df_state.info()


# In[16]:


df_state['weeklyavgdeaths'].describe() 


# ### Impute Numeric Variables for Machine Learning model.
# The missing data is not at random. We will calculate the median for each state. 

# In[21]:


###impute missing data by state 
from sklearn.impute import SimpleImputer
imr = SimpleImputer(strategy='median')
df_state[['mortality_rate']] = imr.fit_transform(df_state[['mortality_rate']])


#df_state.mortality_rate = bystate_class.mortality_rate.transform(impute_median)


# In[ ]:


imr = SimpleImputer(strategy='median')
df_state[['recovered']] = imr.fit_transform(df_state[['recovered']])


# In[24]:


imr = SimpleImputer(strategy='median')
df_state = imr.fit_transform(df_state)


# In[ ]:


imr = SimpleImputer(strategy='median')
df_state[['people_tested ']] = imr.fit_transform(df_state[['people_tested']])


# In[ ]:


imr = SimpleImputer(strategy='median')
df_state[['incident_rate']] = imr.fit_transform(df_state[['incident_rate']])


# In[22]:


df_state.info()


# ## Correlations 

# In[12]:


sns.heatmap(df_state.corr())


# ## 1d plot

# In[40]:


col = list(df_state.columns)[2:15]
from yellowbrick.features import Rank1D
visualizer = Rank2D(algorithm="pearson", size=(1080, 1080))
visualizer.fit_transform(pd.get_dummies(col))
visualizer.poof()


# In[34]:


col = list(df_state.columns)[2:15]


# ## 2d plot

# In[35]:


from yellowbrick.features import Rank2D
visualizer = Rank2D(algorithm="pearson", size=(1080, 1080))
visualizer.fit_transform(pd.get_dummies(col))
visualizer.poof()


# In[41]:


df_state.head()


# In[106]:


start = "2020-04-12"
df_state['Begin'] = df_state['Date'] - pd.to_datetime(start)
df_state['WeekSince'] = df_state['Begin'] /7
df_state['MonthSince'] = df_state['Begin'] / 30


# In[107]:


dt = pd.to_timedelta(df_state['MonthSince'])
df_state['MonthSince']=df_state['MonthSince'].dt.days
df_state['MonthSince'].value_counts() 


# In[108]:


df_state['monthlyavgdeaths'] = df_state.groupby(['MonthSince'])['deaths'].mean()


# In[110]:


df_state['monthlyavgdeaths']


# In[ ]:


df_state['Date']=pd.to_datetime(df_state['Date'], format='%Y-%m-%d')

date1 = datetime.strptime('2020-04-12’, '%Y-%m-%d')
date2 = datetime.strptime('2020-06-12’, '%Y-%m-%d')

df_state['confirmed2months'] = df_state['confirmed'].loc[(df_state['Date']>date1) & (df_state['Date']<date2)]


# In[105]:


df_state.sort_values(by='Date')


# ## Evaluating Regressors
# 
# Regression models attempt to predict a target in a continuous space. Regressor score visualizers display the instances in model space to better understand how the model is making predictions. 
# 
# ### PredictionError
# 
# A prediction error plot shows the actual targets from the dataset against the predicted values generated by our model. This allows us to see how much variance is in the model. Data scientists can diagnose regression models using this plot by comparing against the 45 degree line, where the prediction exactly matches the model.(from lecture)

# In[86]:


from sklearn.linear_model import Lasso
from yellowbrick.regressor import PredictionError


# Load regression dataset


#Index(['confirmed', 'deaths', 'recovered',
      # 'active', 'incident_rate', 'people_tested', 'people_hospitlized', 'mortality_rate', 'testing_rate', 'hospitalization_rate'],
      #dtype='object')

features = ['confirmed', 'deaths', 'recovered',
       'active', 'incident_rate', 'people_tested', 'people_hospitlized', 'mortality_rate', 'testing_rate', 'hospitalization_rate']

#X = df_state.drop(['mortality_rate'], , axis=1)
X = df_state[features]
y = df_state.loc[:, 'mortality_rate']

imr = SimpleImputer(strategy='median')
X = imr.fit_transform(X)

# Create the train and test data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Instantiate the linear model and visualizer
model = Lasso()
visualizer = PredictionError(model, size=(1080, 720))

visualizer.fit(X_train, y_train)  # Fit the training data to the visualizer
visualizer.score(X_test, y_test)  # Evaluate the model on the test data
visualizer.show()                 # Draw the data


# In[88]:


from sklearn.linear_model import LinearRegression
regr_linear = LinearRegression()


# Load regression dataset


#Index(['confirmed', 'deaths', 'recovered',
      # 'active', 'incident_rate', 'people_tested', 'people_hospitlized', 'mortality_rate', 'testing_rate', 'hospitalization_rate'],
      #dtype='object')

features = ['confirmed', 'deaths', 'recovered',
       'active', 'incident_rate', 'people_tested', 'people_hospitlized', 'testing_rate', 'hospitalization_rate']

#X = df_state.drop(['mortality_rate'], , axis=1)
X = df_state[features]
y = df_state.loc[:, 'mortality_rate']

imr = SimpleImputer(strategy='median')
X = imr.fit_transform(X)

# Create the train and test data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Instantiate the linear model and visualizer
model = LinearRegression()
visualizer = PredictionError(model, size=(1080, 720))

visualizer.fit(X_train, y_train)  # Fit the training data to the visualizer
visualizer.score(X_test, y_test)  # Evaluate the model on the test data
visualizer.show()                 # Draw the data


# In[92]:


from sklearn.linear_model import Ridge


regr_linear = Ridge()


# Load regression dataset


#Index(['confirmed', 'deaths', 'recovered',
      # 'active', 'incident_rate', 'people_tested', 'people_hospitlized', 'mortality_rate', 'testing_rate', 'hospitalization_rate'],
      #dtype='object')

features = ['confirmed', 'deaths', 'recovered',
       'active', 'incident_rate', 'people_tested', 'people_hospitlized', 'testing_rate', 'hospitalization_rate']

#X = df_state.drop(['mortality_rate'], , axis=1)
X = df_state[features]
y = df_state.loc[:, 'mortality_rate']

imr = SimpleImputer(strategy='median')
X = imr.fit_transform(X)

# Create the train and test data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Instantiate the linear model and visualizer
model = Ridge()
visualizer = PredictionError(model, size=(1080, 720))

visualizer.fit(X_train, y_train)  # Fit the training data to the visualizer
visualizer.score(X_test, y_test)  # Evaluate the model on the test data
visualizer.show()                 # Draw the data



# In[93]:


type(X)


# In[ ]:


# Time Series Train Test Split 
from sklearn.model_selection import TimeSeriesSplit

# n-splits determine the number folds. N-1 in this case we split our # data into two sets. (3-1)
tss = TimeSeriesSplit(n_splits = 3)

X = df_state
y = df_state['mortality_rate']

for train_index, test_index in tss.split(X):
    X_train, X_test = X.iloc[train_index, :], X.iloc[test_index,:]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

testLength = len(XTest)
trainCvSplit = [(list(range(trainCvIndices[0],trainCvIndices[-testLength])),
                     list(range(trainCvIndices[-testLength],trainCvIndices[-1]+1)))]


# In[90]:


from sklearn.svm import SVR
from sklearn import svm
clf = svm.SVC(kernel='linear') # Linear Kernel


# Load regression dataset


#Index(['confirmed', 'deaths', 'recovered',
      # 'active', 'incident_rate', 'people_tested', 'people_hospitlized', 'mortality_rate', 'testing_rate', 'hospitalization_rate'],
      #dtype='object')

features = ['confirmed', 'deaths', 'recovered',
       'active', 'incident_rate', 'people_tested', 'people_hospitlized', 'testing_rate', 'hospitalization_rate']

#X = df_state.drop(['mortality_rate'], , axis=1)
X = df_state[features]
y = df_state.loc[:, 'mortality_rate']

imr = SimpleImputer(strategy='median')
X = imr.fit_transform(X)

# Create the train and test data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

#Train the model using the training sets
clf.fit(X_train, y_train)
#Predict the response for test dataset
y_pred = clf.predict(X_test)

          #will work if I classify it 


# In[ ]:


visualizer = PredictionError(model, size=(1080, 720))

visualizer.fit(X_train, y_train)  # Fit the training data to the visualizer
visualizer.score(X_test, y_test)  # Evaluate the model on the test data
visualizer.show()  


# In[48]:





# In[60]:


# Target data START HERE 
y=df_state["mortality_rate"]

# Features data
X=df_state.select_dtypes('float').drop(['mortality_rate'], axis=1, inplace=True)


# In[77]:


# Split the timeseries data
split = TimeSeriesSplit(n_splits=5)

from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
# Fit and score the model with cross-validation
model = LinearRegression().fit(X, y)

scores = cross_val_score( model, X, y, cv=split)


print("R^2 scores of each split:", scores)


# In[36]:


X = df_state.values

for train_index, test_index in tss.split(X):
    X_train, X_test = X[train_index, :], X[test_index,:]
    y_train, y_test = y[train_index], y[test_index]
    
    print("Training indices:", train_index, test_index)
tscv = TimeSeriesSplit(n_splits=5)
print(tscv)
pyplot.figure(1)


# In[33]:


X = df_state.values
tscv = TimeSeriesSplit(n_splits=5)
print(tscv)
pyplot.figure(1)


# In[29]:


data_use = df_state.reset_index()['last_update']

for train_index, test_index in tscv.split(data_use):
  train = data_use[train_index]
  test = data_use[test_index]


# In[30]:


TimeSeriesSplit(max_train_size=None, n_splits=5)


# In[37]:


from sklearn.linear_model import Ridge
from yellowbrick.regressor import ResidualsPlot

# Instantiate the linear model and visualizer
model = Ridge()
visualizer = ResidualsPlot(model, size=(1080, 720))

visualizer.fit(X_train, y_train)  # Fit the training data to the visualizer
visualizer.score(X_test, y_test)  # Evaluate the model on the test data
visualizer.show()                 # Draw the data


# In[38]:


from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import BayesianRidge, LinearRegression

regressors = {
    "support vector machine": SVR(),
    "multilayer perceptron": MLPRegressor(),
    "nearest neighbors": KNeighborsRegressor(),
    "bayesian ridge": BayesianRidge(),
    "linear regression": LinearRegression(),
}

for _, regressor in regressors.items():
    visualizer = ResidualsPlot(regressor)
    visualizer.fit(X_train, y_train)
    visualizer.score(X_test, y_test)
    visualizer.show()


# ### Cross Validation 

# In[126]:


from sklearn.model_selection import cross_val_score
clf = svm.SVC(kernel='linear', C=1)
scores = cross_val_score(clf, X, y, cv=3)


# In[127]:


from sklearn.linear_model import RidgeCV    #this works 
clf = RidgeCV(alphas=[1e-3, 1e-2, 1e-1, 1]).fit(X, y)
clf.score(X, y)


# In[ ]:


#Create TS Cross-Validator
                   my_cv = TimeSeriesSplit(n_splits = TS_splits).split(X_train)


# In[ ]:


scores = cross_val_score(model, X_train, y_train, cv=tscv, scoring=r2)


# In[130]:


from sklearn.model_selection import cross_val_score
ols2 = LinearRegression()
ols_cv_mse = cross_val_score(ols2, X, y, scoring='neg_mean_squared_error', cv=10)
ols_cv_mse.mean()


# In[124]:


from sklearn.linear_model import LassoCV
from sklearn.feature_selection import SelectFromModel

lassocv = LassoCV()
lassocv.fit(X, y)
lassocv_score = lassocv.score(X, y)
lassocv_alpha = lassocv.alpha_
print('CV', lassocv.coef_)


# # Hyperparameter Tuning
# The yellowbrick.model_selection package provides visualizers for inspecting the performance of cross validation and hyper parameter tuning. Many visualizers wrap functionality found in sklearn.model_selection and others build upon it for performing multi-model comparisons.

# In[112]:


# Import necessary modules
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
import numpy as np

# Create train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.40, random_state = 42)

# Create the hyperparameter grid
l1_space = np.linspace(0, 1, 30)
param_grid = {'l1_ratio': l1_space}

# Instantiate the ElasticNet regressor: elastic_net
elastic_net = ElasticNet()

# Setup the GridSearchCV object: gm_cv
gm_cv = GridSearchCV(elastic_net, param_grid, cv=5)

# Fit it to the training data
gm_cv.fit(X_train, y_train)

# Predict on the test set and compute metrics
y_pred = gm_cv.predict(X_test)
r2 = gm_cv.score(X_test, y_test)
mse = mean_squared_error(y_test, y_pred)
print("Tuned ElasticNet l1 ratio: {}".format(gm_cv.best_params_))
print("Tuned ElasticNet R squared: {}".format(r2))
print("Tuned ElasticNet MSE: {}".format(mse))


# In[ ]:




