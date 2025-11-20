import os
import matplotlib as plt
import seaborn as sns
import pandas as pd

# --- PLOT STATISTICS ---
def plot_statistics(df, dataset_name, result_dir="plots", notebook_plot=False):
    """
    Generates and saves basic plots for a given DataFrame.

    :param result_dir: where to place plots
    :param df: The pandas DataFrame
    :param dataset_name: A name for titling plots (e.g., 'Titanic')
    """
    print(f"--- Plotting statistics for {dataset_name} ---")

    # Ensure a directory for plots exists
    os.makedirs(result_dir, exist_ok=True)

    # Identify numerical and categorical columns for plotting
    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns

    # Plot 1: Histogram (for a numerical column)
    if not numerical_cols.empty:
        col_to_plot = numerical_cols[0]
        plt.figure(figsize=(10, 6))
        df[col_to_plot].hist(bins=30, edgecolor='black')
        plt.title(f'Histogram of {col_to_plot} - {dataset_name}')
        plt.xlabel(col_to_plot)
        plt.ylabel('Frequency')
        plt.grid(axis='y')
        if not notebook_plot:
            plt.savefig(f'{result_dir}/{dataset_name}_histogram.png')
            print(f"Saved histogram for {col_to_plot}")
            plt.close()
        else:
            plt.plot()

    # Plot 2: Bar Chart (for a categorical column)
    if not categorical_cols.empty:
        # Use the first categorical column with less than 30 unique values
        for col_to_plot in categorical_cols:
            if df[col_to_plot].nunique() < 30:
                plt.figure(figsize=(10, 6))
                df[col_to_plot].value_counts().plot(kind='bar')
                plt.title(f'Bar Chart of {col_to_plot} - {dataset_name}')
                plt.xlabel(col_to_plot)
                plt.ylabel('Count')
                plt.xticks(rotation=45)
                plt.grid(axis='y')
                if not notebook_plot:
                    plt.savefig(f'{result_dir}/{dataset_name}_barchart.png')
                    print(f"Saved bar chart for {col_to_plot}")
                    plt.close()
                else:
                    plt.plot()
                break  # Only plot the first suitable one

    # Plot 3: Scatter Plot (for two numerical columns)
    if len(numerical_cols) >= 2:
        col1 = numerical_cols[0]
        col2 = numerical_cols[1]
        plt.figure(figsize=(10, 6))
        plt.scatter(df[col1], df[col2], alpha=0.5)
        plt.title(f'Scatter Plot: {col1} vs {col2} - {dataset_name}')
        plt.xlabel(col1)
        plt.ylabel(col2)
        plt.grid(True)
        if not notebook_plot:
            plt.savefig(f'{result_dir}/{dataset_name}_scatterplot.png')
            print(f"Saved scatter plot for {col1} vs {col2}")
            plt.close()
        else:
            plt.plot()

def plot_all_trends(csv, result_dir="plots", notebook_plot=False):
    """
    Generates and saves basic plots for all Google trends data.

    :param result_dir: where to place plots
    :param df: The pandas DataFrame
    :param notebook_plot: show plot if function is called in .ipynb
    :param keywords: List of sponsors for titling plots (e.g., 'Rakuten')
    """
    
    all_trends = pd.read_csv('../data/cleaned/All_Trends_Cleaned.csv', parse_dates=['Date'])

    # Ensure a directory for plots exists
    os.makedirs(result_dir, exist_ok=True)

    season_dates = [(2021,'2020-12-22','2021-05-16'),(2022,'2021-10-19','2022-04-10'),(2023,'2022-10-18','2023-04-09'),(2024,'2023-10-24','2024-04-14'),(2025,'2024-10-23','2025-04-13')]

    for year,start_date,end_date in season_dates:
        season_range = (all_trends['Date'] >= pd.to_datetime(start_date)) & (all_trends['Date'] <= pd.to_datetime(end_date))
        plt.figure(figsize=(18,8))
        for keyword in all_trends.columns:
            if keyword == "Date":
                continue
            plt.plot(all_trends.loc[season_range,"Date"], all_trends.loc[season_range,keyword], label=keyword)

        plt.title(f'{year} Sponsor Trend Data')
        plt.legend()
        plt.xlabel('Date')
        plt.ylabel('Interest over Time')

        # Set x-axis major ticks every 10 days
        ax = plt.gca()
        ax.set_xlim(pd.to_datetime(start_date), pd.to_datetime(end_date))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.xticks(rotation=45)

        plt.show()