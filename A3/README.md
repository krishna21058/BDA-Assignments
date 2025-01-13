# Task Overview

Using the provided data, you are required to create a citation graph in Neo4j where:
- **Nodes** represent **papers**.
- **Edges** represent **citation relationships** between papers.

## Steps to Follow

1. **Graph Construction:**
   - Each row in the dataset has a field `"paper"`, which corresponds to the node ID of the citing paper.
   - The `"reference"` field contains a list of node IDs of the cited papers.
   - You will need to create **directed edges** from the citing paper to the cited papers for every row in the dataset.
   - If the `"reference"` list is empty, you **do not create any edges** but still need to keep the citing paper as a node.

2. **SimRank Algorithm:**
   - Once the graph is constructed in Neo4j, you need to run the **SimRank** algorithm to measure the similarity between nodes.
   - Use **Apache Spark** to run the SimRank algorithm on the citation graph.

3. **Query Nodes:**
   - For this task, the given **query node IDs** are:
     - `2982615777`
     - `1556418098`
   - Report the **most similar nodes** with respect to these query nodes.

4. **Run SimRank with Three Different Values of C:**
   - Run the SimRank algorithm three times with different values of **C**: `{0.7, 0.8, 0.9}`.
   - Report the results for each run and analyze the impact of changing the value of **C** on the similarity results.

## Expected Outcome

- A **citation graph** in Neo4j.
- Results of the **SimRank** algorithm for each query node with different values of **C**.
- A comparison of the similarity results across the different values of **C**.
