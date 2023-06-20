class MLModel:
    def __init__(self, model, accuracy_score, confusion_matrix, classification_report) -> None:
        self.model = model
        self.accuracy_score = accuracy_score
        self.confusion_matrix = confusion_matrix
        self.classification_report = classification_report

    