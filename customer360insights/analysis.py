from statistics import correlation
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from os import path

visualization_dir = "visualizations"

def load_data(path : str) -> pd.DataFrame:
    # Load the dataset into a datafram
    data = pd.read_csv(path)

    return data


def preprocess_data(data : pd.DataFrame) -> pd.DataFrame:
    # Check data for missing values
    logging.info(f"Missing data is:\n{data.isna().sum()}")

    # Fill Nan values with proper values
    data["OrderConfirmationTime"].fillna("No Purchase")
    data["PaymentMethod"].fillna("No Purchase")
    data["OrderReturn"].fillna("False")
    data["ReturnReason"].fillna("No Reason")

    # Check data for duplicate values
    logging.info(f"Duplicate rows are:\n{data.duplicated().sum()}")

    # Check for outliers with IQR method
    # Since the outliers are only presented in "Price" and "Cost" columns, which are reasonable based on the product, 
    # there is no need to do anything for them
    described_data = data.drop(columns=["CustomerID"]).describe(include=["int64"])
    for col in described_data.columns:
        q1 = described_data.loc["25%", col]
        q3 = described_data.loc["75%", col]
        iqr = q3 - q1
        outliers = data[(data[col] < q1 - 1.5 * iqr) | (data[col] > q3 + 1.5 * iqr)]
        # Find and log the outliers of the column
        logging.info(f"Outliers of column {col} are:\n{outliers}")

    # Change datatypes to desirable ones using pandas heuristics 
    data["SessionStart"] = pd.to_datetime(data["SessionStart"])
    data["CartAdditionTime"] = pd.to_datetime(data["CartAdditionTime"])
    data["OrderConfirmationTime"] = pd.to_datetime(data["OrderConfirmationTime"])
    data["SessionEnd"] = pd.to_datetime(data["SessionEnd"])
    data["OrderReturn"] = data["OrderReturn"].astype("bool")

    # Encode needed categorical columns
    le = LabelEncoder()
    for col in data.select_dtypes(include=["object", "bool"]).drop(columns=["FullName", "ReturnReason"]).columns:
        data[col + "_encoded"] = le.fit_transform(data[col])

    return data


def eda(data : pd.DataFrame):

    # Log the first 5 rows of the dataset
    logging.info(f"The first 5 rows of the data is:\n{data.head(5)}")

    # Log the last 5 rows of the dataset
    logging.info(f"The last 5 rows of the data is:\n{data.tail(5)}")
    
    # Log datatypes
    logging.info(f"Data types are as follows:\n{data.dtypes}")

    # Log the stats of the numeric fields
    described_data = data.drop(columns=["CustomerID"]).describe(include=["int64"])
    logging.info(f"The statistics of the numeric columns of the data:\n{described_data}")

    correlations = data[described_data.columns].corr()
    logging.info(f"Correlation of columns of the data:\n{correlations}")

    # Set the resolution and quality
    fig = plt.figure(figsize=(16, 9), dpi=600)
    # Setup the layout to fit in the figure
    plt.tight_layout(pad=1, h_pad=0.5, w_pad=0.5)

    # heat map of coorrelations
    sns.heatmap(correlations)
    # Save the file with proper dpi
    file_name = path.join(visualization_dir, f"Correlation_heatmap.png")
    plt.savefig(fname=file_name, format="png", dpi=fig.dpi)
    plt.clf()

    for col in described_data.columns:
        # Create subplots for the current column (Box plot, Histogram, and Bar plot based on the country)
        ax1 = plt.subplot(1, 3, 1)
        sns.boxplot(data[col], ax=ax1)
        ax1.set_title("Box Plot")

        ax2 = plt.subplot(1, 3, 2)
        sns.histplot(data[col], kde=True, ax=ax2)
        ax2.set_title("Histogram")

        ax3 = plt.subplot(1, 3, 3)
        sns.barplot(data, x="Country", y = col, ax=ax3)
        ax3.set_title("Bar Plot")

        # Save the file with proper dpi
        file_name = path.join(visualization_dir, f"{col}.png")
        plt.savefig(fname=file_name, format="png", dpi=fig.dpi)

        plt.clf()
    
    # Scatter plot for all pairs of columns
    sns.pairplot(data)
    # Save the file with proper dpi
    file_name = path.join(visualization_dir, f"PairPlot.png")
    plt.savefig(fname=file_name, format="png", dpi=fig.dpi)
    plt.clf()

    plt.close()


def main():
    # Configure logging to log everything in the app
    logging.basicConfig(filename="analysis.log", filemode="w", level=logging.INFO)

    # Load the dataset
    data = load_data("dataset/customer360insights.csv")

    # Preprocess data and prepare it for analysis
    data = preprocess_data(data)

    # Exploratory Data Analysis
    eda(data)


if __name__ == "__main__":
    main()