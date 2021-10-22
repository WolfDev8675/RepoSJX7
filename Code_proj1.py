#!usr/bin/python

''' Board Game Review Project ''' 
# 

#imports 
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plts
import warnings
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression as LR
from sklearn.linear_model import Ridge as R2
from sklearn.linear_model import BayesianRidge as BR2
from sklearn.svm import SVR 
from sklearn.tree import DecisionTreeRegressor as DTR
from sklearn.ensemble import RandomForestRegressor as RFT
from sklearn.metrics import mean_squared_error,mean_absolute_error,median_absolute_error,r2_score

# Presetting viewer 
pd.set_option('display.max_columns', None)

# Loading dataset: data-specs, size and contents
d_set=pd.read_csv("https://raw.githubusercontent.com/WolfDev8675/RepoSJX7/Assign5_1/data/games.csv")
print('x'.center(70,'*'))
print(' Dataset example: \n',d_set.head(20))
print('_'.center(70,'_'))
print('\n\n Content information :: \n');d_set.info();print('_'.center(70,'_'));
print('\n');input('Press any key to continue . . .');print('x'.center(70,'*'))


# Noise and Vaccancy Study 
print(" Noise and vacancy study ");print('_'.center(70,'_'));
print(' Null values per column \n\n',d_set.isnull().sum());print('_'.center(70,'_'))   #8  fields has nulls 
print(' Connection between nulls of various fields:-> [Name] \n',d_set[d_set['name'].notna()].isnull().sum());print('_'.center(70,'_'))
print(""" Connection between nulls of various fields:-> [yearpublished, minplayers, 
        maxplayers, playingtime, minplaytime, maxplaytime, minage] \n""",
      d_set[d_set['yearpublished'].isnull()])
print('_'.center(70,'_'));
print('\n');input('Press any key to continue . . .');print('x'.center(70,'*'))
# ---- conclusion: nulls in name field is solo others are connected 

# Clearing dataset: noise and vaccancy cleaning 
d_set_f0=d_set.dropna(axis='index'); # separately removes 41+3 index lines 
print(' Pre-Cleaning size  : ',d_set.shape);print('_'.center(70,'_'));
print(' Post-Cleaning size : ',d_set_f0.shape);print('_'.center(70,'_'));
print('\n');input('Press any key to continue . . .');print('x'.center(70,'*'))

# Exploration of the data
print(" Exploration of the data ");print('_'.center(70,'_'));
# EDA:#1
print(' Unique values in Dataset : \n',d_set_f0.nunique());print('_'.center(70,'_'));
#  "type" field is purely categorical with only two categories. More exploration gives us the following.
# unique values of 'type' field
print(' Unique values of "type" field : ',d_set_f0['type'].unique());print('_'.center(70,'_'));
# EDA:#2
fig_1=plts.figure(figsize=(13,6.5));fig_1.canvas.set_window_title('EDA plot(1): Average rating histogram')
sns.histplot(d_set_f0['average_rating']);
plts.xlabel('Average Rating');plts.title('Variation of average rating received');
plts.show();
# EDA:#2
print(' Average rating = 0 data header \n',d_set_f0[d_set_f0['average_rating']==0].head());print('_'.center(70,'_'));
print(' Average rating > 0 data header \n',d_set_f0[d_set_f0['average_rating']>0].head());print('_'.center(70,'_'));
# ---- info determined: games with average_rating =0 also has users_rating =0
#           hence all those games that has no average rating has also no users 
#               rating the game and therefore may not be a candidate to analysis
# EDA decision #1 (EDA#1 & EDA#2)
d_set_f1=d_set_f0[d_set_f0['average_rating']>0] # keeping only the games that have at least an average rating 
print(' Dataset size (After EDA decision: #1 ) : ',d_set_f1.shape);print('_'.center(70,'_'));
# EDA:#3
fig_2=plts.figure(figsize=(13,6.5));fig_2.canvas.set_window_title('EDA plot(2): Average rating histogram')
sns.histplot(d_set_f1['average_rating']);
plts.xlabel('Average Rating');plts.title('Variation of average rating received');
plts.show();
# EDA:#4
corr_info=d_set_f1.corr()
fig_3=plts.figure(figsize=(13,4.5));fig_3.canvas.set_window_title('EDA plot(3): Field Correlation information')
sns.heatmap(corr_info,vmax=0.8);plts.xticks(rotation=45,ha='right');
plts.xlabel('Fields');plts.ylabel('Fields');plts.title('Correlation between fields of the dataset ');
plts.show();
# ---- info determined: average rating is the target variable for determination of a game quality.
#            Secondarily, the name, type and id fields have no contribution. 
#               Also bayes rating and publishing year have very low correlation to the determining factors.
print(' Unique values in Dataset : \n',d_set_f1.nunique());print('_'.center(70,'_'));
d_set_f1.sort_values(['average_rating'], ascending=False)[['name','average_rating']].head(10)
d_set_f1.sort_values(['average_rating'], ascending=False)[['name','average_rating']].tail(10)
# EDA decision #2 (EDA#3 & EDA#4)
contributors=[a_column for a_column in d_set_f1.columns.tolist() if a_column not in ['id','name','type','bayes_average_rating','yearpublished']]
affectors='average_rating'
full_X=d_set_f1[contributors].values
full_Y=d_set_f1[affectors].values
print(' Dataset components (After EDA decision: #2 ) : ');print('_'.center(70,'_'));
print(" Independent variables' value set \n",full_X);print('_'.center(70,'_'));
print(" Dependent variable's value set \n",full_Y);print('_'.center(70,'_'));
print('\n');input('Press any key to continue . . .');print('x'.center(70,'*'))

