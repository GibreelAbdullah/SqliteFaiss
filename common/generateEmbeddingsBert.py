import torch
from transformers import BertTokenizer, BertModel

def generate_embeddings(sentence):
    # Load tokenizer and model
    model_name = "bert-base-multilingual-uncased"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertModel.from_pretrained(model_name)

    # Tokenize the input sentence
    input_ids = tokenizer.encode(sentence, return_tensors='pt', truncation=True)
    # print(input_ids)
    # Obtain the model embeddings
    with torch.no_grad():
        outputs = model(input_ids)
        embeddings = outputs.last_hidden_state.mean(dim=1)  # Average pooling over the tokens

    return embeddings.tolist()[0]

if __name__ == "__main__":
    generate_embeddings("nn")
