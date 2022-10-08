import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import spacy
 
class RoleWordsIDF():
    
    def __init__(self) -> None:
        self.vect = None
    
    def fit(self, DATA, num_words = 20):
        
        nlp = spacy.load('ru_core_news_md', disable=['tagger', 'attribute_ruler', 'senter', 'parser', 'ner'])

        df = pd.DataFrame({'data':DATA})
        data = df.data.apply(nlp)

        def is_alphanum(token):
            return not token.is_punct \
                and not token.is_currency \
                and not token.is_digit \
                and not token.is_punct \
                and not token.is_oov \
                and not token.is_space \
                and not token.is_stop \
                and not token.like_num \
                and not token.pos_ == "PROPN"

        data = data.to_frame() \
            .applymap(lambda x: ' '.join(t.lemma_ for t in x if is_alphanum(t))) \
            .data
        
        self.vect = TfidfVectorizer(norm=None)

        self.vect.fit(data)
        # print(self.vect.get_feature_names_out())
        feature_names = self.vect.get_feature_names_out()
        
        max_value = self.vect.transform(data).max(axis=0).toarray().ravel()
        sorted_by_tfidf = max_value.argsort()

        print("Признаки с наименьшими значениями tfidf")
        print(feature_names[sorted_by_tfidf[:num_words]])
        print("Признаки с наибольшими значениями tfidf")
        print(feature_names[sorted_by_tfidf[-num_words:]])
        
        
        return self
        
    def get_feature_names(self):
        return self.vect.get_feature_names_out()