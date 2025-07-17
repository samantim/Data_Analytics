import pandas as pd
import numpy as np
import sklearn
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(path : str) -> pd.DataFrame:
    # Load the dataset into a datafram
    data = pd.read_csv(path)
    return data


def eda(data : pd.DataFrame):
    