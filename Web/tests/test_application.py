from application.models import Entry
import datetime as datetime
import pytest
from flask import json
import base64

# Unexpected Failure Testing


@pytest.mark.parametrize("predictionList", [
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.png",
        "vgg16", "fine", 15],
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.png",
        "vgg16", "coarse", 15],
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.png",
        "efficient", "fine", 15],
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.png",
        "efficient", "coarse", 15]
])
# 3: Write the test function pass in the arguments1231
def test_EntryClass(predictionList, capsys):
    with capsys.disabled():
        now = datetime.datetime.utcnow()
        new_entry = Entry(
            user=predictionList[0],
            filePath=predictionList[1],
            modelType=predictionList[2],
            dataType=predictionList[3],
            prediction=predictionList[4],
            predicted_on=now)
        assert new_entry.user == predictionList[0]
        assert new_entry.filePath == predictionList[1]
        assert new_entry.filePath[-4:] == ".png" or new_entry.filePath[-4:
                                                                       ] == ".jpg" or new_entry.filePath[-5:] == ".jpeg"
        assert new_entry.modelType == predictionList[2]
        assert new_entry.modelType == "vgg16" or new_entry.modelType == "efficient"
        assert new_entry.dataType == predictionList[3]
        assert new_entry.dataType == "fine" or new_entry.dataType == "coarse"
        assert new_entry.prediction == predictionList[4]
        if new_entry.dataType == "fine":
            assert new_entry.prediction >= 0 and new_entry.prediction < 100
        else:
            assert new_entry.prediction >= 0 and new_entry.prediction < 20
        assert new_entry.predicted_on == now

# Expected Failure Testing
# What happens if imgPath is invalid
# What happens if modelType is not equal to "vgg16"/"efficient"
# What happens if dataType is not equal to "fine"/"coarse"
# What happens if prediction is outside the range fine[0 - 19] and coarse [0 - 99]


@pytest.mark.xfail(reason="arguments fail due to testing")
@pytest.mark.parametrize("predictionList", [
    # Fail due to invalid file path
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.p",
        "vgg16", "fine", 15],
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.p",
        "efficient", "fine", 15],
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.p",
        "vgg16", "coarse", 15],
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.p",
        "efficient", "coarse", 15],
    # Fail due to modelType not equal to "vgg16"/"efficient"
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.png",
        "1231vgg16", "fine", 15],
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.png",
        "1231efficient", "fine", 15],
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.png",
        "1231vgg16", "coarse", 15],
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.png",
        "1231efficient", "coarse", 15],
    # Fail due to dataType is not equal to "fine"/"coarse"
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.png",
        "vgg16", "1231fine", 15],
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.png",
        "efficient", "1231fine", 15],
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.png",
        "vgg16", "1231coarse", 15],
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.png",
        "efficient", "1231coarse", 15],
    # Fail due to prediction is outside the range fine[0 - 19] and coarse [0 - 99]
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.png",
        "vgg16", "fine", -1],
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.png",
        "efficient", "fine", -1],
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.png",
        "vgg16", "coarse", -1],
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.png",
        "efficient", "coarse", -1],
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.png",
        "vgg16", "fine", 100],
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.png",
        "efficient", "fine", 100],
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.png",
        "vgg16", "coarse", 20],
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.png",
        "efficient", "coarse", 20],
])
def test_EntryValidation(predictionList, capsys):
    test_EntryClass(predictionList, capsys)

# Test Add API


@pytest.mark.parametrize("predictionList", [
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.png",
        "vgg16", "fine", 15],
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.png",
        "vgg16", "coarse", 15],
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.png",
        "efficient", "fine", 15],
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.png",
        "efficient", "coarse", 15]
])
def test_addAPI(client, predictionList, capsys):
    with capsys.disabled():
        # prepare the data into a dictionary
        predictData = {
            "user": predictionList[0],
            "imgPath": predictionList[1],
            "modelType": predictionList[2],
            "dataType": predictionList[3],
            "prediction": predictionList[4],
        }
    response = client.post('/api/add',
                           data=json.dumps(predictData),
                           content_type="application/json",)
    # check the outcome of the action
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response_body = json.loads(response.get_data(as_text=True))
    assert response_body["id"]

# Test get API