# Visuals of the contributors and affectors
print(" Visualization of the data ");print('_'.center(70,'_')); 
fig_4=plts.figure(figsize=(20,14.5));fig_4.canvas.set_window_title('Visuals plot(1): Visualization scatters of contributing fields ')
pos_counter=1 #preset value for 16 places 4x4 setup 
warnings.filterwarnings('ignore')
plts.title('Comparison of Average rating with other field values ');
plts.tick_params(axis='x',which='both',bottom=False,top=False,labelbottom=False)
plts.tick_params(axis='y',which='both',left=False,right=False,labelleft=False)
plts.gca().spines['left'].set_visible(False)
plts.gca().spines['right'].set_visible(False)
plts.gca().spines['bottom'].set_visible(False)
plts.gca().spines['top'].set_visible(False)
for a_column in contributors:
    fig_4.add_subplot(4,4,pos_counter)
    sns.scatterplot(d_set_f1[a_column],d_set_f1[affectors],alpha=0.5)
    plts.xlabel(a_column);plts.ylabel(affectors);
    pos_counter+=1
plts.show()
print('\n');input('Press any key to continue . . .');print('x'.center(70,'*'))

# Training on Models 
#Part:1 Splitting 
trainX,testX,trainY,testY=train_test_split(full_X,full_Y,test_size=0.21,random_state=52)
print(' Training set size for Independent variables  : ',trainX.shape);print('_'.center(70,'_'));
print(' Training set size for Dependent variables    : ',trainY.shape);print('_'.center(70,'_'));
print(' Testing set size for Independent variables   : ',testX.shape);print('_'.center(70,'_'));
print(' Testing set size for Dependent variables     : ',testY.shape);print('_'.center(70,'_'));
#Part:2 Model Creation (Multiple models)
model_list="""
        Linear Regression         : LR
        Ridge Regression          : R2
        Bayesian Ridge Regression : BR2
        Support Vector Regression : SVR
        Decision Tree Regression  : DTR
        Random Forest Regression  : RFT
        """
print('Creating models for : \n',model_list);print('_'.center(70,'_'));
models={'LR':LR(),'R2':R2(),'BR2':BR2(),'SVR':SVR(),'DTR':DTR(),'RFT':RFT()} #model dictionary
#Part:3 Training Data on Models (Multiple models)
print(' Model Training Status : ')
for key in models:
    models[key].fit(trainX,trainY)
    print("Trained Model : ",key)
print('_'.center(70,'_'));
#Part:4 Prediction tests from the Trained Models
predicts=dict.fromkeys(models.keys())
print(' Prediction Generation Status : ')
for key in models:
    predicts[key]=models[key].predict(testX)
    print('Prediction generated for : ',key)
print('_'.center(70,'_'));
print('\n');input('Press any key to continue . . .');print('x'.center(70,'*'))
#Part:5 Determining accuracy levels of models from the predictions
for key in models:
    print("Score for %s :: "%key,models[key].score(testX,predicts[key]))
print('_'.center(70,'_'));
# Error Study
print("Model\t|\tMean Squared Error\t|\tMean Absolute Error\t|\tRoot Mean Squared Error\t|\tMedian Absolute Error\t|\t\tR\xb2\t\t|\tAdjusted R\xb2");
print('-'.center(200,'-'))
for key in models:
    print(key,mean_squared_error(predicts[key],testY),
          mean_absolute_error(predicts[key],testY),np.sqrt(mean_squared_error(predicts[key],testY)),
          median_absolute_error(predicts[key],testY),r2_score(predicts[key],testY),
          (1-(1-r2_score(predicts[key],testY))*(len(testY)-1)/(len(testY)-testX.shape[1]-1)),sep='\t|\t')
    
print('_'.center(70,'_'));print('\n');input('Press any key to continue . . .');
print('x'.center(70,'*'))
# END OF CODE