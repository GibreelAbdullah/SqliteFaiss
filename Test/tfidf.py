from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample dataset
documents = []

file1 = open('./data/data.txt', 'r')
lines = file1.readlines()

line_number = 1
for line in lines:
    print(line_number)
    documents.append(line)

# Create a TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Fit and transform the documents
tfidf_matrix = vectorizer.fit_transform(documents)

# Query: The user's search query
query = "bleeding blood"

# Transform the query using the same vectorizer
query_vector = vectorizer.transform([query])

# Calculate cosine similarity between the query and each document
similarities = cosine_similarity(tfidf_matrix, query_vector)

# Get the index of the most similar document
most_similar_index = similarities.argmax()

# Retrieve the most similar document
most_similar_document = documents[most_similar_index]

# Print the result
print(f"Most similar document: {most_similar_document}")