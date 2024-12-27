from src.model import WPAModel
import pandas as pd

if __name__ == '__main__':
    model = WPAModel({})

    model.load_model("./initial_model")

    df = pd.read_csv('testing_features.csv')

    X, Y = df.drop(['id', 'TeamWin'], axis=1), df['TeamWin']

    eval_metrics = model.evaluate(X, Y)

    print("\nModel Performance Metrics:")
    for metric, value in eval_metrics.items():
        print(f"{metric}: {value:.4f}")