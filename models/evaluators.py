import logging
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import joblib
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from optuna.trial import FrozenTrial
from sklearn.metrics import classification_report, precision_recall_fscore_support
from sklearn.pipeline import Pipeline

from configs import configs
from data_manager.structure import StructuredData
from utils.utils import ensure_dir, write_json, write_txt


@dataclass
class TransferObject:
    best_model: Pipeline
    best_trial: FrozenTrial
    y_pred: np.ndarray
    y_true: np.ndarray
    label: np.ndarray
    encoding: dict
    meta: pd.DataFrame
    suffix: str


class ArtifactLogger(Protocol):
    def log_params(params: TransferObject):
        ...

    def log_metrics(tobj: TransferObject):
        ...

    def log_artifacts(tobj: TransferObject):
        ...


class Evaluator:
    def __init__(
        self,
        best_model: Pipeline,
        best_trial: FrozenTrial,
        logger: ArtifactLogger,
    ):
        self.best_model = best_model
        self.best_trial = best_trial
        self.logger = logger

    def run(self, data: StructuredData, suffix: str):
        transfer_object = TransferObject(
            best_model=self.best_model,
            best_trial=self.best_trial,
            y_pred=self.best_model.predict(data.data),
            y_true=data.target.encoded.to_numpy(),
            label=data.target.label.to_numpy(),
            encoding=data.target.encoding.to_dict(),
            meta=data.meta,
            suffix=suffix,
        )
        self.logger.log_params(transfer_object)
        self.logger.log_metrics(transfer_object)
        self.logger.log_artifacts(transfer_object)


class ArtifactLoggerClassification:
    def log_params(self, tobj: TransferObject):
        mlflow.log_params(tobj.best_trial.params)
        logging.info(f"Hyperparameters used: {tobj.best_trial.params}")

    def log_metrics(self, tobj: TransferObject):
        precision, recall, f1, _ = precision_recall_fscore_support(
            tobj.y_true, tobj.y_pred, average="weighted", zero_division=0
        )
        mlflow.log_metrics(
            {
                f"{tobj.suffix}_precision": precision,
                f"{tobj.suffix}_recall": recall,
                f"{tobj.suffix}_f1": f1,
            }
        )
        logging.info(
            f"Classification report on {tobj.suffix} data:\n"
            f"{classification_report(tobj.y_true, tobj.y_pred)}"
        )

    def log_artifacts(self, tobj: TransferObject):
        with tempfile.TemporaryDirectory(dir=configs.BASE_DIR) as dp:
            results_path = ensure_dir(Path(dp, configs.MLFLOW_RESULTS, tobj.suffix))
            configs_path = ensure_dir(Path(dp, configs.MLFLOW_CONFIGS))

            write_json(tobj.best_trial.params, configs_path / "best_params.json")
            write_txt(
                classification_report(tobj.y_true, tobj.y_pred),
                results_path / "classification_report.txt",
            )
            # joblib.dump(model_instance, path) # automatically done by mlflow
            mlflow.log_artifacts(dp)
