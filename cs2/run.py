from src.preprocessing import Preprocessor

if __name__ == "__main__":

    demo_files = ['D:\\CS_2_DEMOS\\astralis-vs-spirit-m1-ancient.dem',
 'D:\\CS_2_DEMOS\\astralis-vs-spirit-m1-dust2.dem',
 'D:\\CS_2_DEMOS\\astralis-vs-spirit-m2-dust2.dem',
 'D:\\CS_2_DEMOS\\astralis-vs-spirit-m2-vertigo.dem',
 'D:\\CS_2_DEMOS\\astralis-vs-spirit-m3-ancient.dem',
 'D:\\CS_2_DEMOS\\astralis-vs-spirit-m3-mirage.dem',
 'D:\\CS_2_DEMOS\\astralis-vs-the-mongolz-inferno.dem',
 'D:\\CS_2_DEMOS\\astralis-vs-virtus-pro-m1-inferno.dem',
 'D:\\CS_2_DEMOS\\astralis-vs-virtus-pro-m2-dust2.dem',
 'D:\\CS_2_DEMOS\\astralis-vs-virtus-pro-m2-mirage.dem',]

    # Create preprocessor instance
    preprocessor = Preprocessor()

    # Process files
    print("Attempting execution of preprocessor")
    try:
        result = preprocessor.process_files(demo_files)
        #print(f"Processing completed. Results: {result}")
    except Exception as e:
        print(f"Error during processing: {e}")