import sys
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from disaster_messaging_classification_model.config import config
import logging


def load_data(messages_filepath):
    """
        Load data from the csv. 
    Args: 
        messages_filepath: the path of the messages.csv files that needs to be transferred
        categories_filepath: the path of the categories.csv files that needs to be transferred
    Returns: 
        merged_df (DataFrame): messages and categories merged dataframe
    """
    # read the csv and skip the first 2 columns
    df = pd.read_csv(messages_filepath)
    return df


def train_test_split_label(df):
    """
        Add a column indicating the datapoint belonging to training/test set

    Args:
        df: The preprocessed dataframe
    Returns:
        df with set_label column added
    """
    np.random.seed(config.RANDOM_SEED)
    df["set_label"] = np.random.choice(
        ["train", "test"],
        size=len(df),
        p=[config.TRAINING_DATA_PCT, 1 - config.TRAINING_DATA_PCT],
    )
    return df


def save_data(df, database_filename):
    """
        Save processed dataframe into sqlite database

    Args: 
        df: The preprocessed dataframe
        database_filename: name of the database
    Returns: 
        None
    """

    # save data into a sqlite database
    engine = create_engine(f"sqlite:///{database_filename}")
    df.to_sql(config.TABLE_NAME, engine, index=False, if_exists="replace")


def process_data():

    _logger = logging.getLogger(__name__)

    # load messages and categories
    messages_filepath = config.DATASET_DIR / config.DATA_FILE_NAME

    _logger.info("Loading data...\n    MESSAGES: {}\n   ".format(messages_filepath))
    df = load_data(messages_filepath)

    _logger.info("Generating train test split label")
    df = train_test_split_label(df)

    _logger.info("Saving data...\n    DATABASE: {}".format(config.DATABASE_NAME))
    save_data(df, config.DATASET_DIR / config.DATABASE_NAME)

    _logger.info("Processed data saved to database!")


if __name__ == "__main__":
    process_data()
