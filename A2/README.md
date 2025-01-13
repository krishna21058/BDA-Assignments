# Assignment Overview

In this assignment where you are required to implement Locality Sensitive Hashing (LSH) to mimic a given hash map, `items.json`, that maps each data sample to its 5 most similar samples. You can use any existing LSH implementation or code your own.

### Files Provided:
You will be given the following three files:
1. **ids.txt** — each line corresponds to the ID of a particular data sample.
2. **texts.txt** — each line corresponds to the text of a particular data sample.
3. **items.json** — contains a hash map relating a particular data sample to its 5 most similar data samples.

### Task:
Your task is to mimic this hash map using LSH as a core component of your model. The main objective is to generate a file that is much closer to the ground truth file `items.json`. Here's how you'll approach this:

1. **Model Design:** 
    - Your model should classify, predict, or retrieve the top 5 most similar items for each data sample.
    - The performance of the model will be evaluated based on the intersection score between your predicted top 5 items and the actual ground truth top 5 items in `items.json`. 
    - The intersection score will range from 0 to 5 based on how many of the top 5 items your model correctly identifies.

2. **Evaluation:**
    - Take the intersection score for each data sample and calculate the average intersection score over all the samples. The final score will also be in the range of (0, 5).

3. **Plotting and Statistical Analysis:**
    - Plot a histogram and a box plot of the intersection scores.
    - Use `pandas.describe()` to generate statistics of the list of intersection scores for better insights into the model’s performance.

### Test Files:
During evaluation, you will be provided with **test_ids.txt** and **test_texts.txt**. These files will contain the IDs and texts of data samples for which you need to retrieve the top 5 items from the given `ids.txt` and `texts.txt` files.

**Note:** Design your model to work with the test files accordingly.

### Key Points:
- **Intersection Score:** Calculate how many items your model correctly identifies from the top 5 predictions compared to the ground truth.
- **Metrics:** Average intersection score over all data samples.
- **Visualizations:** Plot a histogram and box plot of the intersection scores.
