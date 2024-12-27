For training data:
    -Overy every match:
        -going to loop over every round
            -and every tick that is unique in the frames data for that round in the features data. going to use that to create two perspectives and training input to my win probability model

For each round:
    For each tick:
        # Generate two mirror perspectives
        T_perspective = create_feature_vector(T_as_own_team)
        CT_perspective = create_feature_vector(CT_as_own_team)
        
        # Label based on round winner
        if T_won_round:
            T_perspective["won_round"] = 1
            CT_perspective["won_round"] = 0
        else:
            T_perspective["won_round"] = 0
            CT_perspective["won_round"] = 1

DIRECT FEATURES:
    Players Alive (from frames["t/ct"]["alivePlayers"])
    Team Equipment Values (tFreezeTimeEndEqVal/ctFreezeTimeEndEqVal)
    Buy Types (tBuyType/ctBuyType)
    Clock Time (from frames["clockTime"])
    Bomb Plant Status (frames["bombPlanted"])
    Bombsite (frames["bombsite"])
    Team Scores (tScore/ctScore)
    Round Number (roundNum)

