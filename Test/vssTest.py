from transformers import  BertTokenizerFast, BertModel
tokenizer =  BertTokenizerFast.from_pretrained('bert-base-multilingual-cased')
model = BertModel.from_pretrained("bert-base-multilingual-cased")
text = "Allah is King"
encoded_input = tokenizer(text, return_tensors='pt')
# print(encoded_input)
output = model(**encoded_input)
print(output[0])