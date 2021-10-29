#!usr/bin/python

'''Twitter Hate-Speech Combat Project'''
# 

# imports 
import nltk
import numpy as np
import pandas as pd
import  matplotlib.pyplot as plt
import seaborn as sns
import warnings as warns
import time 
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import re
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import confusion_matrix,ConfusionMatrixDisplay
from wordcloud import WordCloud, STOPWORDS
from sklearn.metrics import accuracy_score, classification_report

# Model Class Imports (Multiple Models)
from sklearn.linear_model import LogisticRegression as LGR
from sklearn.naive_bayes import MultinomialNB as NBS
from sklearn.linear_model import SGDClassifier as SGD
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.tree import DecisionTreeClassifier as DTC
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.svm import SVC



# *Primaries

nltk.download('stopwords')
nltk.download('punkt')
pd.set_option('display.max_colwidth', -1)
warns.filterwarnings("ignore")

# import data
trainSet=pd.read_csv("https://github.com/WolfDev8675/RepoSJX7/raw/Assign5_2/Data/train_E6oV3lV.csv")
testSet=pd.read_csv("https://raw.githubusercontent.com/WolfDev8675/RepoSJX7/Assign5_2/Data/test_tweets_anuFYb8.csv")

#Data Display
print(trainSet.head())
print(testSet.head())

# Datatype Information
trainSet.info()
testSet.info()

# Size of datasets

#Train size
print("Size of the training dataset : ", trainSet.shape)

# unlabeled test size
print("Size of the testing dataset : ", testSet.shape)

# Tweet label distribution
percs=trainSet.label.value_counts()*100/len(trainSet.label)
idfs=trainSet.label.value_counts().index.values
fig1=plt.figure(figsize=(9,9));ax1=fig1.add_subplot(111)
ax1.pie(percs,labels=idfs,autopct='%1.2f%%', textprops={'fontsize': 15});
ax1.legend(['Non Hate [0] ','HATE [1] '],fontsize=15);
plt.title("Tweet Label Distribution",fontdict = {'fontsize' : 25})
plt.show()

## So we see that a very low quantity of examples are there (approx: 7%) of the 31962 tweets 
#   that can be termed as Hate Tweets or approximately 2237 tweets convey hatred. 
#       Thus we have fewer examples for our learning algorithms to learn.

# Word Clouds

#   Hatred Set
# Hate speech specific word cloud 
temp_df = trainSet[trainSet.label==1]
words = " ".join(temp_df.tweet)
tweeted_words = " ".join([w for w in words.split()
                              if 'http' not in w
                                and not w.startswith('@')
                                and w!='RT'])

wrdcld = WordCloud(stopwords=STOPWORDS,
                  background_color='black',
                  width=2500,
                  height=1000).generate(tweeted_words)
fig2=plt.figure(figsize=(25,10));ax2=fig2.add_subplot(111); 
plt.imshow(wrdcld)
plt.axis('off')
plt.title(" Hate Words and Contents of Hate tweets ",fontdict = {'fontsize' : 25})
plt.show() 

# Non Hatred Set
# Non-Hate speech specific word cloud 
temp_df = trainSet[trainSet.label==0]
words = " ".join(temp_df.tweet)
tweeted_words = " ".join([w for w in words.split()
                              if 'http' not in w
                                and not w.startswith('@')
                                and w!='RT'])

wrdcld = WordCloud(stopwords=STOPWORDS,
                  background_color='black',
                  width=2500,
                  height=1000).generate(tweeted_words)
fig3=plt.figure(figsize=(25,10));ax3=fig3.add_subplot(111);
plt.imshow(wrdcld)
plt.axis('off')
plt.title(" Contents of Non-Hate tweets ",fontdict = {'fontsize' : 25})
plt.show()

# Data Preparation

# Preset
stops_EN=set(stopwords.words('english'))

# Training Set
trainSet.insert(2,"Cleaned",range(trainSet.shape[0]))
for idx in trainSet.index:
  tweet=trainSet.tweet[idx]
  alph_0=re.sub("[^a-zA-Z]", " ",tweet)
  words=alph_0.lower().split();
  cleaned=[word for word in words if word not in stops_EN]
  trainSet['Cleaned'][idx]=' '.join(cleaned)

# Result of Cleansing
print(trainSet.head())

