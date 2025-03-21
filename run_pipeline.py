# run_pipeline.py
import os
from cosmos_generate import generate_cosmos_videos
from vila_analyze import analyze_and_rank
from join_videos import join_ranked_videos

def main():
    input_dir = "input_assets"
    output_dir = "output_assets"
    final_output = "final_output/final_memory_reel.mp4"

    os.makedirs("final_output", exist_ok=True)

    # Step 1: Generate videos from images
    cosmos_videos = generate_cosmos_videos(input_dir, output_dir)

    # Step 2: Rank videos with VILA
    ranked_videos = analyze_and_rank(cosmos_videos)

    # Step 3: Join the videos in order
    join_ranked_videos(ranked_videos, final_output)

if __name__ == "__main__":
    main()