import pandas as pd
import logging

def load_csv(path):
    try:
        df = pd.read_csv(path)
        logging.info(f"Loaded file: {path}")
        return df
    except Exception as e:
        logging.error(f"Error loading file {path}: {e}")
        return pd.DataFrame()