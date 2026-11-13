# to install: pip install moviepy

import os
from moviepy.editor import VideoFileClip


def process_videos(input_txt_path, output_folder, output_txt_path):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(input_txt_path, "r") as infile, open(output_txt_path, "w") as outfile:
        for line in infile:
            video_path = line.strip()
            if not os.path.exists(video_path):
                print(f"File {video_path} does not exist. Skipping.")
                continue

            try:
                # Load video
                clip = VideoFileClip(video_path)

                # Resize and crop
                # resized_clip = clip.resize(newsize=(1920, 1080))  # Resize to 1920x1080
                # cropped_clip = resized_clip.crop(height=1056)  # Crop height to 1056
                cropped_clip = clip.resize(newsize=(1920, 1056))  # Resize to 1920x1080

                # Prepare output path
                video_name = os.path.basename(video_path)
                output_path = os.path.join(output_folder, video_name)

                # Save the processed video
                cropped_clip.write_videofile(output_path, codec="libx264")

                # Write the output path to the text file
                outfile.write(f"{output_path}\n")

                # Close the video clips
                clip.close()
                # resized_clip.close()
                cropped_clip.close()

            except Exception as e:
                print(f"Failed to process {video_path}: {e}")


if __name__ == "__main__":
    input_txt_path = "/sensei-fs/users/hshariati/del/clineto/raw_videos_for_gen_extend.txt"  # Path to the input text file
    output_folder = "/sensei-fs/users/hshariati/del/clineto/demo_videos"  # Folder to save processed videos
    output_txt_path = "/sensei-fs/users/hshariati/del/clineto/demo_videos/processed_videos_for_gen_extend.txt"  # Path to the output text file

    process_videos(input_txt_path, output_folder, output_txt_path)
