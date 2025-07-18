import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from os import path

# Directory to store all visualizations
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

    # Standard Scaling some columns
    for col in ["Age", "CreditScore", "MonthlyIncome", "Price", "Cost"]:
        ss = StandardScaler()
        data[col] = ss.fit_transform(data[[col]])

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

    # heat map of correlations
    sns.heatmap(correlations, annot=True, fmt="0.2g", cmap="Blues")
    # Save the file with proper dpi
    file_name = path.join(visualization_dir, f"Correlation_heatmap.png")
    plt.savefig(fname=file_name, format="png", dpi=fig.dpi, bbox_inches='tight')
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
        plt.savefig(fname=file_name, format="png", dpi=fig.dpi, bbox_inches='tight')

        plt.clf()
    
    # Scatter plot for all pairs of columns
    sns.pairplot(data)
    # Save the file with proper dpi
    file_name = path.join(visualization_dir, f"PairPlot.png")
    plt.savefig(fname=file_name, format="png", dpi=fig.dpi, bbox_inches='tight')
    plt.clf()

    plt.close()

def classification(data : pd.DataFrame):
    # Create features and label(target) variable
    X = data[data.drop(columns=["CustomerID", "OrderConfirmation_encoded", "OrderReturn_encoded"]).describe(include=["int64"]).columns]
    y = data["OrderConfirmation_encoded"]

    # Split features and label into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a logistic regression model to classify binary "OrderConfirmation"
    lr = LogisticRegression(random_state=42, solver="liblinear")
    lr.fit(X_train, y_train)

    # Predict test set with the trained model
    y_pred = lr.predict(X_test)

    # Create confusion matrix based on preoicted and real label(target) values
    conf_matrix = confusion_matrix(y_test, y_pred)
    logging.info(f"Confusion matrix:\n{conf_matrix}")

    # Create classification report including Accuracy, Precision, Recall, etc.
    class_report = classification_report(y_test, y_pred)
    logging.info(f"classification report:\n{class_report}")

    # Set the resolution and quality
    fig = plt.figure(figsize=(16, 9), dpi=600)
    # Setup the layout to fit in the figure
    plt.tight_layout(pad=1, h_pad=0.5, w_pad=0.5)

    # heat map of confusion matrix
    sns.heatmap(conf_matrix, annot=True, fmt="g", cmap="Blues")
    # Save the file with proper dpi
    file_name = path.join(visualization_dir, f"confusion_matrix_heatmap.png")
    plt.savefig(fname=file_name, format="png", dpi=fig.dpi, bbox_inches='tight')
    plt.clf()


def main():
    # Configure logging to log everything in the app
    logging.basicConfig(filename="analysis.log", filemode="w", level=logging.INFO)

    # Load the dataset
    data = load_data("dataset/customer360insights.csv")

    # Preprocess data and prepare it for analysis
    data = preprocess_data(data)

    # Exploratory Data Analysis
    eda(data)

    # Apply logistic regression classification on the binary "OrderConfirmation"
    classification(data)


if __name__ == "__main__":
    main()