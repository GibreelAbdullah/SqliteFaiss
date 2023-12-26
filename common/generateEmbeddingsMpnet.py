from sentence_transformers import SentenceTransformer

def generate_embeddings(sentence):
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
    return model.encode(sentence).tolist()

if __name__ == "__main__":
    print(generate_embeddings("nn"))
