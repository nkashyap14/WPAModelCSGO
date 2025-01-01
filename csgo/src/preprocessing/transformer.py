from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
import pandas as pd

class Transformer:
    def __init__(self, config: dict):
        self.standard_scaler = StandardScaler()
        self.onehot_encoder = OneHotEncoder(sparse=False, handle_unknown="ignore")
        self.ordinal_encoder = OrdinalEncoder()

        self.buy_type_order = ['Full Eco', 'Semi Eco', 'Semi Buy', 'Full Buy']

    def transform_data(self, features):
        all_vectors = []

        for _, vectors in features.items():
            for vector in vectors:
                all_vectors.append(vector)

        df = pd.DataFrame(all_vectors)

        return self._fit_transform(df)

    def _fit_transform(self, df: pd.DataFrame):

        copy = df.copy()

        numerical_features = [
            'teammatesAlive', 'enemiesAlive', 'teammateHp', 'enemyHp',
            'teamEquipmentValue', 'enemyEquipmentValue', 'teamUtilCount', 
            'enemyUtilCount', 'clockTime', 'playerCountDifferential'
        ]

        copy[numerical_features] = self.standard_scaler.fit_transform(copy[numerical_features])

        bombsite_encoded = self.onehot_encoder.fit_transform(copy[['bombsitePlantedAt']])
        bombsite_cols = [f'bombsite_{site}' for site in ['A', 'B', 'N/A']]

        copy[bombsite_cols] = bombsite_encoded

        copy['teamBuyType'] = self.ordinal_encoder.fit_transform(
            copy[['teamBuyType']].values.reshape(-1, 1)
        )
        copy['enemyBuyType'] = self.ordinal_encoder.fit_transform(
            copy[['enemyBuyType']].values.reshape(-1, 1)
        )

        copy['game_phase'] = copy['roundNumber'].astype(int).apply(self.encode_round_phase)
        #drop the column that we one hot encoded
        copy = copy.drop(['bombsitePlantedAt', 'roundNumber', 'tick'], axis=1)

        return copy
    

    @staticmethod
    def encode_round_phase(round_num):
        if round_num <= 5:
            return 0  # Early game
        elif round_num <= 20:
            return 1  # Mid game
        else:
            return 2  # Late game
