from flask import request
from flask_restful import Resource, Api
from celeryq.task import train_ml
from celery.result import AsyncResult
from celeryq.make_celery import flask_app, celery_app
from ml import predict

app = flask_app
api = Api(app)

celery_app = celery_app


class MLTrainer(Resource):
    def post(self):
        data_url = request.get_json()["url"]
        result = train_ml.delay(data_url)
        return {"result": result.id}


class Job(Resource):
    def get(self, id):
        result = AsyncResult(id)
        return {
            "ready": result.ready(),
            "successful": result.successful(),
        }


class MLPredict(Resource):
    def post(self):
        model_id = request.get_json()["model_id"]
        predict_input = request.get_json()["prediction_input"]
        task_result = AsyncResult(model_id)
        if task_result.ready():
            model_bin = task_result.result
            result = predict(model_bin, predict_input)
        return {"prediction": result}


api.add_resource(MLTrainer, "/train")
api.add_resource(Job, "/model/<id>")
api.add_resource(MLPredict, "/predict")

if __name__ == '__main__':
    app.run(debug=True)
