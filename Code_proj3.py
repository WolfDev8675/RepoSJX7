#!usr/bin/python

'''Predict Rating from Review for E-Commerce Sites'''
# 

# imports 
import nltk
import numpy as np
import pandas as pd
import  matplotlib.pyplot as plt
import seaborn as sns
import warnings as warns
import time 
from copy import deepcopy
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import re
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import confusion_matrix,ConfusionMatrixDisplay
from wordcloud import WordCloud, STOPWORDS
from sklearn.metrics import accuracy_score, classification_report

#primaries
nltk.download('stopwords')
nltk.download('punkt')
pd.set_option('display.max_colwidth', -1)
warns.filterwarnings("ignore")

#import data
data_full=pd.read_csv("https://raw.githubusercontent.com/WolfDev8675/RepoSJX7/Assign5_3/Data/Womens%20Clothing%20E-Commerce%20Reviews.csv")

print(data_full.head())

# Exploration 
#info function
data_full.info()

#description
data_full.describe()

#Size explore
print(" Size of the dataset: ",data_full.shape)

# Nan / Missing Content 
print("Missing Content")
print(data_full.isna().sum())

# Filtering Reviews 
d_set_Filtered=pd.DataFrame(columns=["Clothing ID","Review","Rating","Recommended","Positive Feedback Count"])
d_set_Filtered["Clothing ID"]=data_full["Clothing ID"]
d_set_Filtered["Review"]=data_full["Title"].fillna("")+" "+data_full["Review Text"].dropna()
d_set_Filtered["Rating"]=data_full["Rating"]
d_set_Filtered["Recommended"]=data_full["Recommended IND"]
d_set_Filtered["Positive Feedback Count"]=data_full["Positive Feedback Count"]
print(d_set_Filtered.head())

# finding NANs
print(" NaN checking Filtered Database ")
print(d_set_Filtered.isna().sum())
#Observation : we have the same amount of missing review texts as was in the "data_full" dataframe

# Removing NaN from Reviews
d_set_Filtered.dropna(subset=['Review'],inplace=True)

# Rechecking NAN
print(d_set_Filtered.isna().sum())

#field information
d_set_Filtered.info()

#Size 
print(" Size of the filtered: ",d_set_Filtered.shape)

# Recommendation label distribution
percs=d_set_Filtered.Recommended.value_counts()*100/len(d_set_Filtered.Recommended)
idfs=d_set_Filtered.Recommended.value_counts().index.values
#print(idfs)
fig1=plt.figure(figsize=(13,12));ax1=fig1.add_subplot(111)
ax1.pie(percs,labels=['Recomended [1] ','Not Recomended [0] '],
        autopct='%1.2f%%', textprops={'fontsize': 15});
ax1.legend(['Recomended [1] ','Not Recomended [0] '],fontsize=14);
plt.title("Distribution of Recommendations",fontdict = {'fontsize' : 25})
plt.show()

# Ratings label distribution
percs=d_set_Filtered.Rating.value_counts()*100/len(d_set_Filtered.Rating)
idfs=d_set_Filtered.Rating.value_counts().index.values
#print(idfs)
fig2=plt.figure(figsize=(14,13));ax2=fig2.add_subplot(111)
ax1.pie(percs,labels=[f'\u272D\u272D\u272D\n\u272D\u272D',f'\u272D\u272D\n\u272D\u272D',f'\u272D\u272D\u272D',f'\u272D\u272D',f'\u272D']
        ,autopct='%1.2f%%', textprops={'fontsize': 15});
ax1.legend([f'\u272D\u272D\u272D\n\u272D\u272D\n',f'\u272D\u272D\n\u272D\u272D\n',f'\u272D\u272D\u272D\n',f'\u272D\u272D\n',f'\u272D'],fontsize=14);
plt.title("Distribution of Rating",fontdict = {'fontsize' : 25})
plt.show()

# Word Clouds 
# Recommended Products Reviews 
temp_df = d_set_Filtered[d_set_Filtered.Recommended==1]
words = " ".join(temp_df.Review)
review_words = " ".join([w for w in words.split()
                              if 'http' not in w
                                and not w.startswith('@')
                                and w!='RT'])

wrdcld = WordCloud(stopwords=STOPWORDS,
                  background_color='#EEDEFD',
                  width=2500,
                  height=1000).generate(review_words)
fig3=plt.figure(figsize=(25,10));ax3=fig3.add_subplot(111);
plt.imshow(wrdcld)
plt.axis('off')
plt.title(" Words in Recommended Product Reviews ",fontdict = {'fontsize' : 25})
plt.show()

# Not-Recommended Products Reviews 
temp_df = d_set_Filtered[d_set_Filtered.Recommended==0]
words = " ".join(temp_df.Review)
review_words = " ".join([w for w in words.split()
                              if 'http' not in w
                                and not w.startswith('@')
                                and w!='RT'])

wrdcld = WordCloud(stopwords=STOPWORDS,
                  background_color='#d9a6a6',
                  width=2500,
                  height=1000).generate(review_words)
