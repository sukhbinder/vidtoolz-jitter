import vidtoolz
import numpy as np
from moviepy import VideoClip, VideoFileClip, concatenate_videoclips
import os
import sys


def determine_output_path(input_file, output_file):
    input_dir, input_filename = os.path.split(input_file)
    name, _ = os.path.splitext(input_filename)

    if output_file:
        output_dir, output_filename = os.path.split(output_file)
        if not output_dir:  # If no directory is specified, use input file's directory
            return os.path.join(input_dir, output_filename)
        return output_file
    else:
        return os.path.join(input_dir, f"{name}_jitter.mp4")


def jitter_clip(clip, jitter_amount=5):
    def apply_jitter(frame, jitter_amount):
        jitter_x = np.random.randint(-jitter_amount, jitter_amount + 1)
        jitter_y = np.random.randint(-jitter_amount, jitter_amount + 1)
        new_frame = np.roll(frame, (jitter_x, jitter_y), axis=(1, 0))
        return new_frame

    # Apply the jitter effect to each frame of the video
    jittered_frames = [
        apply_jitter(frame, jitter_amount) for frame in clip.iter_frames()
    ]
    total_frames = len(jittered_frames)

    def make_frame(t):
        idx = int(t * clip.fps)
        if idx >= total_frames:
            idx = total_frames - 1  # Clamp to avoid overflow
        return jittered_frames[idx]

    jittered_clip = VideoClip(make_frame, duration=clip.duration).with_fps(clip.fps)
    return jittered_clip


def apply_jitter_effect(input_video, start_time, duration):
    clip = VideoFileClip(input_video)
    end_time = start_time + duration
    # Extract parts
    before = clip.subclipped(0, start_time)
    middle = clip.subclipped(start_time, end_time)
    after = clip.subclipped(end_time, clip.duration)
    # Apply jitter to the middle part
    jittered_middle = jitter_clip(middle, jitter_amount=10)
    # Concatenate the final clip
    final_clip = concatenate_videoclips(
        [before, jittered_middle, after], method="compose"
    )
    return final_clip, clip.fps


def create_parser(subparser):
    parser = subparser.add_parser(
        "jitter", description="Add jitter effect to a video using moviepy"
    )
    # Add subprser arguments here.
    parser.add_argument("input", type=str, help="Path to the input video file.")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Path to save the output video with the shake effect.",
    )
    parser.add_argument(
        "-st",
        "--start-time",
        type=float,
        required=True,
        help="Start time for the shake effect (in seconds).",
    )
    parser.add_argument(
        "-d",
        "--duration",
        type=float,
        default=0.5,
        help="Duration for the shake effect (in seconds). Default 0.5",
    )
    return parser


def write_file(video_with_text, output_video_path, fps):
    try:
        # Write the result to a file
        video_with_text.write_videofile(
            output_video_path,
            codec="libx264",
            fps=fps,
            audio_codec="aac",
            temp_audiofile="temp_audio.m4a",
            remove_temp=True,
            audio_bitrate="320k",
        )
    except Exception as e:
        sys.exit("Error writing video file: " + str(e))
    video_with_text.close()


class ViztoolzPlugin:
    """Add jitter effect to a vider using moviepy"""

    __name__ = "jitter"

    @vidtoolz.hookimpl
    def register_commands(self, subparser):
        self.parser = create_parser(subparser)
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        # add actual call here
        output = determine_output_path(args.input, args.output)
        # Call the function to add the shake effect
        final_clip, fps = apply_jitter_effect(
            args.input, args.start_time, args.duration
        )
        write_file(final_clip, output, fps)

    def hello(self, args):
        # this routine will be called when "vidtoolz "jitter is called."
        print("Hello! This is an example ``vidtoolz`` plugin.")


jitter_plugin = ViztoolzPlugin()
