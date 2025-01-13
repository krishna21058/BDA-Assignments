import json
from tqdm import tqdm

def load_test_data(test_ids_file, test_texts_file):
    with open(test_ids_file, 'r', encoding='utf-8') as file:
        test_ids = [line.strip() for line in file]
    
    with open(test_texts_file, 'r', encoding='utf-8') as file:
        test_texts = [line.strip() for line in tqdm(file, desc="Reading test texts")]

    return test_ids, test_texts

def load_predictions(predictions_file):
    with open(predictions_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def retrieve_top_items(test_ids, predictions):
    top_items = {}
    
    for test_id in tqdm(test_ids, desc="Retrieving top items"):
        top_items[test_id] = predictions.get(test_id, [])[:5]  

    return top_items

def save_top_items(top_items, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(top_items, f, ensure_ascii=False, indent=4)

test_ids, test_texts = load_test_data('test_ids.txt', 'test_texts.txt')
predictions = load_predictions('predictions.json')

top_items = retrieve_top_items(test_ids, predictions)

save_top_items(top_items, 'top_items.json')

print("Top items retrieval completed and saved to top_items.json.")
