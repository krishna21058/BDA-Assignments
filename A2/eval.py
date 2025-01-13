import json
import re
import pickle
from tqdm import tqdm
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer  
from datasketch import MinHash

def preprocess_text(text, lemmatize=True, stem=False):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()

    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    words = [word for word in text.split() if word not in stop_words]

    if lemmatize:
        words = [lemmatizer.lemmatize(word) for word in words]
    if stem:
        words = [stemmer.stem(word) for word in words]

    return ' '.join(words)

def text_to_minhash(text, num_perm=128):
    m = MinHash(num_perm=num_perm)
    words = text.split()
    for word in words:
        m.update(word.encode('utf8'))
    return m

def retrieve_top_items(lsh_model, test_ids, test_texts, num_perm=128):
    top_items = {}

    for idx, test_id in enumerate(tqdm(test_ids, desc="Retrieving top items")):
        preprocessed_text = preprocess_text(test_texts[idx])
        minhash = text_to_minhash(preprocessed_text, num_perm=num_perm)

        similar_items = lsh_model.query(minhash)
        top_items[test_id] = similar_items[:5] 

    return top_items

def load_test_data(test_ids_file, test_texts_file):
    with open(test_ids_file, 'r', encoding='utf-8') as file:
        test_ids = [line.strip() for line in file]

    with open(test_texts_file, 'r', encoding='utf-8') as file:
        test_texts = [line.strip() for line in tqdm(file, desc="Reading test texts")]

    return test_ids, test_texts

with open('lsh_model.pkl', 'rb') as f:
    lsh_model = pickle.load(f)

test_ids, test_texts = load_test_data('test_ids.txt', 'test_texts.txt')

top_items = retrieve_top_items(lsh_model, test_ids, test_texts)
#Saving the results
with open('top_items.json', 'w', encoding='utf-8') as f:
    json.dump(top_items, f, ensure_ascii=False, indent=4)

print("Top items retrieval completed and saved to top_items.json.")
