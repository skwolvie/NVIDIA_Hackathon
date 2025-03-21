# join_videos.py
import os
import ffmpeg

def join_ranked_videos(video_paths, output_path):
    temp_list_file = "temp_video_list.txt"
    with open(temp_list_file, "w") as f:
        for video in video_paths:
            f.write(f"file '{video}'\n")

    ffmpeg.input(temp_list_file, format='concat', safe=0).output(output_path, c='copy').run(overwrite_output=True)
    os.remove(temp_list_file)
    print(f"✅ Final stitched video saved at: {output_path}")
