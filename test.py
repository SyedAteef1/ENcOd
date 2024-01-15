# Importing required libraries
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import codecs
# Loading dataset
#dataset = pd.read_csv('amazon_dataset_1.csv')
with codecs.open("amazon_dataset_2.csv", "r",encoding='utf-8', errors='ignore') as file_dat:
     dataset = pd.read_csv(file_dat)
#print(dataset)

# Data preprocessing
dataset = dataset.drop(['DOC_ID', 'PRODUCT_ID', 'PRODUCT_TITLE', 'REVIEW_TITLE'], axis=1)
dataset['LABEL'] = dataset['LABEL'].map({'__label1__': 1, '__label2__': 0})
dataset['VERIFIED_PURCHASE'] = dataset['VERIFIED_PURCHASE'].map({'N': 0, 'Y': 1})
dataset['REVIEW_TEXT'] = dataset['REVIEW_TEXT'].str.lower()

# Splitting dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(dataset.drop('LABEL', axis=1), dataset['LABEL'], test_size=0.2)

# Vectorizing text data
vectorizer = TfidfVectorizer(stop_words='english')
X_train_text = vectorizer.fit_transform(X_train['REVIEW_TEXT'])
X_test_text = vectorizer.transform(X_test['REVIEW_TEXT'])

# Concatenating vectorized text data with other features
X_train_final = pd.concat([X_train.drop('REVIEW_TEXT', axis=1), pd.DataFrame(X_train_text.toarray())], axis=1)
X_test_final = pd.concat([X_test.drop('REVIEW_TEXT', axis=1), pd.DataFrame(X_test_text.toarray())], axis=1)

# Training machine learning model
model = RandomForestClassifier()
model.fit(X_train_final, y_train)

# Testing machine learning model
y_pred = model.predict(X_test_final)
accuracy = accuracy_score(y_test, y_pred)
confusion_matrix = confusion_matrix(y_test, y_pred)
print('Accuracy:', accuracy)
print('Confusion Matrix:', confusion_matrix)

# Prediction for single input review
def predict_review(text, rating, verified_purchase, product_category):
    text = text.lower()
    text_vectorized = vectorizer.transform([text])
    text_final = pd.concat([pd.DataFrame({'RATING': [rating], 'VERIFIED_PURCHASE': [verified_purchase], 'PRODUCT_CATEGORY': [product_category]}), pd.DataFrame(text_vectorized.toarray())], axis=1)
    prediction = model.predict(text_final)[0]
    if prediction == 1:
        return 'Fake review'
    else:
        return 'Real review'
