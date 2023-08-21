from moviepy.video.fx.crop import crop as _crop
from moviepy.editor import TextClip as _TextClip, \
    CompositeVideoClip as _CompositeVideoClip, \
    VideoClip as _VideoClip, \
    ColorClip as _ColorClip, \
    clips_array as _clips_array \



def crop(video_clip: _VideoClip, coords: tuple[int, int, int, int]) -> _VideoClip:
    assert len(coords) == 4, "coords must be a tuple of 4 integers"
    assert all([isinstance(coord, int) for coord in coords]
               ), "coords must be a tuple of 4 integers"
    assert coords[0] < coords[2], "coords[0] must be less than coords[2]"
    assert coords[1] < coords[3], "coords[1] must be less than coords[3]"
    assert all([coord >= 0 for coord in coords])
    assert coords[2] <= video_clip.size[0], "coords[2] must be less than the width of the video"
    assert coords[3] <= video_clip.size[1], "coords[3] must be less than the height of the video"

    return video_clip.crop(x1=coords[0], y1=coords[1], x2=coords[2], y2=coords[3])


def _zoomVideo(video_clip: _VideoClip, zoom_factor: float, center: tuple[int, int] = None) -> _VideoClip:
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
    caption_clip = _TextClip(
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
    caption_clip = caption_clip.set_position(
        ('center', 10)).set_duration(video_clip.duration)

    # Overlay the caption on the video
    final_video = _CompositeVideoClip([video_clip, caption_clip])
    return final_video


def title(video_clip: _VideoClip, title_text: str) -> _VideoClip:
    title_clip = _TextClip(
        title_text,
        fontsize=80,
        font='Arial',
        color='white',
        stroke_color='white',
        stroke_width=2,
        align='center',
        interline=1,
    )
    black_background = _ColorClip(
        (video_clip.size[0], title_clip.size[1]), col=(0, 0, 0))

    # Overlay the TextClip on the ColorClip
    caption_on_black = _CompositeVideoClip(
        [black_background, title_clip.set_position('center')]).set_duration(video_clip.duration)

    return _clips_array([[caption_on_black], [video_clip]])


def mute(video_clip: _VideoClip, is_mute: bool) -> _VideoClip:
    if is_mute:
        return video_clip.without_audio()
    else:
        return video_clip
