import logging
from abc import ABC, abstractmethod

import pandas as pd

from configs import configs
from configs.parser import FormatterConfig, GeneralConfig
from data_structures.schemas import ClassificationTarget, RegressionTarget, StructuredData


class Formatter(ABC):
    @abstractmethod
    def __init__(self, general_cfg: GeneralConfig, formatter_cfg: FormatterConfig):
        pass

    @abstractmethod
    def format(self, data: StructuredData) -> StructuredData:
        pass

    def _filter_data(self, data: StructuredData) -> StructuredData:
        # keep only rows where the date, treatment and varieties are defined in the toml config
        # note: date and treatment filtered before, so only varieties are filtered here
        indices = data.meta.index[
            data.meta[configs.VARIETY_ENG].isin(self.general_cfg.varieties)
            & data.meta[configs.TREATMENT_ENG].isin(self.general_cfg.treatments)
            & data.meta[configs.DATE_ENG].isin(self.general_cfg.dates)
        ].to_list()
        return data[indices].reset_index()


class ClassificationFormatter(Formatter):
    def __init__(self, general_cfg: GeneralConfig, formatter_cfg: FormatterConfig):
        self.general_cfg = general_cfg
        self.formatter_cfg = formatter_cfg

    def format(self, data: StructuredData) -> StructuredData:
        # keep only varieties defined in the toml config
        data = self._filter_data(data)

        # create one column labels from multiple columns
        label = data.meta[self.formatter_cfg.classification_labels].apply(tuple, axis=1)
        # encode to numbers
        encoded, encoding = pd.factorize(label)
        encoded = pd.Series(encoded, name="encoded")
        encoding = pd.Series(encoding, name="encoding")
        data.target = ClassificationTarget(label=label, value=encoded, encoding=encoding)
        return data


class RegressionFormatter(Formatter):
    def __init__(self, general_cfg: GeneralConfig, formatter_cfg: FormatterConfig):
        self.general_cfg = general_cfg
        self.formatter_cfg = formatter_cfg

        columns_slo = [
            configs.DATE_SLO,
            configs.TREATMENT_SLO,
            configs.BLOCK_SLO,
            configs.PLANT_SLO,
            configs.VARIETY_SLO,
        ]
        self.columns_eng = [
            configs.DATE_ENG,
            configs.TREATMENT_ENG,
            configs.BLOCK_ENG,
            configs.PLANT_ENG,
            configs.VARIETY_ENG,
        ]
        self.columns = {old_name: new_name for old_name, new_name in zip(columns_slo, self.columns_eng)}

    def format(self, data: StructuredData) -> StructuredData:
        regression_label = self.formatter_cfg.regression_label
        measurements_paths = self.formatter_cfg.measurements_paths
        target_column_label = measurements_paths[regression_label][0]
        file_path = measurements_paths[regression_label][1]

        measurements = pd.read_excel(file_path)
        # change date format to match the one in the config
        measurements[configs.DATE_SLO] = measurements[configs.DATE_SLO].dt.strftime(configs.DATE_FORMAT)
        measurements.rename(columns=self.columns, inplace=True, errors="raise")

        # keep only varieties defined in the toml config
        data = self._filter_data(data)

        # match rows from measurements with rows from metadata
        merged_df = pd.merge(
            data.meta, measurements, on=self.columns_eng, how="inner", validate="one_to_one"
        )
        if len(data.meta) != len(merged_df):
            logging.error(
                f"Number of rows in metadata and measurements do not match.\n"
                f"Metadata: {len(data.meta)}, measurements: {len(merged_df)}."
            )
            raise ValueError("Number of rows in metadata and measurements do not match.")

        data.target = RegressionTarget(name=target_column_label, value=merged_df[target_column_label])
        return data
