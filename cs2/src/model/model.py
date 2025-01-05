import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score, log_loss
import pandas as pd

class WPAModel:
    """
    A Win Probability Model desinged to work with extracted features from professional Counter Strike Global Offensive games utilizing awpy library. Underlying architecture utilizes
    XGBoost as the driving force behind it.
    """

    def __init__(self, config: dict):
        '''
        Sets up model parameters and the configuration. 
        Utilizes a binary logistic objective function as win probability is a binary classification problem (Either we win or lose). The objective function outputs probabilities between 0 and 1
        Limit the decision tree to a depth of 6 which prevents overfitting by making sure tree's don't grow too complex and specific to our training data
        Subsample is limited to .8 so each tree uses only 80% of the training data randomly sampled
        We limit each tree to use only 80% of the features randomly sampled. Used to make the model more robust by preventing it from relying too heavily on any particular feature
        Uses a histogram based algorithm for faster training.
        '''
        self.model = None
        self.config = config

        #set up params
        #histogram based alogirthm divides continuous feature values into discrete bins
        #instead of eavluating every possible split points it only evaluates bin boundaries
        #Reduces amount of computation
        self.params = {
            'objective': 'binary:logistic',
            'eval_metric': 'logloss',
            'max_depth': 6,
            'learning_rate' : 0.1,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'tree_method': 'hist'
        }

    def train(self, X: pd.DataFrame, y: pd.Series):
        """
        Train the WPA Model
        Args:
            X: Feature Dataframe
            Y: Target Series (In our case the TeamWin column)
        """

        #set up training and validation data
        X_train, X_val, Y_train, Y_val = train_test_split(X, y, test_size=.2, random_state=42)

        #set up DMatrix datatypes
        dtrain = xgb.DMatrix(X_train, label=Y_train)
        dval = xgb.DMatrix(X_val, label=Y_val)

        #train model
        self.model = xgb.train(
            self.params,
            dtrain,
            evals=[(dtrain, 'train'), (dval, 'val')],
            num_boost_round = 1000,
            early_stopping_rounds=50,
            verbose_eval=100
        )

    def predict_proba(self, X: pd.DataFrame):
        '''
        Predicts probabilities on a feature set
        Args:
            X: Feature Dataframe
        Return:
            returns a numpy array which represents outputted predictions for each of the feature vectors
        '''
        dtest = xgb.DMatrix(X)
        return self.model.predict(dtest)

    def evaluate(self, X: pd.DataFrame, y: pd.Series):
        '''
        Evaluation metrics:
            AUC: Area under ROC Curve
                -Measures how well the model can distinguish between wins and losses
                -Ranges between 0 and 1
                -Shows performance across all probability thresholds
            LogLoss:
                -Measures how accurate predicated probabilities are 
                -Heavily penalizes confident wrong predictions through the use of a logarithmic function
            Accuracy:
                -Using a threshold of .5. > .5 means prediction of round win, <= means round loss
        
        Return:
            Dictionary representing the evaluation metrics for the feature set. 3 params are auc, logloss, and accuracy
        '''
        # Convert X to DMatrix for prediction
        dtest = xgb.DMatrix(X)
        predictions = self.model.predict(dtest)

        # Use original y (not DMatrix) for evaluation metrics
        return {
            'auc': roc_auc_score(y, predictions),
            'logloss': log_loss(y, predictions),
            'accuracy': accuracy_score(y, predictions > 0.5)
        }
    
    def get_feature_importance(self):
        '''
        Outputs the feature importance values for the model. Throws an exception if model doesn't exist

        Return:
            Pandas dataframe representing importance scores for the features sorted from most important to least
        '''
        #get importance score
        importance_scores = self.model.get_score(importance_type='gain')

        return pd.DataFrame({
            'feature': list(importance_scores.keys()),
            'importance': list(importance_scores.values())
        }).sort_values('importance', ascending=False)
    
    def save_model(self, path: str):
        '''
        Saves model to disk

        Args:
            path: location on disk to save the model
        '''
        self.model.save_model(path)

    def load_model(self, path: str):
        '''
        Loads model from disk
        
        Args:
            path: Location on disk to load the model from 
        '''
        self.model = xgb.Booster()
        self.model.load_model(path)