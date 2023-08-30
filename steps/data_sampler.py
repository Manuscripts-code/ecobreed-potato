import logging

from typing_extensions import Annotated
from zenml import step

from configs import configs
from configs.parser import SamplerConfig
from data_manager import samplers
from data_manager.loaders import StructuredData
from utils.utils import init_object

SPLITTERS_OPT = {
    "SimpleSplitter": samplers.SimpleSplitter,
}


@step
def data_sampler(
    data: StructuredData, sampler_cfg: SamplerConfig
) -> tuple[
    Annotated[StructuredData, "data_train"],
    Annotated[StructuredData, "data_val"],
    Annotated[StructuredData, "data_test"],
]:
    splitter_name = sampler_cfg.splitter
    splitter = init_object(SPLITTERS_OPT, splitter_name, **sampler_cfg.to_dict())
    sampler = samplers.Sampler(splitter)
    data_train, data_val, data_test = sampler.sample(data)
    return data_train, data_val, data_test
