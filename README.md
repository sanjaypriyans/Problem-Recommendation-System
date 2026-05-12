# AI Coding Problem Assistant

This project implements a simple NLP-powered system to help users search and
recommend LeetCode-style coding problems using natural language queries. The
application demonstrates text preprocessing, rule-based query parsing,
semantic recommendation, and a Flask web interface.

## Dataset

The CSV located in `dataset/leetcode_problems.csv` contains the problem
information used by the system. A handful of sample rows are provided but the
file can be extended with real LeetCode data.

## Installation

```bash
python -m pip install -r requirements.txt
python -m nltk.downloader stopwords
```

## Running the App

```bash
python app.py
```

Visit `http://127.0.0.1:5000` and enter queries such as "easy array
problems" or "two sum".

## File Structure

```
project/
│
├── dataset/
│   └── leetcode_problems.csv
│
├── nlp/
│   ├── query_parser.py
│   ├── recommendation.py
│
├── app.py
│
├── templates/
│   ├── index.html
│   └── results.html
│
├── static/
│   └── style.css
│
├── requirements.txt
└── README.md
```

## Project Report

The report is also included in `project_report.md` (see below) or can be used
for the viva presentation.

---

### Project Report Summary

**Abstract:** A short overview explaining the goal to build an NLP-based
system that organizes and recommends coding problems using natural language.

**Introduction:** Discussion of motivation—LeetCode’s tag-based search and the
need for intuitive query understanding.

**Problem Statement:** How to parse user queries into meaningful properties
(topic/difficulty) and provide semantic recommendations.

**Methodology:** Use pandas to load data, nltk for basic preprocessing, a
rule-based parser for topic/difficulty, and sentence-transformers for
semantic similarity.

**System Architecture:** A Python backend with `nlp` modules and a Flask server
delivering HTML templates. Diagram (not shown) would include the flow from the
browser → Flask → query parser & recommender → CSV.

**Results:** The web interface correctly identifies `Topic` & `Difficulty` and
returns filtered lists. Semantic search returns related problem names.

**Conclusion:** Demonstrated a simple but effective NLP assistant for coding
problems, suitable for a college submission.

**Future Work:** Expand parser with ML/NLP, integrate a larger dataset,
add user accounts, or use more sophisticated ranking models.

---

### Viva Explanation (Short)

"When a user types a sentence like \"easy array problems\", the system uses a
small parser that strips punctuation and looks for keywords from a list of
known topics and difficulties. It returns those as detected attributes and then
filters the dataset accordingly. If the user types a specific problem name,
it's preprocessed and turned into an embedding using a sentence-transformer
model (`all-MiniLM-L6-v2`). We compute cosine similarity between the query
embedding and all problem embeddings to recommend similar problems. The web
interface is a simple Flask app with a search form and results rendered via
Jinja templates."
