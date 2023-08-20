from moviepy.video.fx.crop import crop as _crop
from moviepy.editor import TextClip as _TextClip, \
    CompositeVideoClip as _CompositeVideoClip, \
    VideoClip as _VideoClip


def crop(video_clip: _VideoClip, coords: tuple[int, int, int, int]) -> _VideoClip:
    print("Cropping video")
    return video_clip.crop(x1=coords[0], y1=coords[1], x2=coords[2], y2=coords[3])


def _zoomVideo(video_clip: _VideoClip, zoom_factor: int, center: tuple[int, int] = None) -> _VideoClip:
    width, height = video_clip.size
    if center is None:
        center = (width // 2, height // 2)

    new_width, new_height = width // zoom_factor, height // zoom_factor

    x1 = center[0] - new_width // 2
    y1 = center[1] - new_height // 2
    x2 = center[0] + new_width // 2
    y2 = center[1] + new_height // 2

    return _crop(video_clip, x1, y1, x2, y2).resize((width, height))


def zoom(video_clip: _VideoClip, zoom_factor: int):
    return video_clip.fx(_zoomVideo, zoom_factor)


def subclip(video_clip: _VideoClip, time_range: tuple[float, float]) -> _VideoClip:
    return video_clip.subclip(time_range[0], time_range[1])


def caption(video_clip: _VideoClip, caption_text: str) -> _VideoClip:
    caption = _TextClip(
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
    caption = caption.set_position(
        ('center', 10)).set_duration(video_clip.duration)

    # Overlay the caption on the video
    final_video = _CompositeVideoClip([video_clip, caption])
    return final_video


def mute(video_clip: _VideoClip, is_mute: bool) -> _VideoClip:
    if is_mute:
        return video_clip.without_audio()
    else:
        return video_clip
