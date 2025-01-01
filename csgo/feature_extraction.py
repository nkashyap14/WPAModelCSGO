from src.preprocessing import Preprocessor


if __name__ == "__main__":
    # Configuration dictionary
    config = {
        'loader': {
            'num_processes': 4,  # Number of processes for parallel processing
            'parse_rate': 128    # Parse rate for demo parser
        },
        'transformer': {
            # Any transformer specific config
        },
        'extractor': {
            # Any extractor specific config
        }
    }

    # Demo files to test out
    '''
    demo_files = ['D:\\CS_DEMOS\\003105352163501539569_1701770142_1_g2_vs_mousesports_inferno.dem',
    'D:\\CS_DEMOS\\003105575497505964289_1041781123_1_tsm_vs_g2_dust2.dem',
    'D:\\CS_DEMOS\\003105714961536516196_1827256016_1_mousesports_vs_g2_mirage.dem',
    'D:\\CS_DEMOS\\003105724614475514016_1321533067_1_mousesports_vs_g2_inferno.dem',
    'D:\\CS_DEMOS\\003105733442780791103_1310212764_1_mousesports_vs_g2_cache.dem',
    'D:\\CS_DEMOS\\100-thieves-vs-g2-m1-dust2.dem',
    'D:\\CS_DEMOS\\100-thieves-vs-g2-m1-mirage.dem',
    'D:\\CS_DEMOS\\100-thieves-vs-g2-m2-dust2.dem',
    'D:\\CS_DEMOS\\100-thieves-vs-g2-m2-vertigo.dem',
    'D:\\CS_DEMOS\\11_g2-nip_de_cache.dem',
    'D:\\CS_DEMOS\\12054_g2-kinguin-natus-vincere_de_train.dem',
    'D:\\CS_DEMOS\\12058_g2-kinguin-fnatic_de_cache.dem',
    'D:\\CS_DEMOS\\12059_g2-kinguin-fnatic_de_inferno.dem',
    'D:\\CS_DEMOS\\158_cloud9-g2-kinguin_de_cache.dem',
    'D:\\CS_DEMOS\\159_cloud9-g2-kinguin_de_train.dem',
    'D:\\CS_DEMOS\\160_cloud9-g2-kinguin_de_cbble.dem',
    'D:\\CS_DEMOS\\166_astralis-g2-kinguin_de_train.dem',
    'D:\\CS_DEMOS\\167_astralis-g2-kinguin_de_overpass.dem',
    'D:\\CS_DEMOS\\169_cloud9-g2-kinguin_de_cache.dem',
    'D:\\CS_DEMOS\\16_natus-vincere-g2_de_train.dem',
    'D:\\CS_DEMOS\\170_cloud9-g2-kinguin_de_train.dem',
    'D:\\CS_DEMOS\\173_clg-g2-kinguin_de_dust2.dem',
    'D:\\CS_DEMOS\\174_clg-g2-kinguin_de_inferno.dem',
    'D:\\CS_DEMOS\\175_clg-g2-kinguin_de_cbble.dem',
    'D:\\CS_DEMOS\\18_natus-vincere-g2_de_cbble.dem',
    'D:\\CS_DEMOS\\1917_virtus-pro-cloud9-g2a_de_overpass.dem',
    'D:\\CS_DEMOS\\1923_cloud9-g2a-team-envyus_de_dust2.dem',
    'D:\\CS_DEMOS\\1924_cloud9-g2a-team-envyus_de_cache.dem',
    'D:\\CS_DEMOS\\1934_cloud9-g2a-counter-logic-gaming_de_cache.dem',
    'D:\\CS_DEMOS\\1935_cloud9-g2a-counter-logic-gaming_de_dust2.dem',
    'D:\\CS_DEMOS\\DHCluj2015-clg-vs-navi-cbble.dem',
    'D:\\CS_DEMOS\\DHCluj2015-navi-vs-clg-inferno.dem',
    'D:\\CS_DEMOS\\DHCluj2015-navi-vs-clg-train.dem',
    'D:\\CS_DEMOS\\DHW13-GroupA-fnatic-vs-navi-mirage.dem',
    'D:\\CS_DEMOS\\DHW13-GroupA-lgb-vs-navi-mirage.dem',
    'D:\\CS_DEMOS\\DHW14-GroupD-navi-vs-flipside-mirage.dem',
    'D:\\CS_DEMOS\\DHW14-GroupD-navi-vs-flipside-overpass.dem',
    'D:\\CS_DEMOS\\DHW14-GroupD-virtuspro-vs-navi-nuke.dem',
    'D:\\CS_DEMOS\\DHW14-QF-navi-vs-dignitas-cobblestone.dem',
    'D:\\CS_DEMOS\\DHW14-QF-navi-vs-dignitas-mirage.dem',
    'D:\\CS_DEMOS\\DHW14-SF-ldlc-vs-navi-dust2.dem',
    'D:\\CS_DEMOS\\DHW14-SF-ldlc-vs-navi-inferno.dem',
    'D:\\CS_DEMOS\\EMSKato-GroupD-lgb-vs-navi-inferno.dem',
    'D:\\CS_DEMOS\\ESLOneCologne-GroupB-ldlc-vs-navi-inferno.dem',
    'D:\\CS_DEMOS\\ESLOneCologne-QF-fnatic-vs-navi-inferno.dem',
    'D:\\CS_DEMOS\\ESLOneCologne-QF-fnatic-vs-navi-nuke.dem',
    'D:\\CS_DEMOS\\ESLOneCologne-QF-navi-vs-fnatic-dust2.dem',
    'D:\\CS_DEMOS\\ESLOneCologne2015-envyus-vs-navi-inferno.dem',
    'D:\\CS_DEMOS\\ESLOneCologne2015-envyus-vs-navi-mirage.dem',
    'D:\\CS_DEMOS\\ESLOneCologne2015-fnatic-vs-navi-inferno-1.dem',
    'D:\\CS_DEMOS\\ESLOneCologne2015-navi-vs-clg-cobblestone-1.dem',
    'D:\\CS_DEMOS\\ESLOneCologne2015-navi-vs-titan-overpass-1.dem',
    'D:\\CS_DEMOS\\ESLOneKatowice2015-Groups-navi-vs-flipsid3-mirage.dem',
    'D:\\CS_DEMOS\\ESLOneKatowice2015-Groups-navi-vs-voxeminor-inferno.dem',
    'D:\\CS_DEMOS\\ESLOneKatowice2015-QF-envyus-vs-navi-cache.dem',
    'D:\\CS_DEMOS\\ESLOneKatowice2015-QF-envyus-vs-navi-cobblestone.dem',
    'D:\\CS_DEMOS\\ESLOneKatowice2015-QF-navi-vs-envyus-dust2.dem']
    '''

    demo_files = ['D:\\CS_DEMOS\\liquid-vs-gambit-mirage.dem',
    'D:\\CS_DEMOS\\liquid-vs-grayhound-m2-mirage.dem',
    'D:\\CS_DEMOS\\liquid-vs-hellraisers-m1-mirage.dem',
    'D:\\CS_DEMOS\\liquid-vs-heroic-m1-mirage.dem',
    'D:\\CS_DEMOS\\liquid-vs-mousesports-m1-mirage.dem',
    'D:\\CS_DEMOS\\liquid-vs-mousesports-m2-mirage.dem',
    'D:\\CS_DEMOS\\liquid-vs-movistar-riders-m1-mirage.dem',
    'D:\\CS_DEMOS\\liquid-vs-movistar-riders-m2-mirage.dem',
    'D:\\CS_DEMOS\\liquid-vs-natus-vincere-m3-mirage.dem',
    'D:\\CS_DEMOS\\liquid-vs-ninjas-in-pyjamas-m2-mirage.dem']





    # Create preprocessor instance
    preprocessor = Preprocessor(config)

    # Process files
    print("Attempting execution of preprocessor")
    try:
        result = preprocessor.process_files(demo_files, "testing_features.csv")
        #print(f"Processing completed. Results: {result}")
    except Exception as e:
        print(f"Error during processing: {e}")