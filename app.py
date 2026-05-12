from flask import Flask, render_template, request, session, redirect, url_for
from nlp.query_parser import parse_query
from nlp.recommendation import ProblemRecommender
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "change-me")  # set a real secret in prod

# instantiate recommender with the dataset path
DATA_PATH = os.path.join(os.path.dirname(__file__), "dataset", "leetcode_problems_dataset_extended (2).csv")
recommender = ProblemRecommender(DATA_PATH)


def _add_history(query: str):
    if not query:
        return
    history = session.get("history", [])
    if query in history:
        history.remove(query)
    history.insert(0, query)
    session["history"] = history[:10]


def _add_saved(query: str):
    if not query:
        return
    saved = session.get("saved", [])
    if query not in saved:
        saved.append(query)
        session["saved"] = saved


@app.route("/", methods=["GET"])
def index():
    # prepare options for filter controls
    # build filter options dynamically from categorical columns only
    df = recommender.df
    
    # Exclude descriptive, URL, and ID fields
    excluded_cols = {"id", "problem", "url", "description", "notes", "solution_approach", "time_complexity", "space_complexity", "last_attempted", "confidence_level", "attempts", "_clean_problem"}
    filter_columns = [c for c in df.columns if c not in excluded_cols]
    
    options = {}
    for col in filter_columns:
        # Split comma-separated values (like companies or tags) to build cleaner filter options
        opts_set = set()
        for val in df[col].dropna():
            if isinstance(val, str) and ',' in val:
                opts_set.update([v.strip() for v in val.split(',')])
            else:
                opts_set.add(val)
        options[col] = sorted(list(opts_set))
    history = session.get("history", [])
    saved = session.get("saved", [])
    return render_template(
        "index.html",
        filter_options=options,
        history=history,
        saved=saved,
    )


@app.route("/results", methods=["GET", "POST"])
def results():
    # support GET from history links
    if request.method == "POST":
        form = request.form
    else:
        form = request.args
    query = form.get("query", "")

    _add_history(query)

    # collect filter values from the request (everything except query)
    criteria = {}
    for key, vals in form.lists():
        if key == "query":
            continue
        criteria[key] = vals

    # if no explicit filters, fall back to NLP detection for topic/difficulty
    if not criteria and query:
        detected = parse_query(query)
        criteria = {
            "topic": detected.get("topic"),
            "difficulty": detected.get("difficulty"),
        }

    filtered_df = recommender.filter(**criteria)
    filtered_list = filtered_df.to_dict(orient="records")

    semantic = recommender.recommend_similar(query) if query else []

    # additional suggestions from history (other than current query)
    extra = []
    hist = session.get("history", [])
    for past in hist:
        if past and past.lower() != query.lower():
            recs = recommender.recommend_similar(past)
            for r in recs:
                if r not in semantic and r not in extra:
                    extra.append(r)
            if len(extra) >= 5:
                break
    extra = extra[:5]

    return render_template(
        "results.html",
        query=query,
        topic=criteria.get('topic'),
        difficulty=criteria.get('difficulty'),
        filtered_list=filtered_list,
        semantic=semantic,
        extra=extra,
    )


@app.route("/save", methods=["POST"])
def save_query():
    q = request.form.get("query")
    _add_saved(q)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
