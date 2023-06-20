Tech stack: Flask + Celery + Redis

Simplified version of AA with functionality of train and predict data

Data source: https://raw.githubusercontent.com/jbrownlee/Datasets/master/iris.csv <- currently only work with this dataset or any dataset of the same format
Data format: ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']

ML model: SVC (hard-coded for now)

-----------------------API Design----------------------

API:
POST /train

Request: { "url": {dataset url}}

Response: { "result": {task/model_id} }
=> Initiate Training model with input dataset

GET /model/<task_id>
Response: {
    "ready": true,
    "successful": true
}
=> Check status of model

POST /predict
Request: {
    "model_id": <model_id>,
    "prediction_input": <list_of_datapoint> Sample: [[5.1,3.5,1.4,0.2], [5.1,3.5,1.4,0.2], [6.5,3.2,5.1,2.0]]
}
Response: { "prediction": <list_of_prediction> Sample: ['Iris-setosa' 'Iris-setosa' 'Iris-virginica']}

------------------Flow----------------------------

Flow:
Training: When requested -> we queue task train_ml which train ML model with input data -> the model is trained, dumps to binary with pickle and saved in Redis Broker
Prediction: When requested -> we use model_id to fetch model from Redis -> convert model from binary to model -> use it to predict datapoint -> return result

-------------------------------Tech Stack---------------------------------------

Celery:
- For task queue
- Default number of concurrent task = number of core available

Redis:
- Message Broker + cache

---------------------------Execution------------------------------------

Celery start worker: 
celery -A celeryq.make_celery worker --loglevel INFO --concurrency {number_of_core}

Start server:
python3 api.py
