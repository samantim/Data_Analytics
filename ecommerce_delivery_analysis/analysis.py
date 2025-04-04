# Here is the code for the analysis of the ecommerce delivery data
# The code is divided into different functions for better readability and maintainability
# The code uses the following libraries:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from general import Logger, show_elapsed_time
from sklearn.preprocessing import LabelEncoder

@show_elapsed_time
def read_data(path : str) -> pd.DataFrame:
    # Read the data from the csv file
    # and return the data as a pandas dataframe
    data = pd.read_csv(path)
    return data

@show_elapsed_time
def data_exploration(data : pd.DataFrame, suffix_msg : str, logger: Logger):
    # Data exploration function (EDA)
    # This function takes the data as input and performs the following operations

    # Log the data exploration
    logger.log(f"Data Exploratory Analysis {suffix_msg}:\n")

    # Get the first 5 rows
    logger.log(f"The first 5 rows of the data:\n{data.head()}\n")

    # Get the data types
    logger.log(f"Data types of the columns are:\n{data.dtypes}\n")

    # Get the number of rows and columns
    logger.log(f"Row and Column count of the data:\n{data.shape}\n")

    # Get the number of missing values
    logger.log(f"Missing values of the data are:\n{data.isna().sum()}\n")

    # Get the unique values
    logger.log(f"Data has these unique values:\n{data.nunique()}\n")

    # Get the number of duplicates
    logger.log(f"Duplicate values of the data are:\n{data.duplicated().sum()}\n")

    # Get the summary statistics
    logger.log(f"Summary of statisticals info of numberical columns:\n{data.describe()}\n")

@show_elapsed_time
def clean_data(data : pd.DataFrame, logger: Logger) -> pd.DataFrame:
    # Data cleaning function
    # This function takes the data as input and performs the following operations

    # Drop the missing values
    data.dropna(inplace=True)

    # Drop the duplicates
    data.drop_duplicates(inplace=True)

    # encode the categorical columns (convert them to numerical values)
    le = LabelEncoder()
    data["Delivery Delay"] = le.fit_transform(data["Delivery Delay"])
    data["Refund Requested"] = le.fit_transform(data["Refund Requested"])

    # Drop the columns that are not useful
    data.drop(["Order ID", "Customer ID", "Order Date & Time","Customer Feedback"], axis=1, inplace=True)

    # Change column names
    data.rename(columns={"Delivery Time (Minutes)":"Delivery_Time"}, inplace=True)
    data.rename(columns={"Product Category":"Product_Category"}, inplace=True)
    data.rename(columns={"Order Value (INR)":"Order_Value"}, inplace=True)
    data.rename(columns={"Service Rating":"Service_Rating"}, inplace=True)
    data.rename(columns={"Delivery Delay":"Delivery_Delay"}, inplace=True)
    data.rename(columns={"Refund Requested":"Refund_Requested"}, inplace=True)

    return data

def handle_outlier_values(data : pd.DataFrame, output_folder : str = "output", logger : Logger = None) -> pd.DataFrame:
    # Distinguish and remove the outliers based on IQR analysis
    describe = data.describe()

    # Box plot to show outliers
    plot_box(data=data, output_folder=output_folder, logger=logger)

    # Detecting outliers with IQR method
    logger.log("Outliers based on IQR method and skewness before handling them:\n")

    outliers_index = {}
    for col in describe.columns:
        # acquiring q1 and q3 to establish allowed area
        q1 = describe.loc["25%", col]
        q3 = describe.loc["75%", col]
        iqr = q3 - q1
        # every value outside of allowed area is distiguished as an outlier
        outliers = data[col].loc[(data[col] > q3 + 1.5*iqr) | (data[col] < q1 - 1.5*iqr)]
        logger.log(f"Outliers of Column {col} count: {outliers.count()}  ---  skewness: {data[col].skew()}")
        # outlier index of each column
        if not outliers.empty:
            outliers_index[col] = outliers.index

    # Replace outliers with mode of that columns
    for col in outliers_index.keys():
        data.loc[outliers_index[col],col] = data.mode(numeric_only=True).loc[0,col]
    
    # Detecting outliers with IQR method after handling them
    logger.log("\nOutliers based on IQR method and skewness after handling them:\n")
    
    outliers_index = {}
    for col in describe.columns:
        # acquiring q1 and q3 to establish allowed area
        q1 = describe.loc["25%", col]
        q3 = describe.loc["75%", col]
        iqr = q3 - q1
        # every value outside of allowed area is distiguished as an outlier
        outliers = data[col].loc[(data[col] > q3 + 1.5*iqr) | (data[col] < q1 - 1.5*iqr)]
        logger.log(f"Outliers of Column {col} count: {outliers.count()}  ---  skewness: {data[col].skew()}")
        # outlier index of each column
        if not outliers.empty:
            outliers_index[col] = outliers.index

    return data

