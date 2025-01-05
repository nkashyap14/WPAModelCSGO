from src.preprocessing import Preprocessor

if __name__ == "__main__":

    demo_files = ['D:\\CS_2_DEMOS\\ence-vs-gamerlegion-m1-ancient.dem',
 'D:\\CS_2_DEMOS\\ence-vs-gamerlegion-m1-nuke_87081.dem',
 'D:\\CS_2_DEMOS\\ence-vs-gamerlegion-m2-overpass.dem',
 'D:\\CS_2_DEMOS\\ence-vs-gamerlegion-m2-overpass_87081.dem',
 'D:\\CS_2_DEMOS\\ence-vs-havu-nuke.dem',
 'D:\\CS_2_DEMOS\\ence-vs-heroic-m1-ancient.dem',
 'D:\\CS_2_DEMOS\\ence-vs-heroic-m2-nuke.dem',
 'D:\\CS_2_DEMOS\\ence-vs-heroic-m3-vertigo.dem',
 'D:\\CS_2_DEMOS\\ence-vs-heroic-m4-dust2.dem',
 'D:\\CS_2_DEMOS\\ence-vs-lynn-vision-anubis-p1.dem',
 'D:\\CS_2_DEMOS\\ence-vs-lynn-vision-anubis-p2.dem',
 'D:\\CS_2_DEMOS\\ence-vs-monte-m1-nuke.dem',
 'D:\\CS_2_DEMOS\\ence-vs-monte-m2-vertigo.dem',
 'D:\\CS_2_DEMOS\\ence-vs-natus-vincere-m1-anubis.dem',
 'D:\\CS_2_DEMOS\\ence-vs-natus-vincere-m2-ancient.dem',
 'D:\\CS_2_DEMOS\\ence-vs-natus-vincere-m3-nuke.dem',
 'D:\\CS_2_DEMOS\\ence-vs-ninjas-in-pyjamas-m1-nuke.dem',
 'D:\\CS_2_DEMOS\\ence-vs-ninjas-in-pyjamas-m2-overpass.dem',
 'D:\\CS_2_DEMOS\\ence-vs-ninjas-in-pyjamas-m3-ancient.dem',
 'D:\\CS_2_DEMOS\\ence-vs-red-canids-m1-ancient.dem']

    # Create preprocessor instance
    preprocessor = Preprocessor()

    # Process files
    print("Attempting execution of preprocessor")
    try:
        result = preprocessor.process_files(demo_files)
        #print(f"Processing completed. Results: {result}")
    except Exception as e:
        print(f"Error during processing: {e}")