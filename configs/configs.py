import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# PATHS
BASE_DIR = Path(__file__).parent.parent.absolute()
LOGS_DIR = Path(BASE_DIR, "logs")
DATA_DIR = Path(BASE_DIR, "data")
TOML_DIR = Path(BASE_DIR, "configs", "specific")

MUTISPECTRAL_DIR = Path(DATA_DIR, "multispectral_images")
SHAPEFILES_DIR = Path(DATA_DIR, "shapefiles")
MEASUREMENTS_DIR = Path(DATA_DIR, "measurements")

SAVE_DIR = Path(BASE_DIR, "saved")
SAVE_MERGED_DIR = Path(SAVE_DIR, "merged")
SAVE_RESULTS_DIR = Path(SAVE_DIR, "results")

# MAKE DIRS
SAVE_DIR.mkdir(parents=True, exist_ok=True)

# DATA CONFIGS
CACHING = os.getenv("CACHING", "false") == "true"
SAVE_COORDS = os.getenv("SAVE_COORDS", "false") == "true"
TOML_ENV_NAME = "DATA_TOML_NAME"
TOML_DEFAULT_FILE_NAME = "clf/_base.toml"
USE_REDUCED_DATASET = os.getenv("USE_REDUCED_DATASET", "false") == "true"

# TOML CONFIG ROOT KEYS
BASE_CFG_NAME = "_base.toml"
GENERAL_CFG_NAME = "general"
MULTISPECTRAL_CFG_NAME = "multispectral"
SAMPLER_CFG_NAME = "sampler"
FEATURES_CFG_NAME = "features_generator"
BALANCER_CFG_NAME = "balancer"
FORMATTER_CFG_NAME = "formatter"
MODEL_CFG_NAME = "model"
OPTIMIZER_CFG_NAME = "optimizer"
EVALUATOR_CFG_NAME = "evaluator"
REGISTRY_CFG_NAME = "registry"

# MULTISPECTRAL AND MEASUREMENTS LOADER CONFIG
DATE_ENG = "dates"
TREATMENT_ENG = "treatments"
BLOCK_ENG = "blocks"
PLANT_ENG = "plants"
VARIETY_ENG = "varieties"

DATE_SLO = "Datum"
TREATMENT_SLO = "Poskus"
BLOCK_SLO = "Blok"
PLANT_SLO = "Rastlina"
VARIETY_SLO = "Sorta"

# MISCELLANEOUS
RANDOM_SEED = 100
DATE_FORMAT = "%Y_%m_%d"
TIME_FORMAT = "%H_%M_%S"
DATETIME_FORMAT = "".join([DATE_FORMAT, "__", TIME_FORMAT])
TRAIN_STR = "train"
TEST_STR = "test"
DATE_FEATURE_ENCODING = "date_feature"

# MLFLOW ARTIFACTS SAVE VARS
MLFLOW_TRAIN = TRAIN_STR
MLFLOW_TEST = TEST_STR
MLFLOW_RESULTS = "results"
MLFLOW_CONFIGS = "configs"
MLFLOW_MODEL = "model"
MLFLOW_EXPLAINER = "explainer"

# COMMAND LINE CONFIGS
CMD_TRAIN_AND_REGISTER = "train"
CMD_DEPLOY_AND_TEST = "test"
CMD_EXECUTE_ALL = "all"

# MATERIALIZER CONFIGS
MATERIALIZER_DATA_JSON = "structured_data.json"
MATERIALIZER_DESCRIBE_DATA_CSV = "describe_data.csv"
MATERIALIZER_DESCRIBE_META_CSV = "describe_meta.csv"
MATERIALIZER_DESCRIBE_TARGET_CSV = "describe_target.csv"

# DATABASE CONFIGS
DB_NAME = os.getenv("DB_NAME", "database.db")
DB_PATH = Path(SAVE_DIR, DB_NAME)
DB_ECHO = os.getenv("DB_ECHO", "false") == "true"
DB_DATA_TRAIN = TRAIN_STR
DB_DATA_TEST = TEST_STR
DB_PREDICTIONS_TRAIN = TRAIN_STR
DB_PREDICTIONS_TEST = TEST_STR
DB_CV_METRIC_NAME = "cv_metric"

# SPECTRAL BANDS
BAND_BLUE = "blue"
BAND_GREEN = "green"
BAND_RED = "red"
BAND_RED_EDGE = "red_edge"
BAND_NIR = "nir"
BAND_BLUE_S = "B"
BAND_GREEN_S1 = "G"
BAND_GREEN_S2 = "G1"
BAND_RED_S = "R"
BAND_RED_EDGE_S1 = "RE1"
BAND_RED_EDGE_S2 = "RE2"
BAND_RED_EDGE_S3 = "RE3"
BAND_NIR_S1 = "N"
BAND_NIR_S2 = "N2"
