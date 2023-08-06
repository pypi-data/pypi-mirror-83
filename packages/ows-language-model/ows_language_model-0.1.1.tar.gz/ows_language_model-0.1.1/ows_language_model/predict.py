import logging

import pandas as pd

from ows_language_model import __version__ as _version
from ows_language_model.processing import data_management as dm

_logger = logging.getLogger(__name__)
PIPELINE = dm.load_pipeline()


def make_single_prediction(*, input_text):
    """Make a single prediction using the saved model pipeline.

        Args:
            input_text: variable length sequence of text

        Returns
            Dictionary with both raw next-word predictions and readable values.
        """
    
    predictions = input_text #PIPELINE.predict(input_text)
    
    _logger.info(f'Made prediction: {predictions}'
                 f' with model version: {_version}')

    return dict(predictions=predictions,
                version=_version)


def make_bulk_prediction(*, text_df: pd.Series) -> dict:
    """Make multiple predictions using the saved model pipeline.

    Currently, this function is primarily for testing purposes,
    allowing us to pass in a series of text examples

    Args:
        images_df: Pandas series of images

    Returns
        Dictionary with both raw predictions and their classifications.
    """

    _logger.info(f'received input df: {text_df}')

    predictions = PIPELINE.predict(text_df)

    _logger.info(f'Made predictions: {predictions}'
                 f' with model version: {_version}')

    return dict(predictions=predictions,
                version=_version)