# Testing Set
testSet.insert(2,"Cleaned",range(testSet.shape[0]))
for idx in testSet.index:
  tweet=testSet.tweet[idx]
  alph_0=re.sub("[^a-zA-Z]", " ",tweet)
  words=alph_0.lower().split();
  cleaned=[word for word in words if word not in stops_EN]
  testSet['Cleaned'][idx]=' '.join(cleaned)

# Result of Cleansing
print(testSet.head())

# **** Model Creation

# ** Trainer & Tester Datasets
# Splitter
# dataset splitting for "trainSet"
trainer_X,tester_X,trainer_Y,tester_Y=train_test_split(trainSet.Cleaned, trainSet.label, test_size=0.2)

# Vectorization
# Vectorizer object
vector=CountVectorizer(analyzer = "word",tokenizer = None,preprocessor = None,stop_words = None,max_features = 5000);
# Trainers # vectorizing trainers
trainerFeatures=vector.fit_transform(trainer_X)
trainerFeatures=trainerFeatures.toarray()
# Testers# vectorizing testers
testerFeatures=vector.fit_transform(tester_X)
testerFeatures=testerFeatures.toarray()

# Classification Models
# Model Creation (Multiple models)
model_list={'LGR':'Logistic Regression',
            'NBS':'Naïve Bayes',
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
    models[key].fit(trainerFeatures,trainer_Y)
    toc=time.perf_counter()
    print('\tTrained Model : ',key,f"\t time taken: {toc - tic:0.4f} seconds");
print('_'.center(80,'_'));

# Model Testing (Multiple Models)

# ^^ Generating Predictions for Tests
#Prediction tests from the Trained Models
predicts=dict.fromkeys(models.keys())
print(' Prediction Generation Status : ')
for key in models:
    tic=time.perf_counter()
    predicts[key]=models[key].predict(testerFeatures)
    toc=time.perf_counter()
    print('Prediction generated for : ',key,f"\t time taken: {toc - tic:0.4f} seconds");
print('_'.center(80,'_'));

# Studying Accuracy and Reports of the Model
accr=dict.fromkeys(models.keys())
for key in models:
    accr[key]=100*accuracy_score(predicts[key],tester_Y)
    print('Metrics for : ',model_list[key])
    print('Accuracy : {:10.4f}%'.format(accr[key]))
    print(classification_report(predicts[key],tester_Y))
    print('_'.center(80,'_'));print('\n\n');
print('*'.center(80,'-'));

# << Comparative Study
# Accuracy Comparisons
#Comparison of Accuracies of Models 
fig4=plt.figure(figsize=(15,6));ax4=fig4.add_subplot(111)
sns.barplot(list(accr.values()),list(range(len(accr))),orient='h');
plt.yticks(range(len(accr)), list(model_list.values()),rotation=0,ha='right',fontsize=15)
plt.title(" Comparison of Accuracies of Models ",fontdict = {'fontsize' : 25});
plt.show()

# Confusion Matrices for the models 
for key in models:
  fig5=plt.figure(figsize=(9,9));ax5=fig5.add_subplot(111);
  confMat=confusion_matrix(predicts[key],tester_Y)
  viewer=ConfusionMatrixDisplay(confMat,display_labels=['Non Hate','Hate']);
  viewer.plot(ax=ax5);
  plt.title(model_list[key],fontdict = {'fontsize' : 25});
  plt.show()

### CONCLUSIVE STUDY 
##as far as visible we have worked on, the models in descending order of their accuracies the top $3$ are 
##1. K-Nearest Neighbour : accuracy at $93.1331\%$
##2. Logistic Regression : accuracy at $91.7879\%$
##3. Stocastic Gradient Descent : accuracy at $89.1287\%$

##If we see carefully the KNN algorithm has many areas of performance better than the others 
#   at the cost of Precision and Recall metrics being quite one-sided, 
#       marking that there may be cases of Over-trained or an Under-trained model besides
#        the time parameters are also to be noted in this situationAlso notable is the fact that
#         the Multinominal Naïve Bayes and Support Vector Machines took majority of the time rather than others.

##*	Logistic Regression took 25.5523 seconds
##*	Naïve Bayes took 3.8908 seconds
##*	Stocastic Gradient descent took 5.0862 seconds
##*	K-Nearest Neighbour took 31.2326 seconds
##*	Decision Trees took 576.5010 seconds
##*	Random Forests took 738.8697 seconds
##*	Support Vector Machine took 2112.6999 seconds

##Moreover if cases are researched we have a lower quantity of hate tweets for the machine to learn properly.
#    Rather suggestive to this is that we may use Cross-Validation in later stages to refine this work. 

##With detailed scrutinization we might choose the Support Vector Machines as a better model inspite of the fact
#    it provides lower accuracy than the KNN marked at a value of $86.6416\%$. 
#       The same also goes for the Random Forests. Inspite of this low accuracy the SVM model
#        has precision and recall values better than the compared models. Now, for SVM models we
#          might need hyperparameter boosting as a further measure to understand the hate-speech 
#          more than the other models. We also conclude about SVM from studies made from the Confusion matrices,
#           showing a tendency to define hate speech more than the other models comparably.
#            Thus showing a promise for better chances in the future if trained, 
#            but this thing also goes for all other models, viz., if given the scope, data,
#             training to the proper limits and weightages of parameters and hyperparameters all
#              models could be equally beter in classifying their forte in spaces the models are 
#              comfortable with or to say working with each model keeping in mind the cons of a model more than the pros.
#               Till then our choice goes to SVM only if took a little less time to train than others.

##On this note mention must be made of the data in the tweets which show that there are words
#    which turn up in both the hate-tweets as well as non-hate ones that, as per a machine, 
#       learning that will obviously confuse it as we people with our brain an deeper understanding of language
#            often fail to understand languages and the information they want to convey.

##** † NOTE: All information and metrics discussed above is subject to change on every execution. 
#       The study made here is purely on the basis of a complete run which took a time of 
#       1 hour and 15 minutes for complete execution. The results so obtained from that execution
#        cycle is used for study and the conclusions drawn. Any values spoken here may not be taken
#         for face value if future executions.**

#### *End Notes*
##After getting success in speech recognition and vision research, natural language processing
#    is the most targeted research area in artificial intelligence.

##Although it is started decades ago, most people lack the NLP experience. 
#   Because it’s hard to teach a machine with the challenges listed below: 
##1. Sarcasm
##2. Ambiguity (Syntactical and Lexical)
##3. Syntax
##4. Co-reference
##5. Typos
##6. Normalization
##7. Puns 

##For a machine running on numbers it is behemoth of a task to make it understand 
#   which even normal people fail to cope up with sometimes owning to large variations
#        languages among us, the sense in which it is spoken, tone of voice, etc., although
#         for tweets a large amount of this problem is overcome due to the size of the tweets
#          and scanability of tweets still a challege is a challenge and as long as people will be there,
#           there will be communication, there will be sentiments involved in communication, there will 
#           difference of opininon which some may take for the face value others may make it a bigger issue, 
#           thus fight for a stand to express the opinion over others, and till the time there will be a rift 
#           in opinion there will be either indifference to some hatred for others. 

##As far as technology goes a platform will always try to supress hatred to maintain an friendly environment
#    than going full on hostile if this hate is allowed to spread. 

#### *Bibliography*
##* https://developer.twitter.com/en/community/success-stories/hatelab
##* https://forward.com/news/352133/twitter-gives-online-hate-speech-its-biggest-platform-why/
##* https://www.convinceandconvert.com/social-media-strategy/twitter-engagement/
##* https://www.lifewire.com/what-exactly-is-twitter-2483331
##* https://www.cfr.org/backgrounder/hate-speech-social-media-global-comparisons
##* https://monkeylearn.com/blog/what-is-natural-language-processing/
##* https://analyticsindiamag.com/7-types-classification-algorithms/
##* https://stackoverflow.com/questions/62658215/convergencewarning-lbfgs-failed-to-converge-status-1-stop-total-no-of-iter
##* https://towardsdatascience.com/do-you-know-how-to-choose-the-right-machine-learning-algorithm-among-7-different-types-295d0b0c7f60
##* https://towardsdatascience.com/nlp-with-spacy-part-1-beginner-guide-to-nlp-4b9460652994
##* https://towardsdatascience.com/the-10bias-and-causality-techniques-of-that-everyone-needs-to-master-6d64dc3a8d68

##&copy;[Bishal Biswas(@WolfDev8675)](https://github.com/WolfDev8675)
##<br>
##*(b.biswas_94587@ieee.org)*