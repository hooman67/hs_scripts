import cv2
import pandas as pd
import os
from pathlib import Path

# Input and output paths
input_csv = "/sensei-fs/users/hshariati/del/v2v_v1.8_dva_460_just_horizantal.csv"
output_dir = "/sensei-fs/users/hshariati/del/last_2_s"
output_csv = "/sensei-fs/users/hshariati/del/last_2_s/v2v_v1.8_dva_460_just_horizantal_trimmed.csv"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Read the CSV file
df = pd.read_csv(input_csv)


def trim_video(video_path):
    # Open the video
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Calculate frames to keep (remove last 2 seconds)
    frames_to_remove = 2 * fps
    frames_to_keep = total_frames - frames_to_remove

    # Create output video path
    video_name = Path(video_path).name
    output_path = os.path.join(output_dir, f"trimmed_{video_name}")

    # Create VideoWriter object with H.264 codec
    fourcc = cv2.VideoWriter_fourcc(*"avc1")  # H.264 codec
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    if not out.isOpened():
        # Fallback to alternative H.264 codec name if 'avc1' is not available
        out.release()
        fourcc = cv2.VideoWriter_fourcc(*"H264")
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        if not out.isOpened():
            raise Exception("Failed to initialize video writer with H.264 codec")

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret or frame_count >= frames_to_keep:
            break

        out.write(frame)
        frame_count += 1

    # Release everything
    cap.release()
    out.release()

    return output_path


# Process each video and update paths
new_paths = []
for idx, row in df.iterrows():
    video_path = row["video"]
    print(f"Processing video {idx + 1}/{len(df)}: {video_path}")

    try:
        new_path = trim_video(video_path)
        new_paths.append(new_path)
    except Exception as e:
        print(f"Error processing {video_path}: {str(e)}")
        new_paths.append(None)

# Update the DataFrame with new paths
df["video"] = new_paths

# Save the updated CSV
df.to_csv(output_csv, index=False)
print(f"Processing complete. Updated CSV saved to: {output_csv}")
