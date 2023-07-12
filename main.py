import argparse
from utils import readVideoConfig

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Video Processing Tool")

    # Add the arguments
    parser.add_argument('ConfigPath', metavar='config_path', type=str, help='the path to the video config file')
    parser.add_argument('OutputPath', metavar='output_path', type=str, help='the path to save the output video')

    # Parse the arguments
    args = parser.parse_args()

    # Read the video config
    final_clip = readVideoConfig(args.ConfigPath)

    # Save the video
    final_clip.write_videofile(args.OutputPath)

if __name__ == "__main__":
    main()