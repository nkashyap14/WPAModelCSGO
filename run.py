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
    demo_files = ['D:\\CS_DEMOS\\003105321972028932195_0767047190_1_fnatic_vs_vexed_cobblestone.dem',
 'D:\\CS_DEMOS\\003105332913458118659_1512464813_1_luminosity_vs_cloud9_dust2.dem',
 'D:\\CS_DEMOS\\003105341507687677999_2120817205_1_tsm_vs_flipsid3_cache.dem',
 'D:\\CS_DEMOS\\003105352163501539569_1701770142_1_g2_vs_mousesports_inferno.dem',
 'D:\\CS_DEMOS\\003105365252414374069_0560812768_1_virtuspro_vs_liquid_cobblestone.dem',
 'D:\\CS_DEMOS\\003105376732861956362_1451569146_1_nip_vs_titan_cobblestone.dem',
 'D:\\CS_DEMOS\\003105386725103370542_0742292761_1_envyus_vs_dignitas_cobblestone.dem',
 'D:\\CS_DEMOS\\003105397499028832300_1022102112_1_natusvincere_vs_clg_cobblestone.dem',
 'D:\\CS_DEMOS\\003105507815263830017_1580923915_1_vexed_vs_cloud9_cobblestone.dem',
 'D:\\CS_DEMOS\\003105523418880016535_1142020467_1_flipsid3_vs_mousesports_overpass.dem',
 'D:\\CS_DEMOS\\003105535363184066773_0562556283_1_liquid_vs_nip_mirage.dem',
 'D:\\CS_DEMOS\\003105549276730622074_0458887648_1_dignitas_vs_clg_cobblestone.dem',
 'D:\\CS_DEMOS\\003105563911831683409_2082986634_1_fnatic_vs_luminosity_inferno.dem',
 'D:\\CS_DEMOS\\003105575497505964289_1041781123_1_tsm_vs_g2_dust2.dem',
 'D:\\CS_DEMOS\\003105586950036259130_0947387958_1_virtuspro_vs_titan_train.dem',
 'D:\\CS_DEMOS\\003105598155605934161_1717882650_1_envyus_vs_natusvincere_mirage.dem',
 'D:\\CS_DEMOS\\003105686876745367632_1807606374_1_cloud9_vs_fnatic_dust2.dem',
 'D:\\CS_DEMOS\\003105694790222610452_0569511311_1_cloud9_vs_fnatic_overpass.dem',
 'D:\\CS_DEMOS\\003105714961536516196_1827256016_1_mousesports_vs_g2_mirage.dem',
 'D:\\CS_DEMOS\\003105724614475514016_1321533067_1_mousesports_vs_g2_inferno.dem']


    # Create preprocessor instance
    preprocessor = Preprocessor(config)

    # Process files
    print("Attempting execution of preprocessor")
    try:
        result = preprocessor.process_files(demo_files)
        #print(f"Processing completed. Results: {result}")
    except Exception as e:
        print(f"Error during processing: {e}")
