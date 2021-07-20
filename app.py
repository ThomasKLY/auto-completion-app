import os

from flask import Flask, jsonify, request
from model import model

app = Flask(__name__)


@app.route('/generate', methods=['POST'])
def hello_world():
    if request.method == 'POST':
        text_input = request.json.get('text')
        model_name = request.json.get('model', 'GPT2-amzReview')
        num_return_sequences = request.json.get('num_return_sequences', 1)
        max_suggestion_length = request.json.get('max_suggestion_length', 25)
        generated_text = model.generate_text(
            model_name, text_input,
            num_return_sequences=num_return_sequences, max_suggestion_length=max_suggestion_length
        )
        return jsonify(generated_text=generated_text), 200


if __name__ == '__main__':
    app.run(port=5500, debug=True)
