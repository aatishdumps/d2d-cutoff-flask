from flask import Flask, render_template, request, jsonify
import pandas as pd
from pathlib import Path

app = Flask(__name__)
cutoff_file = Path(__file__).resolve().parent / 'cutoff_list.csv'

@app.route('/')
def index():
    df = pd.read_csv(cutoff_file)
    categories = df['CATEGORY'].unique()
    cutoff_table = df.to_dict(orient='records')
    return render_template('index.html', table=cutoff_table, categories=categories)

@app.route('/filter', methods=['POST'])
def filter():
    rank = int(request.form['rank'])
    selected_categories = request.form.getlist('category[]')
    selected_types = request.form.getlist('type[]')
    df = pd.read_csv(cutoff_file)
    eligible_df = df[(df['OPENING'] <= rank) & (df['CLOSING'] >= rank)]
    if selected_categories:
        eligible_df = eligible_df[eligible_df['CATEGORY'].isin(selected_categories)]
    if selected_types:
        eligible_df = eligible_df[eligible_df['TYPE'].isin(selected_types)]
    result = eligible_df.to_dict(orient='records')
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
