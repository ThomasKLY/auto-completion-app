import os

from flask import Flask, jsonify, request, render_template
from model import model

app = Flask(__name__)


@app.route('/generate', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
        text_input = request.args.get('term')
        print(text_input)
        generated_text = model.generate_text(
            'GPT2-amzReview', text_input
        )
        print(generated_text)
        return jsonify([
                {'id': idx, 'value': text, 'label': text} for idx, text in enumerate(generated_text)
            ])
    if request.method == 'POST':
        text_input = request.json.get('text')
        model_name = request.json.get('model', 'GPT2-amzReview')
        num_return_sequences = request.json.get('num_return_sequences', 1)
        max_suggestion_length = request.json.get('max_suggestion_length', 25)
        generated_text = model.generate_text(
            model_name, text_input,
            num_return_sequences=num_return_sequences, max_suggestion_length=max_suggestion_length
        )
        response = [{'label': f'choice{i}', 'value': val} for i, val in enumerate(generated_text)]
        return response


@app.route('/remote')
def remote():
    return render_template("remote.html")


@app.route('/review')
def review():
    return render_template("review.html")


if __name__ == '__main__':
    app.run()
