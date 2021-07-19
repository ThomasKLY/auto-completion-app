import os

from flask import Flask, jsonify, request
from model import model

app = Flask(__name__)


@app.route('/generate', methods=['POST'])
def hello_world():
    if request.method == 'POST':
        text_input = request.json.get('text')
        model_name = request.json.get('model', 'GPT2-amzReview')
        entry_count = request.json.get('entry_count', 1)
        entry_length = request.json.get('entry_length', 25)
        generated_text = model.generate(model_name, text_input, entry_count=entry_count, entry_length=entry_length)
        return jsonify(generated_text=generated_text), 200


if __name__ == '__main__':
    app.run(debug=True)
