from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import db, ai_description, imageArr, dataset_description
from tensorflow.keras.preprocessing import image
from application.models import Entry, Quiz
from datetime import datetime
from sqlalchemy import desc
from flask import json, jsonify
import random
from flask_cors import CORS, cross_origin
from PIL import Image, ImageOps
import base64
import requests
import numpy as np
import re
import datetime

main = Blueprint('main', __name__)

# Render Link
url = {
    "coarse": {
        "vgg16": "https://cifar20vgg16.onrender.com/v1/models/Cifar20CustomVGG16:predict",
        "efficient": "https://cifar20efficient.onrender.com/v1/models/Cifar20Efficient:predict"
    },
    "fine": {
        "vgg16": "https://cifar100vgg16.onrender.com/v1/models/Cifar100CustomVGG16:predict",
        "efficient": "https://cifar100efficient.onrender.com/v1/models/Cifar100Efficient:predict"
    }
}

# # Local Link
# url = {
#     "coarse": {
#         "vgg16": "http://localhost:8501/v1/models/Cifar20CustomVGG16:predict",
#         "efficient": "http://localhost:8501/v1/models/Cifar20Efficient:predict"
#     },
#     "fine": {
#         "vgg16": "http://localhost:8501/v1/models/Cifar100CustomVGG16:predict",
#         "efficient": "http://localhost:8501/v1/models/Cifar100Efficient:predict"
#     }
# }


def parseImage(imgData, imageName):
    imgStr = re.search('base64,(.*)', imgData).group(1)
    imgStr = str.encode(imgStr)
    imgPath = f'./application/static/images/saved/{datetime.datetime.now().strftime("%f")}-{imageName}'
    with open(imgPath, 'wb') as output:
        output.write(base64.decodebytes(imgStr))
        output.close()
    im = Image.open(imgPath).convert('RGB')
    im.save(imgPath)
    return imgPath


def make_prediction(instances, model, dataset):
    data = json.dumps({"signature_name": "serving_default", "instances":
                       instances.tolist()})
    headers = {"content-type": "application/json"}
    json_response = requests.post(
        url[dataset][model], data=data, headers=headers)
    predictions = json.loads(json_response.text)['predictions']
    return predictions


@main.route('/')
@main.route('/index')
@main.route('/home')
@login_required
def index():
    number = 10
    random.shuffle(imageArr)
    return render_template("index.html", logIn=current_user, imageArr=imageArr[:number * 2], number=number)


@main.route('/history')
@login_required
def history():
    if request.args.get("id"):
        return render_template('history.html', logIn=current_user, entries=get_entries(current_user), dataset_description=dataset_description, result=get_entry(request.args.get("id")), quiz_entry=get_quiz_entries(current_user))
    return render_template('history.html', logIn=current_user, entries=get_entries(current_user), dataset_description=dataset_description, result=None, quiz_entry=get_quiz_entries(current_user))


@main.route('/quiz', methods=["GET", "POST"])
@login_required
def quiz():
    if request.method == "POST":
        new_quiz = Quiz(
            user=current_user.id,
            modelType=request.json["model"],
            dataType=request.json['dataset'],
            imgs=request.json['imgs'],
            userScore=request.json['userScore'],
            aiScore=request.json['aiScore'],
            quiz_on=datetime.datetime.now())
        new_entryID = add_entry(new_quiz)
        return jsonify({'message': f'success'})
    random.shuffle(imageArr)
    return render_template('quiz.html', imageArr=imageArr, logIn=current_user, dataset_description=dataset_description, ai_description=ai_description)


@main.route('/predict', methods=["GET", "POST"])
@cross_origin()
@login_required
def predict():
    if request.method == "POST":
        imgPath = parseImage(
            request.json["imageBlob"], request.json["imageName"])
        img = image.img_to_array(image.load_img(imgPath,
                                                target_size=(32, 32)))
        img = img.reshape(1, 32, 32, 3)
        prediction = make_prediction(
            img, request.json["model"], request.json['dataset'])
        if not request.json["quiz"]:
            new_entry = Entry(
                user=current_user.id,
                filePath=imgPath,
                modelType=request.json["model"],
                dataType=request.json['dataset'],
                prediction=int(np.argmax(prediction[0])),
                predicted_on=datetime.datetime.now())
            new_entryID = add_entry(new_entry)
            return jsonify({'redirect': f'/history?id={new_entryID}', "prediction": int(np.argmax(prediction[0]))})
        return jsonify({"prediction": int(np.argmax(prediction[0]))})
    random.shuffle(imageArr)
    return render_template("predict.html", logIn=current_user, ai_description=ai_description, dataset_description=dataset_description, imageArr=imageArr)


