class Extractor:
    def __init__(self, config: dict):
        pass

    def extractFeatures(self, matches):
        """
        Will take in matches which represents a list of parsed counter strike games Each individual game is a 
        dictionary with a set of keys. The relevant keys to us are in turn mapped to a dataframe which contains data
        related to the specific match of the type specified by the keys
        Proceeds to extract features from each individual match relevant to the feature vector for the counter strike WPA model
        """
        output = {}
        print("in extract features")
        for match in matches:
            print('extract features of match {}'.format(match["matchID"]))
            if len(match['rounds']) > 0:
                feature_vectors = self._extractFeature(match)
                output[match['matchID'] + match['mapName']] = feature_vectors

        return output

    def _extractFeature(self, match):
        vectors = []
        print('extracting features for match {} which has {} rounds and {} ticks'.format(match['matchID'], len(match['rounds']), len(match['frames'])))
        for round in match['rounds']['roundNum'].unique():
            for tick in match['frames'][match['frames']['roundNum'] == round]['tick'].unique():
                ctVector, tVector = {}, {}
                self._extract_direct_features(match, round, tick, 'CT', ctVector)
                self._extract_calculated_features(match, round, tick, 'CT', ctVector)
                self._extract_direct_features(match, round, tick, 'T', tVector)
                self._extract_calculated_features(match, round, tick, 'T', tVector)
                vectors.append(ctVector)
                vectors.append(tVector)
                #self._extract_engineered_features(match, round, tick)

        print("extracted features the number of features extracted is {}".format(len(vectors)))

        return vectors


    def _extract_direct_features(self, match, round, tick, side, vector):
        """
        Extracts direct features from a match datastructure which is a dictionary mapping keys to various types of dataframes which contain different types of data about an individual counter strike game
        """
        frameRow =  match['frames'].loc[(match['frames']['roundNum'] == round) & (match['frames']['tick'] == tick)]
        roundRow = match['rounds'].loc[(match['rounds']['roundNum'] == round)]
        bombEvents = match['bombEvents'].loc[(match['bombEvents']['roundNum'] == round) & (match['bombEvents']['bombAction'] == 'plant')]
        match side:
            case 'T':
                vector['teammatesAlive'] = frameRow['tAlivePlayers'].iloc[0]
                vector['enemiesAlive'] = frameRow['ctAlivePlayers'].iloc[0]
                vector['teamEquipmentValue'] = frameRow['tEqVal'].iloc[0]
                vector['enemyEquipmentValue'] = frameRow['ctEqVal'].iloc[0]
                vector['teamBuyType'] = roundRow['tBuyType'].iloc[0]
                vector['enemyBuyType'] = roundRow['ctBuyType'].iloc[0]
            case 'CT':
                vector['teammatesAlive'] = frameRow['ctAlivePlayers'].iloc[0]
                vector['enemiesAlive'] = frameRow['tAlivePlayers'].iloc[0]
                vector['teamEquipmentValue']= frameRow['ctEqVal'].iloc[0]
                vector['enemyEquipmentValue'] = frameRow['tEqVal'].iloc[0]
                vector['teamBuyType'] = roundRow['ctBuyType'].iloc[0]
                vector['enemyBuyType'] = roundRow['tBuyType'].iloc[0]
            case _:
                return Exception("Pass in a valid side")
        vector['clockTime'] = frameRow['seconds'].iloc[0]
        if len(bombEvents) > 0:
            vector['bombPlantStatus'] = tick < bombEvents.iloc[-1]['tick']
            vector['bombsitePlantedAt'] = bombEvents.iloc[-1]['bombSite']
        else:
            vector['bombPlantStatus'] = False
            vector['bombsitePlantedAt'] = 'N/A'
        vector['roundNumber'] = str(round)
        vector['tick'] = str(tick)
        vector['id'] = match['matchID'] + ":" + vector['roundNumber'] + ":" + vector['tick']


    def _extract_calculated_features(self, match, round, tick, side, vector):
        frameRow =  match['frames'].loc[(match['frames']['roundNum'] == round) & (match['frames']['tick'] == tick)]
        roundRow = match['rounds'].loc[(match['rounds']['roundNum'] == round)]
        playerFrames = match['playerFrames'][(match['playerFrames']['roundNum'] == round) & (match['playerFrames']['tick'] == tick)]
        match side:
            case 'T':
                vector['teammateHp'] = playerFrames[playerFrames['side'] == 'T'].hp.sum()
                vector['enemyHp'] = playerFrames[playerFrames['side'] == 'CT'].hp.sum()
                vector['teamUtilCount'] = playerFrames[playerFrames['side'] == 'T'].totalUtility.sum()
                vector['enemyUtilCount'] = playerFrames[playerFrames['side'] == 'CT'].totalUtility.sum()
                vector['playerCountDifferential'] = frameRow['tAlivePlayers'].iloc[0] - frameRow['ctAlivePlayers'].iloc[0]
                vector['TeamWin'] = 1 if roundRow['winningSide'].iloc[0] == 'T' else 0
            case 'CT':
                vector['teammateHp'] = playerFrames[playerFrames['side'] == 'CT'].hp.sum()
                vector['enemyHp'] = playerFrames[playerFrames['side'] == 'T'].hp.sum()
                vector['teamUtilCount'] = playerFrames[playerFrames['side'] == 'CT'].totalUtility.sum()
                vector['enemyUtilCount'] = playerFrames[playerFrames['side'] == 'T'].totalUtility.sum()
                vector['playerCountDifferential'] = frameRow['ctAlivePlayers'].iloc[0] - frameRow['tAlivePlayers'].iloc[0]
                vector['TeamWin'] = 1 if roundRow['winningSide'].iloc[0] == 'CT' else 0
            case _:
                return Exception("Pass in a valid side")


    def _extract_engineered_features(self, match, round, tick):
        pass