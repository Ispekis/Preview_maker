# Preview Maker

**Preview maker** is a Python script that creates a preview video by extracting multiple clips from an original video file. It allows users to customize the output file, total length of the preview, and the number of clips to extract. Additional features include muting the audio, setting a custom path for the FFmpeg executable, and enabling verbose output for detailed logging.

## Features

- Specify the input video file.
- Choose the output file name.
- Set the total length of the preview video.
- Define the number of clips to extract.
- Mute audio if desired.
- Optionally specify a custom path for FFmpeg.
- Enable verbose mode for detailed logging.

## Requirements

- Python 3.x
- FFmpeg installed on your system (make sure it's in your system PATH or provide the path using the `--ffmpeg-path` option).

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/Ispekis/Preview_maker.git
   cd Preview_maker
   ```

2. Install required packages (if any):
   ```bash
   pip install -r requirements.txt
   ```

3. Run the script with the required arguments:
   ```bash
   python preview_maker.py -f <input_video_file> [options]
   ```

### Options

- `-f`, `--file`: Path to the input video file (required).
- `-o`, `--output`: Path to save the generated preview video (optional, defaults to `preview.mp4`).
- `-m`, `--mute`: Mute the preview video (optional).
- `-l`, `--length`: Total length (in seconds) of the preview video (optional, defaults to `60`).
- `-n`, `--number-clips`: Number of clips to extract from the original video (optional, defaults to `15`).
- `--ffmpeg-path`: Optional custom path to the FFmpeg executable (defaults to `ffmpeg` in the system PATH).
- `-v`, `--verbose`: Enable verbose output for detailed logging (optional, defaults to `False`).

### Example

```bash
python preview_maker.py -f input_video.mp4 -o output_preview.mp4 -l 30 -n 5 -m -v
```

This command will generate a preview video from `input_video.mp4`, save it as `output_preview.mp4`, set the length to 30 seconds, extract 5 clips, mute the audio, and enable verbose output.

<!-- ## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. -->
