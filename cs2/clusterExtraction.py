from src.cluster_processor import ClusterProcessor


if __name__ == '__main__':
    processor = ClusterProcessor(
        demo_dir="D:\\CS_2_DEMOS\\",
        output_dir="./cluster_data",
        batch_size=10
    )

    # Process all maps
    processor.process_all_maps()