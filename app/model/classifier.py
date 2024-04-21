import pickle
from .preprocess import preprocess_item


class HTTPRequestClassifier:
    def __init__(self, weights_path):
        with open(weights_path, 'rb') as f:
            self.clf = pickle.load(f)

    def __call__(self, sample):
        features = preprocess_item(sample)
        label = self.clf.predict(features)[0].item()
        return label
