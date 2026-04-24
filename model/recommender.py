import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Recommender:
    def __init__(self, data_path):
        self.df = pd.read_excel(data_path)
        self.df.fillna('', inplace=True)

        # Combine features
        self.df['content'] = (
            self.df['name'] + " " +
            self.df['category'] + " " +
            self.df['description']
        )

        # TF-IDF Vectorization
        self.tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = self.tfidf.fit_transform(self.df['content'])

        # Similarity Matrix
        self.similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    def recommend(self, product_name, top_n=10):
        product_name = product_name.lower()

        if product_name not in self.df['name'].values:
            return pd.DataFrame()

        idx = self.df[self.df['name'] == product_name].index[0]

        scores = list(enumerate(self.similarity_matrix[idx]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:top_n+1]

        product_indices = [i[0] for i in scores]
        return self.df.iloc[product_indices]