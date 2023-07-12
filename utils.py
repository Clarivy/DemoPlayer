from moviepy.editor import VideoClip, TextClip, CompositeVideoClip, clips_array, VideoFileClip
from moviepy.video.fx.crop import crop
import json

def makeCaptionClip(video_clip: VideoClip, caption_text: str) -> VideoClip:
    caption = TextClip(
        caption_text,
        fontsize=40,
        font='Arial',
        color='white',
        stroke_color='white',
        stroke_width=2,
        align='center',
        interline=1,
    )

    # Position the caption at the top center of the video with a small margin from the top
    caption = caption.set_position(('center', 10)).set_duration(video_clip.duration)

    # Overlay the caption on the video
    final_video = CompositeVideoClip([video_clip, caption])
    return final_video

def makeClipCollection(video_clips: list[VideoClip]) -> VideoClip:
    # Make sure all clips have the same duration
    min_duration = min([clip.duration for clip in video_clips])
    trimmed_clips = [clip.subclip(0, min_duration) for clip in video_clips]

    # Arrange the clips side by side
    final_clip = clips_array([trimmed_clips])
    return final_clip

def cropVideo(video_clip: VideoClip, coords: tuple[int, int, int, int]) -> VideoClip:
    return video_clip.crop(x1=coords[0], y1=coords[1], x2=coords[2], y2=coords[3])

def _zoomVideo(video_clip: VideoClip, zoom_factor: int, center: tuple[int, int] = None) -> VideoClip:
    width, height = video_clip.size
    if center is None:
        center = (width // 2, height // 2)

    new_width, new_height = width // zoom_factor, height // zoom_factor

    x1 = center[0] - new_width // 2
    y1 = center[1] - new_height // 2
    x2 = center[0] + new_width // 2
    y2 = center[1] + new_height // 2

    return crop(video_clip, x1, y1, x2, y2).resize((width, height))

def zoomVideo(video_clip: VideoClip, zoom_factor: int):
    return video_clip.fx(_zoomVideo, zoom_factor)

def makeSubclip(video_clip: VideoClip, time_range: tuple[float, float]) -> VideoClip:
    return video_clip.subclip(time_range[0], time_range[1])

def readVideoFiles(video_files: list[str]) -> list[VideoClip]:
    return list(map(VideoFileClip, video_files))

def readVideoConfig(config_file: str) -> VideoClip:
    with open(config_file) as f:
        config = json.load(f)

    video_clips = []
    for video_config in config:
        video_clip = VideoFileClip(video_config['path'], fps_source='fps')
        if 'subclip' in video_config:
            video_clip = makeSubclip(video_clip, video_config['subclip'])
        if video_config.get("mute", False):
            video_clip = video_clip.without_audio()
        if 'crop' in video_config:
            video_clip = cropVideo(video_clip, video_config['crop'])
        if 'zoom' in video_config:
            video_clip = zoomVideo(video_clip, video_config['zoom'])
        if 'caption' in video_config:
            video_clip = makeCaptionClip(video_clip, video_config['caption'])
        video_clips.append(video_clip)
    
    return makeClipCollection(video_clips)