@pytest.mark.parametrize("predictionList", [
    [8, 1, "./application/static/images/saved/854316-13930-trout-fish.png",
        "vgg16", "coarse", 1],
    [17, 1, "./application/static/images/saved/951416-23530-chair-household furniture.png",
        "vgg16", "fine", 20],
    [10, 1, "./application/static/images/saved/350882-43714-chimpanzee-large omnivores and herbivores.png",
        "efficient", "coarse", 11],
    [11, 1, "./application/static/images/saved/775114-11802-butterfly-insects.png",
        "efficient", "fine", 14],
])
def test_getAPI(client, predictionList, capsys):
    with capsys.disabled():
        response = client.get(f'/api/get/{predictionList[0]}')
        ret = json.loads(response.get_data(as_text=True))
        # check the outcome of the action
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        response_body = json.loads(response.get_data(as_text=True))
        assert response_body["id"] == predictionList[0]
        assert response_body["user"] == predictionList[1]
        assert response_body["filePath"] == predictionList[2]
        assert response_body["modelType"] == predictionList[3]
        assert response_body["dataType"] == predictionList[4]
        assert response_body["prediction"] == predictionList[5]

# Test delete API


@pytest.mark.parametrize("predictionList", [
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.png",
        "vgg16", "fine", 15],
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.png",
        "vgg16", "coarse", 15],
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.png",
        "efficient", "fine", 15],
    [1, "./application/static/images/saved/001586-11802-butterfly-insects.png",
        "efficient", "coarse", 15]
])
def test_deleteAPI(client, predictionList, capsys):
    with capsys.disabled():
        # prepare the data into a dictionary
        predictData = {
            "user": predictionList[0],
            "imgPath": predictionList[1],
            "modelType": predictionList[2],
            "dataType": predictionList[3],
            "prediction": predictionList[4],
        }
    response = client.post('/api/add',
                           data=json.dumps(predictData),
                           content_type="application/json",)
    response_body = json.loads(response.get_data(as_text=True))
    assert response_body["id"]
    id = response_body["id"]
    response2 = client.get(f'/api/delete/{id}')
    ret = json.loads(response2.get_data(as_text=True))
    # check the outcome of the action
    assert response2.status_code == 200
    assert response2.headers["Content-Type"] == "application/json"
    response2_body = json.loads(response2.get_data(as_text=True))
    assert response2_body["result"] == "ok"

# Consistency Test
# Test Predict API


@pytest.mark.parametrize("bigPredictionList", [
    [[1, "./application/static/images/saved/992451-19607-wolf-large carnivores.png", 
        "vgg16", "fine", 97], 
     [1, "./application/static/images/saved/992451-19607-wolf-large carnivores.png", 
        "vgg16", "fine", 97], 
     [1, "./application/static/images/saved/992451-19607-wolf-large carnivores.png", 
        "vgg16", "fine", 97]
     ],
    [[1, "./application/static/images/saved/854316-13930-trout-fish.png",
        "vgg16", "coarse", 1],
     [1, "./application/static/images/saved/854316-13930-trout-fish.png",
        "vgg16", "coarse", 1],
     [1, "./application/static/images/saved/854316-13930-trout-fish.png",
        "vgg16", "coarse", 1], ],
    [[1, "./application/static/images/saved/775114-11802-butterfly-insects.png", 
        "efficient", "fine", 14], 
     [1, "./application/static/images/saved/775114-11802-butterfly-insects.png", 
        "efficient", "fine", 14], 
     [1, "./application/static/images/saved/775114-11802-butterfly-insects.png", 
        "efficient", "fine", 14]
     ],
    [[1, "./application/static/images/saved/350882-43714-chimpanzee-large omnivores and herbivores.png",
        "efficient", "coarse", 11],
     [1, "./application/static/images/saved/350882-43714-chimpanzee-large omnivores and herbivores.png",
        "efficient", "coarse", 11],
     [1, "./application/static/images/saved/350882-43714-chimpanzee-large omnivores and herbivores.png",
        "efficient", "coarse", 11], ],
])
def test_predictAPI(client, bigPredictionList, capsys):
    predictOutput = []
    for predictionList in bigPredictionList:
        with capsys.disabled():
            with open(predictionList[1], "rb") as f:
                encoded_string = base64.b64encode(f.read()).decode('utf-8')
                encoded_string = "data:image/png;base64," + encoded_string
            predictData = {
                "user": predictionList[0],
                "imageBlob": encoded_string,
                "imageName": predictionList[1].split("/")[-1],
                "model": predictionList[2],
                "dataset": predictionList[3],
                "prediction": predictionList[4],
            }            
            response = client.post('/api/predict',
                                    data=json.dumps(predictData),
                                    content_type="application/json",)
            # check the outcome of the action
            assert response.status_code == 200
            assert response.headers["Content-Type"] == "application/json"
            response_body = json.loads(response.get_data(as_text=True))
            assert response_body["id"]
            predictOutput.append(response_body["prediction"])
        assert len(set(predictOutput)) <= 1