def plot_box(data : pd.DataFrame, suffix : str = "", output_folder : str = "output", logger : Logger = None):
    # Boxplots of input of dataset (features) to show outliers
    # set the figure resolution and dpi
    fig = plt.figure(figsize=(16, 9), dpi=600)

    # Distinguish and remove the outliers based on IQR analysis
    describe = data.describe()
    row_count = 1
    col_count = len(describe.columns)

    i = 1
    for col in describe.columns:
        # Creating inputs subplots
        plt.subplot(row_count, col_count, i)
        sns.boxplot(data[col])
        plt.title(f"{col} (input)")
        i += 1

    # setup the layout to fit in the figure
    plt.tight_layout(pad=1, h_pad=0.5, w_pad=0.5) 
    # Save the file with proper dpi
    plt.savefig(fname=f"{output_folder}/input_outliers{('_' if suffix else '') + suffix}.png", format="png", dpi = fig.dpi)


@show_elapsed_time
def visualize_data(data : pd.DataFrame):
    # Data visualization function
    # This function takes the data as input and performs the following operations using matplotlib and seaborn

    # Create the figure and set the size and dpi
    fig = plt.figure(figsize=(16,9), dpi=600)

    # pairplot which shows the distribution of each feature and the relationship between each pair of features
    sns.pairplot(data)
    plt.savefig(fname="outputs/plots/pairplot.png", format="png", dpi=fig.dpi)
    plt.clf()

    # Pie chart of order value of each product category 
    # Group the data by product category and sum the order value
    data_grouped = data.groupby("Product_Category").sum(numeric_only=True).reset_index()
    plt.pie(x=data_grouped["Order_Value"], labels=data_grouped["Product_Category"])
    plt.xlabel("Product_Category")
    plt.ylabel("Order Value")
    plt.title("Order Value of each Product Category")
    plt.savefig(fname="outputs/plots/order_value_of_each_product_category.png", format="png", dpi=fig.dpi)
    plt.clf()

    # Bar Plot of refund requested of each product category
    sns.barplot(data=data_grouped, x="Product_Category", y="Refund_Requested")
    plt.xlabel("Product_Category")
    plt.ylabel("Refund Requested")
    plt.title("Refund Requested of each Product Category")
    plt.savefig(fname="outputs/plots/refund_requested_of_each_product_category.png", format="png", dpi=fig.dpi)
    plt.clf()

    # Bar plot of delivery delay of each platform
    # Group the data by platform and sum the delivery delay
    data_grouped = data.groupby("Platform").sum(numeric_only=True).reset_index()
    sns.barplot(data=data_grouped, x="Platform", y="Delivery_Delay")
    plt.xlabel("Platform")
    plt.ylabel("Delivery Delay")
    plt.title("Delivery Delay of each Platform")
    plt.savefig(fname="outputs/plots/delivery_delay_of_each_platform.png", format="png", dpi=fig.dpi)
    plt.clf()

    # Bar plot of Average Service Rating of each product category
    # Group the data by product category and mean of service rating
    data_grouped = data.groupby("Product_Category").mean(numeric_only=True).reset_index()
    sns.barplot(data=data_grouped, x="Product_Category", y="Service_Rating")
    plt.xlabel("Product_Category")
    plt.ylabel("Service Rating")
    plt.title("Average Service Rating of each Product_Category")
    plt.savefig(fname="outputs/plots/average_service_rating_of_each_product_category.png", format="png", dpi=fig.dpi)
    plt.clf()

    # Bar plot of Average Service_Rating of each Platform
    # Group the data by platform and mean of service rating
    data_grouped = data.groupby("Platform").mean(numeric_only=True).reset_index()
    sns.barplot(data=data_grouped, x="Platform", y="Service_Rating")
    plt.xlabel("Platform")
    plt.ylabel("Service Rating")
    plt.title("Average Service Rating of each Platform")
    plt.savefig(fname="outputs/plots/average_service_rating_of_each_platform.png", format="png", dpi=fig.dpi)
    plt.clf()

    # Histogram of Service Rating
    sns.histplot(data=data, x="Service_Rating",kde=True)
    plt.xlabel("Service Rating")
    plt.ylabel("Rating Count")
    plt.title("Service Rating Distribution")
    plt.savefig(fname="outputs/plots/service_rating_histogram.png", format="png", dpi=fig.dpi)
    plt.clf()

def plot_correlation(data : pd.DataFrame, suffix : str = "", output_folder : str = "output", logger : Logger = None):
    # Extract correlatoin between features themselves and also with label plus plot their heatmap
    # set the figure resolution and dpi
    fig = plt.figure(figsize=(16, 9), dpi=600)
    correlations = data.drop(columns=["Platform", "Product_Category"]).corr()
    logger.log(f"correlations of features:\n{correlations}")
    sns.heatmap(correlations,annot=True)
    # Save the file with proper dpi
    plt.savefig(fname=f"{output_folder}/correlations{('_' if suffix else '') + suffix}.png", format="png", dpi = fig.dpi)
   

def main():
    # Initialize the logger
    logger = Logger()

    # Load the data
    data = read_data("dataset/Ecommerce_Delivery_Analytics.csv")

    # explore the data before cleaning
    data_exploration(data, "Before Cleaning" , logger)

    # Handle outlier values
    data = handle_outlier_values(data, output_folder="outputs/plots", logger=logger)

    # Clean the data
    data = clean_data(data, logger)

    # explore the data after cleaning
    data_exploration(data, "After Cleaning" , logger)

    # Plot the correlation between features
    plot_correlation(data, suffix="after_cleaning", output_folder="outputs/plots", logger=logger)

    # Visualize the data
    visualize_data(data)

    logger.save_file("outputs/logs/log.txt")

if __name__ == "__main__":
    main()

