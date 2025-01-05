from src.model import WPAModel
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob

if __name__ == "__main__":
    # Path to the folder containing the preprocessed features
    features_folder = "D:/Data_Warehouse_CS/WPA_MODEL/cs2/features"

    # Get all CSV files in the folder
    all_files = glob.glob(os.path.join(features_folder, "preprocessed_*"))

    # Read and concatenate all CSV files
    df_list = []
    for filename in all_files:
        df = pd.read_csv(filename)
        df_list.append(df)

    # Concatenate all dataframes
    df = pd.concat(df_list, ignore_index=True)

    X, Y = df.drop(['TeamWin'], axis=1), df['TeamWin']

    model = WPAModel({})

    model.train(X, Y)
    model.save_model('initial_model')

    # Get evaluation metrics
    eval_metrics = model.evaluate(X, Y)
    print("\nModel Performance Metrics:")
    for metric, value in eval_metrics.items():
        print(f"{metric}: {value:.4f}")

    feature_importance = model.get_feature_importance()
    feature_importance.to_csv('feature_importance_initial.csv')

    # Plot top N most important features
    plt.figure(figsize=(12, 6))
    sns.barplot(data=feature_importance.head(10), x='importance', y='feature')
    plt.title('Top 10 Most Important Features')
    plt.tight_layout()
    plt.savefig('feature_importance.png')