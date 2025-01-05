from sklearn.preprocessing import StandardScaler, OneHotEncoder
import pandas as pd
import numpy as np

class Transformer:
    def __init__(self):
        self.standard_scaler = StandardScaler()
        self.onehot_encoder = OneHotEncoder(sparse=False, handle_unknown="ignore")

    def fit_transform(self, features):
        df = pd.DataFrame(features)
        return self._fit_transform(df)

    def _fit_transform(self, df: pd.DataFrame):
        copy = df.copy()

        # Numerical features to be standardized
        numerical_features = [
            'ctEquipVal', 'tEquipVal', 'tPlayersAlive', 'ctPlayersAlive',
            'tHPRemaining', 'ctHPRemaining', 'tFlashDuration', 'ctFlashDuration',
            'activeTSmokes', 'activeCTSmokes', 'activeTInfernos', 'activeCTInfernos',
            'tAVGDist', 'ctAVGDist', 'killDifferential', 'ctDefuseKitCount'
        ]

        # Standardize numerical features
        copy[numerical_features] = self.standard_scaler.fit_transform(copy[numerical_features])

        # One-hot encode the bombPlantSite
        bombsite_encoded = self.onehot_encoder.fit_transform(copy[['bombPlantSite']])
        bombsite_cols = [f'bombsite_{site}' for site in self.onehot_encoder.categories_[0]]
        copy[bombsite_cols] = bombsite_encoded

        # Convert boolean to int
        copy['bombPlanted'] = copy['bombPlanted'].astype(int)

        # Drop the original bombPlantSite column
        copy = copy.drop(['bombPlantSite'], axis=1)

        # Ensure 'teamWin' is not transformed
        if 'teamWin' in copy.columns:
            copy['teamWin'] = copy['teamWin'].astype(int)

        return copy