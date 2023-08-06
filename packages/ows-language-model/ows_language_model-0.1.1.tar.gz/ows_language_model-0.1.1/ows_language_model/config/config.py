# The Keras model loading function does not play well with
# Pathlib at the moment, so we are using the old os module
# style

import os

PWD = os.path.dirname(os.path.abspath(__file__))
PACKAGE_ROOT = os.path.abspath(os.path.join(PWD, '..'))
DATASET_DIR = os.path.join(PACKAGE_ROOT, 'datasets')
TRAINED_MODEL_DIR = os.path.join(PACKAGE_ROOT, 'trained_models')
DATA_FOLDER = os.path.join(DATASET_DIR, 'text_data')

# MODEL PERSISTING
MODEL_NAME = 'language_model'
PIPELINE_NAME = 'lm_pipe'

# MODEL FITTING HYPERPARAMETERS
VOCAB_SIZE = 30000
BATCH_SIZE = 16
EPOCHS = int(os.environ.get('EPOCHS', 1))  # 1 for testing, 10 for final model


with open(os.path.join(PACKAGE_ROOT, 'VERSION')) as version_file:
    _version = version_file.read().strip()

MODEL_FILE_NAME = f'{MODEL_NAME}_{_version}.h5'
MODEL_PATH = os.path.join(TRAINED_MODEL_DIR, MODEL_FILE_NAME)

PIPELINE_FILE_NAME = f'{PIPELINE_NAME}_{_version}.pkl'
PIPELINE_PATH = os.path.join(TRAINED_MODEL_DIR, PIPELINE_FILE_NAME)
