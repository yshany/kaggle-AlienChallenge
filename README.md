# kaggle-AlienChallenge
https://www.kaggle.com/c/the-allen-ai-science-challenge


### Question data can be foud here:
http://data.allenai.org/ai2-science-questions/ \
http://data.allenai.org/arc/

### dependency:
data collecting: scrapy, bs4, pdfminer6\
data processing:pandas,numpy\
text processing,indexing and scoring: nltk, pylucene(http://lucene.apache.org/pylucene/) \
modeling: xgboost

### text data source:
#### pdf textbook: 
ck12.org\
openstack.org
#### study card:
quizlet.com\
studystack.com
#### wikipedia:
all simiplewiki corpus\
about 2000 science tag in wikipeida \

1. collect all the data in txt folder
2.run textprocessing
3.run luence indexing and scoring
4.use xgb make final model
