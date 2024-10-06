import subprocess
import os
import sys
import argparse

def get_video_duration(video_file, ffmpeg_path):
    """Get the total duration of the video using FFmpeg."""
    result = subprocess.run(
        [ffmpeg_path, '-i', video_file], 
        stderr=subprocess.PIPE, 
        stdout=subprocess.PIPE
    )
    output = result.stderr.decode('utf-8')

    # Find duration in the output
    duration_line = [line for line in output.splitlines() if 'Duration' in line][0]
    time_str = duration_line.split(' ')[3].split(',')[0]
    h, m, s = map(float, time_str.split(':'))
    duration_in_seconds = h * 3600 + m * 60 + s
    return duration_in_seconds

def extract_clips(video_file, output_dir, total_duration, preview_duration, num_clips, is_mute, ffmpeg_path, fds):
    """Extract equal parts from the video to create preview clips."""
    clip_duration = preview_duration / num_clips
    interval = total_duration / num_clips

    clip_paths = []
    for i in range(num_clips):
        print(f"Extracting clip {i+1}")
        start_time = interval * i
        output_clip = os.path.join(output_dir, f'clip{i+1}.mp4')
        clip_paths.append(output_clip)

        # Extract the clip using FFmpeg with re-encoding to ensure
        command = [
            ffmpeg_path, '-ss', str(start_time), '-i', video_file, '-t', str(clip_duration),
            '-c:v', 'libx264', '-crf', '23', '-preset', 'veryfast',
            '-c:a', 'aac', '-b:a', '128k'
        ]

        if is_mute:
            command.append('-an')

        command.extend([output_clip, '-y'])

        subprocess.run(command, stdout=fds[0], stderr=fds[1])

    return clip_paths

def concatenate_clips(clip_paths, output_preview, ffmpeg_path, fds):
    """Concatenate the extracted clips into one preview video."""
    with open('file_list.txt', 'w') as f:
        for clip in clip_paths:
            f.write(f"file '{clip}'\n")

    print("Concatening clips...")
    subprocess.run([
        ffmpeg_path, '-f', 'concat', '-safe', '0', '-i', 'file_list.txt', 
        '-c:v', 'libx264', '-crf', '23', '-preset', 'veryfast', 
        '-c:a', 'aac', '-b:a', '128k', '-movflags', 'faststart',  # Added movflags
        output_preview, '-y'
    ], stdout=fds[0], stderr=fds[1])

    # Clean up the file_list.txt and the individual clips
    os.remove('file_list.txt')
    for clip in clip_paths:
        os.remove(clip)


def create_video_preview(video_file:str, output_preview:str, is_mute:bool, preview_duration:int, num_clips:int, ffmpeg_path:str, fds):
    """Main function to create a preview from a video."""
    # Create a temporary directory to store the clips
    output_dir = './temp_clips'
    os.makedirs(output_dir, exist_ok=True)

    # Get the total duration of the video
    total_duration = get_video_duration(video_file, ffmpeg_path)
    print(f"Video's total duration : {total_duration}")

    # Extract clips and concatenate them into a preview
    clip_paths = extract_clips(video_file, output_dir, total_duration, preview_duration, num_clips, is_mute, ffmpeg_path, fds)
    concatenate_clips(clip_paths, output_preview, ffmpeg_path, fds)

    # Clean up the temporary directory
    os.rmdir(output_dir)

def is_valid_video_path(file_path):
    if os.path.exists(file_path):
        if file_path.lower().endswith('.mp4'):
            return True
    return False

def get_output_fd(is_verb):
    if (is_verb):
        return (sys.stdout, sys.stderr)
    else:
        return (subprocess.DEVNULL, subprocess.DEVNULL)

def show_config(args):
    print(
        f"You have chosen to process the video '{args['file']}' with the following options:\n"
        f"  - Output file:        '{args['output']}'\n"
        f"  - Mute audio:         {'enabled' if args['mute'] else 'disabled'}\n"
        f"  - Preview length:     {args['length']} seconds\n"
        f"  - Number of clips:    {args['number_clips']}\n"
        f"  - FFmpeg path:        '{args['ffmpeg_path']}'\n"
        f"  - Verbose mode:       {'enabled' if args['verbose'] else 'disabled'}."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a preview video from the original video by extracting multiple clips.")
    parser.add_argument("-f", "--file", type=str, required=True, help="Path to the input video file.")
    parser.add_argument("-o", "--output", type=str, required=False, default="preview.mp4", help="Path to save the generated preview video. Defaults to 'preview.mp4'.")
    parser.add_argument("-m", "--mute", action="store_true", required=False, help="Mute the preview video (remove the audio). Defaults to False.")
    parser.add_argument("-l", "--length", type=int, required=False, default=60, help="Total length (in seconds) of the preview video. Defaults to 60 seconds.")
    parser.add_argument("-n", "--number-clips", type=int, required=False, default=15, help="Number of clips to extract from the original video for the preview. Defaults to 15 clips.")
    parser.add_argument("--ffmpeg-path", type=str, required=False, default="ffmpeg", help="Optional custom path to the ffmpeg executable. Defaults to 'ffmpeg' in the system path.")
    parser.add_argument("-v", "--verbose", action="store_true", required=False, help="Enable verbose output for detailed logging. Defaults to False.")
    args = vars(parser.parse_args())

    if not is_valid_video_path(args["file"]):
        sys.exit(1)

    show_config(args)

    fds = get_output_fd(args['verbose'])
    # # Create a preview from the input video
    create_video_preview(args['file'], args['output'], args['mute'], args['length'], args['number_clips'], args['ffmpeg_path'], fds)
    print(f"Preview video saved as {args['output']}")

