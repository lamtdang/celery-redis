from celery import shared_task
from model.MLModel import MLModel
from ml import train_model, predict


@shared_task(ignore_result=False)
def train_ml(data_source: str) -> bytes:
    return train_model(data_source=data_source)