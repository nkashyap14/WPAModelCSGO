from src.model import WPAModel
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


if __name__ == "__main__":

    df = pd.read_csv("preprocessed_features.csv")

    X, Y = df.drop(['id', 'TeamWin'], axis=1), df['TeamWin']


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
    sns.barplot(data=feature_importance.head(15), x='importance', y='feature')
    plt.title('Top 15 Most Important Features')
    plt.tight_layout()
    plt.savefig('feature_importance.png')
