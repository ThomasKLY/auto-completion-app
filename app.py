import os

from flask import Flask, jsonify, request, render_template
from flask.json import JSONEncoder
from model import model

from bson import json_util, ObjectId
from datetime import datetime, timedelta

import db


class MongoJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)


app = Flask(__name__)
app.json_encoder = MongoJsonEncoder


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
        return jsonify(results=response)


@app.route('/remote')
def remote():
    return render_template("remote.html")


@app.route('/review')
def review():
    return render_template("review.html")


@app.route('/models', methods=['POST'])
def models():
    model_name = request.json.get('name')
    result = db.add_model(model_name)
    if not result.acknowledged:
        return jsonify(error='Failed to add model'), 400
    return jsonify(id=result.inserted_id), 201


@app.route('/models/<model_id>')
def models_with_id(model_id):
    result = db.get_model(model_id)
    if result is None:
        return jsonify(error='Model not found'), 404
    return jsonify(result), 200


if __name__ == '__main__':
    app.run()
