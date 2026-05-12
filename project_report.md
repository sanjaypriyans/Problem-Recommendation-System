# Project Report: AI Coding Problem Assistant

## Abstract

This project presents an intelligent assistant for searching and recommending
coding problems similar to those found on platforms like LeetCode. Using a
combination of basic NLP for query understanding and semantic embeddings for
recommendation, the system accepts natural language queries and returns
relevant problems categorized by topic and difficulty.

## Introduction

With the proliferation of coding practice platforms, students often face
difficulty in locating problems that match their desired topic or difficulty
level. Traditional tag-based browsing requires manual selection of filters. The
AI Coding Problem Assistant aims to provide a more natural interface where a
user can simply type a phrase such as "easy graph questions" and receive
appropriate results.

## Problem Statement

Design a system that can:

* Parse free-form user queries to detect problem topic (Array, Graph, Dynamic
  Programming, etc.) and difficulty (Easy, Medium, Hard).
* Filter a dataset of problems according to these attributes.
* Further recommend problems semantically similar to a query string, even if
  it does not explicitly mention a topic or difficulty.

## Methodology

1. **Dataset loading:** Utilized `pandas` to read a CSV file (`leetcode_problems.csv`) containing problem id, name, topic, and difficulty.
2. **Text preprocessing:** Employed `nltk` to remove stopwords and punctuation and lowercase strings.
3. **Query parsing:** Implemented a rule-based parser (`nlp/query_parser.py`) that matches lowercased query tokens against a small dictionary of known topics and difficulties.
4. **Filtering:** After parsing, the dataset is filtered using simple dataframe operations.
5. **Semantic recommendation:** Used the `sentence-transformers` library with the `all-MiniLM-L6-v2` model to compute embeddings for problem names and incoming query text; similarity measured via cosine similarity with `scikit-learn`.
6. **Web interface:** Built a Flask application (`app.py`) with two routes: one for the homepage with a search form and another for displaying results with detected attributes and recommendation lists.

## System Architecture

The architecture is straightforward:

```
Browser (search query)
    |
Flask server (/ app.py)
    |-- parse_query (nlp/query_parser.py)
    |-- ProblemRecommender (nlp/recommendation.py)
    |      -- loads CSV
    |      -- preprocess + embeddings
    |      -- filter & recommend
    |
Templates render results (index.html / results.html)
```

A diagram could illustrate this flow with arrows between components.

## Results

After deploying locally and entering queries, the system reliably identifies
expected topics and difficulty levels. Filtered results match the dataset and
semantic suggestions return related problem names even when only partial
phrases are given. The interface is minimal but functional.

## Conclusion

The AI Coding Problem Assistant satisfies the project goal of demonstrating
natural language query understanding and recommendation in a simple,
undergraduate-friendly implementation. It showcases the key areas of NLP,
recommendation systems, and web development.

## Future Work

Possible enhancements include:

* Expanding the query parser with machine learning or more robust NLP
  techniques (e.g., named entity recognition).
* Incorporating a larger dataset with tags and descriptions.
* Allowing multi-criteria filtering and advanced search options.
* Adding user accounts, history tracking, or personalized recommendations.
* Deploying the app on a cloud service or Docker container.
