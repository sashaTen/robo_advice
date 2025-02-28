import numpy as np 
import pandas as pd
import nltk
from typing import Tuple , List, Dict
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score
from zenml import pipeline
from zenml.steps import step
from scipy.sparse import csr_matrix
# Define the pipeline steps
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
@step
def load_df_original_csv() -> pd.DataFrame:
    df = pd.read_csv(r'C:\Users\HP\Desktop\portfolio_app\data\Data.csv',encoding='ISO-8859-1')
    df.dropna(inplace=True)
    df_copy = df.copy()
    df_copy.reset_index(inplace=True)
    return df_copy


@step
def  train_test_split(df_copy:pd.DataFrame) ->  Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    train = df_copy[df_copy['Date'] < '20150101']
    test = df_copy[df_copy['Date'] > '20141231']

    y_train = train['Label']
    train = train.iloc[:, 3:28]
    y_test = test['Label']
    test = test.iloc[:, 3:28]
    return train , y_train ,    test  ,  y_test

@step 
def regex_preprocess(train: pd.DataFrame, test: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    train.replace(to_replace='[^a-zA-Z]', value=' ', regex=True, inplace=True)
    test.replace(to_replace='[^a-zA-Z]', value=' ', regex=True, inplace=True)
    return train ,    test  

@step
def  column_rename(train: pd.DataFrame, test: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    new_columns = [str(i) for i in range(0,25)]
    train.columns = new_columns
    test.columns = new_columns

    for i in new_columns:
        train[i] = train[i].str.lower()
        test[i] = test[i].str.lower()
    
    return train ,    test  



@step
def generate_headlines(train: pd.DataFrame, test: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
    train_headlines = []  
    test_headlines = []   

    for row in range(0, train.shape[0]):
     train_headlines.append(' '.join(str(x) for x in train.iloc[row, 0:25]))

    for row in range(0, test.shape[0]):
     test_headlines.append(' '.join(str(x) for x in test.iloc[row, 0:25]))

    train_headlines   = pd.Series(train_headlines)
    test_headlines   = pd.Series( test_headlines)

    return train_headlines, test_headlines



@step
def apply_porter_stemmer(train_headlines: pd.Series, test_headlines: pd.Series) -> Tuple[pd.Series, pd.Series]:
    """Applies tokenization, stopword removal, and stemming to the headlines."""
    
    ps = PorterStemmer()
    stop_words = set(stopwords.words('english'))  # Load stopwords

    def preprocess_headlines(headlines: pd.Series) -> pd.Series:
        """Tokenizes, removes stopwords, stems words, and joins back into sentences."""
        corpus = []
        for headline in headlines:
            words = headline.split()
            words = [word for word in words if word.lower() not in stop_words]  # Remove stopwords
            words = [ps.stem(word) for word in words]  # Apply stemming
            corpus.append(' '.join(words)) 
          # Reconstruct the headline
        corpus =   pd.Series(corpus)
        return corpus

    # Process train and test headlines
    train_corpus = preprocess_headlines(train_headlines)
    test_corpus = preprocess_headlines(test_headlines)
    
    return train_corpus, test_corpus


@step
def vectorize_text(X_train: pd.Series, X_test: pd.Series) -> Tuple[CountVectorizer,csr_matrix, csr_matrix]:
    vectorizer = CountVectorizer(stop_words='english', max_features=1000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    return vectorizer, X_train_vec, X_test_vec




@step
def  train_model(X_train_vec: csr_matrix, y_train: pd.Series) ->LogisticRegression:
    model = LogisticRegression()
    model.fit(X_train_vec, y_train)
    return model


@step
def train_nb_model(X_train_vec: csr_matrix, y_train: pd.Series) ->MultinomialNB:
    model_nb =  MultinomialNB()
    model_nb.fit(X_train_vec, y_train)
    return  model_nb


@step
def    train_tree(X_train_vec: csr_matrix, y_train: pd.Series) ->DecisionTreeClassifier:
    model_tree =    DecisionTreeClassifier()
    model_tree.fit(X_train_vec ,   y_train)
    return    model_tree



# Step 5: Evaluate the model
@step
def  evaluate_model(model:LogisticRegression, X_test_vec: csr_matrix, y_test: pd.Series  ) ->  float:
    y_pred = model.predict(X_test_vec)
    accuracy = accuracy_score(y_test, y_pred)
    return   accuracy 


@step
def  evaluate_model_nb(model_nb:MultinomialNB, X_test_vec: csr_matrix, y_test: pd.Series  ) ->  float:
    y_pred_nb  =   model_nb.predict(X_test_vec)
    accuracy_nb   =   accuracy_score(y_test, y_pred_nb)
    return   accuracy_nb 



@step
def  evaluate_model_tree(model_tree: DecisionTreeClassifier, X_test_vec: csr_matrix, y_test: pd.Series  ) ->  float:
     y_pred_tree = model_tree.predict(X_test_vec)
     accuracy_tree = accuracy_score(y_test, y_pred_tree)
     return   accuracy_tree


        
 



@pipeline
def sentiment_analysis_pipeline():
    # Load and preprocess data
    df_copy = load_df_original_csv()
    train, y_train, test, y_test = train_test_split(df_copy)
    train, test = regex_preprocess(train, test)
    train, test = column_rename(train, test)
    train_headlines, test_headlines = generate_headlines(train, test)
    train_headlines, test_headlines  = apply_porter_stemmer( train_headlines, test_headlines )
    vectorizer, X_train_vec, X_test_vec   =vectorize_text(train_headlines, test_headlines)
    model  =  train_model( X_train_vec,  y_train)
    model_nb  = train_nb_model( X_train_vec,  y_train)
    model_tree  =  train_tree( X_train_vec,  y_train)
    accuracy =  evaluate_model(model, X_test_vec, y_test)
    accuracy_nb =  evaluate_model_nb(model_nb, X_test_vec, y_test)
    accuracy_tree  =  evaluate_model_tree(model_tree, X_test_vec, y_test)
    