def add_entry(new_entry):
    try:
        db.session.add(new_entry)
        db.session.commit()
        return new_entry.id
    except Exception as error:
        db.session.rollback()
        flash(error, "danger")
        return 0


def get_entries(user):
    try:
        entries = Entry.query.filter_by(
            user=user.id).order_by(desc(Entry.id)).all()
        print(entries)
        return entries
    except Exception as error:
        db.session.rollback()
        flash(error, "danger")
        return 0


def get_quiz_entries(user):
    try:
        entries = Quiz.query.filter_by(
            user=user.id).order_by(desc(Quiz.id)).all()
        print(entries)
        return entries
    except Exception as error:
        db.session.rollback()
        flash(error, "danger")
        return 0


@main.route('/delete/<id>', methods=['POST'])
def delete(id):
    if request.method == "POST":
        delete_entry(id)
    return redirect(url_for('main.history'))


@main.route('/quiz/delete/<id>', methods=['POST'])
def quiz_delete(id):
    if request.method == "POST":
        delete_quiz(id)
    return redirect(url_for('main.history'))


def get_entry(id):
    try:
        result = Entry.query.get(id)
        return result
    except Exception as error:
        db.session.rollback()
        flash(error, "danger")
        return 0


def delete_entry(id):
    try:
        entry = Entry.query.get(id)
        db.session.delete(entry)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        flash(error, "danger")
        return 0


def delete_quiz(id):
    try:
        entry = Quiz.query.get(id)
        db.session.delete(entry)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        flash(error, "danger")
        return 0

# # API GET ENTRY


@main.route("/api/get/<id>", methods=['GET'])
def api_get(id):
    entry = get_entry(int(id))
    data = {
        "id": entry.id,
        "user": entry.user,
        "filePath": entry.filePath,
        "modelType": entry.modelType,
        "dataType": entry.dataType,
        "prediction": entry.prediction
    }
    result = jsonify(data)
    return result

# API DELETE ENTRY


@main.route('/api/delete/<id>', methods=['GET'])
def api_delete(id):
    if request.method == "GET":
        delete_entry(id)
    return jsonify({'result': 'ok'})

# API ADD


@main.route("/api/add", methods=['POST'])
def api_add():
    # retrieve the json file posted from client
    data = request.get_json()
    # retrieve each field from the data
    user = data['user']
    imgPath = data["imgPath"]
    if imgPath[-4:] != ".png" and imgPath[-4:] != ".jpg" and imgPath[-5:] == ".jpeg":
        return 'bad request!', 400
    modelType = data["modelType"]
    if modelType != "vgg16" and modelType != "efficient":
        return 'bad request!', 400

    dataType = data["dataType"]

    if dataType != "fine" and dataType != "coarse":
        return 'bad request!', 400

    prediction = data['prediction']

    if dataType == "fine":
        if not (prediction >= 0 and prediction < 100):
            return 'bad request!', 400
    else:
        if not (prediction >= 0 and prediction < 20):
            return 'bad request!', 400

    # create an Entry object store all data for db action
    new_entry = Entry(
        user=user,
        filePath=imgPath,
        modelType=modelType,
        dataType=dataType,
        prediction=int(prediction),
        predicted_on=datetime.datetime.now())
    # invoke the add entry function to add entry
    result = add_entry(new_entry)
    # return the result of the db action
    return jsonify({'id': result})

# API Predict Endpoint to test AI Model


@main.route("/api/predict", methods=['POST'])
def api_predict():
    data = request.get_json()
    imgPath = parseImage(
        data["imageBlob"], data["imageName"])
    img = image.img_to_array(image.load_img(imgPath,
                                            target_size=(32, 32)))
    img = img.reshape(1, 32, 32, 3)
    prediction = make_prediction(
        img, data["model"], data['dataset'])

    new_entry = Entry(
        user=data["user"],
        filePath=imgPath,
        modelType=data["model"],
        dataType=data['dataset'],
        prediction=int(np.argmax(prediction[0])),
        predicted_on=datetime.datetime.now())

    result = add_entry(new_entry)
    return jsonify({'id': result, "prediction": int(np.argmax(prediction[0]))})
