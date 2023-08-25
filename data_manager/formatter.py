import pandas as pd

from data_manager.loaders import StructuredData, Target


class ClassificationFormatter:
    def __init__(self, labels_to_encode):
        self.labels_to_encode = labels_to_encode

    def format(self, data: StructuredData) -> StructuredData:
        # create one column labels from multiple columns
        label = data.meta[self.labels_to_encode].apply(tuple, axis=1)
        # encode to numbers
        encoded, encoding = pd.factorize(label)
        encoded = pd.Series(encoded, name="label")
        encoding = pd.Series(encoding, name="encoding")
        data.target = Target(label, encoded, encoding)
        return data