fig4=plt.figure(figsize=(25,10));ax4=fig4.add_subplot(111);
plt.imshow(wrdcld)
plt.axis('off')
plt.title(" Words in Non-Recommended Product Reviews ",fontdict = {'fontsize' : 25})
plt.show()

# Data Preparation 
# Presets
stops_EN=set(stopwords.words('english'))
#Cleaning Reviews
d_set_Filtered.insert(2,"Cleaned Review",range(d_set_Filtered.shape[0]))
for idx in d_set_Filtered.index:
  Review=d_set_Filtered.Review[idx]
  alph_0=re.sub("[^a-zA-Z]"," ",Review)
  words=alph_0.lower().split();
  cleaned=[word for word in words if word not in stops_EN]
  d_set_Filtered['Cleaned Review'][idx]=' '.join(cleaned)
# Result of cleaning 
print(d_set_Filtered.head())

#Model Creation
#Dataset Fixation 
# Abscissa and Ordinates 
abscissa_primary=d_set_Filtered[['Clothing ID','Cleaned Review','Recommended','Positive Feedback Count']]
ordinate=d_set_Filtered['Rating']
# Vectorizer object
vector=CountVectorizer(analyzer = "word",tokenizer = None,preprocessor = None,stop_words = None,max_features = 5000);
#Review Vectorization 
ReviewFeatures=vector.fit_transform(abscissa_primary['Cleaned Review'])
VectoredReview=pd.DataFrame(ReviewFeatures.toarray())
# splitting
abscissa=deepcopy(abscissa_primary);abscissa.join(VectoredReview);abscissa.drop(labels="Cleaned Review",inplace=True,axis=1)
trainer_X,tester_X,trainer_Y,tester_Y=train_test_split(abscissa, ordinate, test_size=0.2)
 
#Model Class Imports
from sklearn.linear_model import LogisticRegression as LGR
from sklearn.naive_bayes import MultinomialNB as NBS
from sklearn.linear_model import SGDClassifier as SGD
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.tree import DecisionTreeClassifier as DTC
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.svm import SVC 
#Model Creation (Multiple models)
model_list={'LGR':'Logistic Regression',
            'NBS':'Na�ve Bayes',
            'SGD':'Stochastic Gradient Descent',
            'KNN':'K-Nearest Neighbours',
            'DTC':'Decision Tree',
            'RFC':'Random Forest',
            'SVM':'Support Vector Machine'}

print('Creating models for : \n')
for key in model_list: print('\t',model_list[key].ljust(30,' '),' : ',key,sep='  ');
print('_'.center(80,'_'));
models={'LGR':LGR(solver='lbfgs', max_iter=10000),
        'NBS':NBS(),
        'SGD':SGD(),
        'KNN':KNN(n_neighbors = 5),
        'DTC':DTC(),
        'RFC':RFC(n_estimators=200),
        'SVM':SVC(kernel='linear',C=1.0)};
#Training Data on Models (Multiple models)
print(' Model Training Status : ')
for key in models:
    tic=time.perf_counter();
    models[key].fit(trainer_X,trainer_Y)
    toc=time.perf_counter()
    print('\tTrained Model : ',key,f"\t time taken: {toc - tic:0.4f} seconds");
print('_'.center(80,'_'));
#Prediction tests from the Trained Models
predicts=dict.fromkeys(models.keys())
print(' Prediction Generation Status : ')
for key in models:
    tic=time.perf_counter()
    predicts[key]=models[key].predict(tester_X)
    toc=time.perf_counter()
    print('Prediction generated for : ',key,f"\t time taken: {toc - tic:0.4f} seconds");
print('_'.center(80,'_'));
#Accuracy and Classification Reports
accr=dict.fromkeys(models.keys())
for key in models:
    accr[key]=100*accuracy_score(predicts[key],tester_Y)
    print('Metrics for : ',model_list[key])
    print('Accuracy : {:10.4f}%'.format(accr[key]))
    print(classification_report(predicts[key],tester_Y))
    print('_'.center(80,'_'));print('\n\n');
print('*'.center(80,'-'));

#Comparison of Accuracies of Models 
fig4=plt.figure(figsize=(15,6));ax4=fig4.add_subplot(111)
sns.barplot(list(accr.values()),list(range(len(accr))),orient='h');
plt.yticks(range(len(accr)), list(model_list.values()),rotation=0,ha='right',fontsize=15)
plt.title(" Models' Accuracy Comparisons ",fontdict = {'fontsize' : 25});
plt.show()

# Confusion Matrices for the models 
for key in models:
  fig5=plt.figure(figsize=(9,9));ax5=fig5.add_subplot(111);
  confMat=confusion_matrix(predicts[key],tester_Y)
  viewer=ConfusionMatrixDisplay(confMat,display_labels=[1,2,3,4,5]);
  viewer.plot(ax=ax5);
  plt.title(model_list[key],fontdict = {'fontsize' : 25});
  plt.show()

### END OF CODES

##  © Bishal Biswas(@WolfDev8675)
##  (b.biswas_94587@ieee.org)
##**
##**