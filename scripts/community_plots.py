import matplotlib.pyplot as plt
import pandas as pd


def node_type_count_bar_plot(df_sorted, rows):
    # Select percentage columns and first 10 rows (sroted by score)
    df_to_plot = df_sorted.iloc[rows, df_sorted.columns.str.endswith('_Nodes')]

    # Transpose DataFrame for plotting
    df_to_plot = df_to_plot.transpose()

    # Create bar plot
    df_to_plot.plot(kind='bar', figsize=(10, 6), colormap="Set3")
    plt.xlabel('Label')
    plt.ylabel('Count')
    plt.title('Count of Node Labels for Top 10 Communities')
    plt.xticks(rotation=45)
    plt.legend(title='Community ID')
    plt.tight_layout()
    plt.show()


def node_type_percentage_bar_plot(df_sorted):
    # Select percentage columns and first 10 rows (sroted by score)
    df_to_plot = df_sorted.iloc[:10, df_sorted.columns.str.endswith('nodes_perc')]

    # Transpose DataFrame for plotting
    df_to_plot = df_to_plot.transpose()

    # Create bar plot
    df_to_plot.plot(kind='bar', figsize=(10, 6), colormap="Set3")
    plt.xlabel('Label')
    plt.ylabel('Percentage')
    plt.title('Percentage of Node Labels for Top 10 Communities')
    plt.xticks(rotation=45)
    plt.legend(title='Community ID')
    plt.tight_layout()
    plt.show()


def edge_type_count_bar_plot(df_sorted):
    # Select columns and first 10 rows (sroted by score)
    df_to_plot = df_sorted.iloc[:10, df_sorted.columns.str.endswith('_edges')]

    # Transpose DataFrame for plotting
    df_to_plot = df_to_plot.transpose()

    # Create bar plot
    df_to_plot.plot(kind='bar', figsize=(10, 6), colormap="Set3")
    plt.xlabel('Type')
    plt.ylabel('Count')
    plt.title('Count of Edge Types for Top 10 Communities')
    plt.xticks(rotation=45)
    plt.legend(title='Community ID')
    plt.tight_layout()
    plt.show()


def edge_type_percentage_bar_plot(df_sorted):
    # Select columns and first 10 rows (sroted by score)
    df_to_plot = df_sorted.iloc[:10, df_sorted.columns.str.endswith('_edges_perc')]

    # Transpose DataFrame for plotting
    df_to_plot = df_to_plot.transpose()

    # Create bar plot
    df_to_plot.plot(kind='bar', figsize=(10, 6), colormap="Set3")
    plt.xlabel('Type')
    plt.ylabel('Percentage')
    plt.title('Percentage of Edge Types for Top 10 Communities')
    plt.xticks(rotation=45)
    plt.legend(title='Community ID')
    plt.tight_layout()
    plt.show()


def percentage_top_n_communities(df_sorted, top_n=10):
    # Select columns and first 10 rows (sroted by score)
    df_to_plot = df_sorted.iloc[:top_n, df_sorted.columns.str.endswith('fraud_pct')]

    # Transpose DataFrame for plotting
    df_to_plot = df_to_plot.transpose()

    # Create bar plot
    df_to_plot.plot(kind='bar', figsize=(10, 6), colormap="Set3")
    plt.xlabel('Type')
    plt.ylabel('Percentage')
    plt.title(f'Percentage of Fraud Indicators for Top {top_n} Communities')
    plt.xticks(rotation=45)
    plt.legend(title='Community ID')
    plt.tight_layout()
    plt.show()