from awpy import Demo
import numpy as np

class Extractor:
    def __init__(self):
        pass

    def extractFeatures(self, demos: Demo):
        """
        Will take in matches which represents a list of parsed counter strike games Each individual game is a 
        dictionary with a set of keys. The relevant keys to us are in turn mapped to a dataframe which contains data
        related to the specific match of the type specified by the keys
        Proceeds to extract features from each individual match relevant to the feature vector for the counter strike WPA model
        """

        return self._extractFeature(demos)
    
    def _calculate_average_distance_to_centroid(self, coordinates):
        # Convert list of coordinates to a numpy array
        coords_array = np.array(coordinates)

        # Calculate the centroid (mean position)
        centroid = np.mean(coords_array, axis=0)

        # Calculate distances from each point to the centroid
        distances = np.linalg.norm(coords_array - centroid, axis=1)

        # Calculate the average distance
        average_distance = np.mean(distances)

        return average_distance

    def _extractFeature(self, demo: Demo):
        rounds = demo.rounds
        ticks = demo.ticks
        smokes = demo.smokes
        kills = demo.kills
        infernos = demo.infernos
        vectors = []
        for round in rounds['round'].unique():
            startTick, endTick = rounds[rounds['round'] == round]['freeze_end'].iloc[0], rounds[rounds['round'] == round]['end'].iloc[0]
            roundSmokes = smokes[(smokes['round'] == round)]
            roundInfernos = infernos[(infernos['round'] == round)]
            currTicks = ticks[(ticks['tick'] >= startTick) & (ticks['tick'] <= endTick)]
            roundKills = kills[kills['round'] == round]
            bombEvents = demo.bomb[demo.bomb['round'] == round]
            for tick in currTicks.tick.unique():
                tickData = currTicks[currTicks['tick'] == tick]
                killsToPoint = roundKills[roundKills['tick'] <= tick]
                ctTicks, tTicks = tickData[tickData['team_name'] == 'CT'], tickData[tickData['team_name'] == 'TERRORIST']
                vector = {}
                vector['ctEquipVal'] = ctTicks.current_equip_value.sum()
                vector['tEquipVal'] = tTicks.current_equip_value.sum()
                vector['tPlayersAlive'] = len(tTicks[tTicks['health'] > 0])
                vector['ctPlayersAlive'] = len(ctTicks[ctTicks['health'] > 0])
                vector['tHPRemaining'] = tTicks.health.sum()
                vector['ctHPRemaining'] = ctTicks.health.sum()
                vector['bombPlanted'] = tickData.iloc[0].is_bomb_planted
                vector['tFlashDuration'] = tTicks.flash_duration.mean()
                vector['ctFlashDuration'] = ctTicks.flash_duration.mean()
                vector['activeTSmokes'] = len(roundSmokes[(roundSmokes['start_tick'] <= tick) & (roundSmokes['end_tick'] >= tick) & (roundSmokes['thrower_team_name'] == 'TERRORIST')])
                vector['activeCTSmokes'] = len(roundSmokes[(roundSmokes['start_tick'] <= tick) & (roundSmokes['end_tick'] >= tick) & (roundSmokes['thrower_team_name'] == 'CT')])
                vector['activeTInfernos'] = len(roundInfernos[(roundInfernos['start_tick'] <= tick) & (roundInfernos['end_tick'] >= tick) & (roundInfernos['thrower_team_name'] == 'TERRORIST')])
                vector['activeCTInfernos'] = len(roundInfernos[(roundInfernos['start_tick'] <= tick) & (roundInfernos['end_tick'] >= tick) & (roundInfernos['thrower_team_name'] == 'CT')])
                
                vector['tAVGDist'] = self._calculate_average_distance_to_centroid((tTicks.X.values, tTicks.Y.values, tTicks.Z.values))
                vector['ctAVGDist'] = self._calculate_average_distance_to_centroid((ctTicks.X.values, ctTicks.Y.values, ctTicks.Z.values))

                vector['killDifferential'] = len(roundKills[roundKills['attacker_team_name'] == 'CT']) - len(roundKills[roundKills['attacker_team_name'] == 'TERRORIST'])
                vector['ctDefuseKitCount'] = ctTicks.has_defuser.sum()
                
                if not bombEvents.empty:
                    vector['bombPlantSite'] = bombEvents.site.iloc[0]
                else:
                    vector['bombPlantSite'] = 'NA'
                #vector['teamBombsiteDistance']
                if rounds[rounds['round'] == round]['winner'].iloc[0] == 'CT':
                    vector['TeamWin'] = 1 
                else:
                    vector['TeamWin'] = 0
                vectors.append(vector)
        return vectors