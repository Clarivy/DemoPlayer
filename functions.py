from moviepy.editor import VideoClip as _VideoClip, \
    clips_array as _clips_array, \
    VideoFileClip as _VideoFileClip, \
    concatenate_videoclips as _concatenate_videoclips, \
    ColorClip as _ColorClip


def makeColView(video_clips: list[dict]) -> _VideoClip:
    from utils import readVideoConfig as _readVideoConfig
    video_clips = list(map(_readVideoConfig, video_clips))
    max_duration = max([clip.duration for clip in video_clips])
    padded_clips = [_adjust_clip_duration(
        clip, max_duration) for clip in video_clips]

    # Arrange the clips side by side
    final_clip = _clips_array([padded_clips])
    return final_clip


def makeGridView(video_clips_2d: list[list[dict]]) -> _VideoClip:
    from utils import readVideoConfig as _readVideoConfig
    video_clips_2d = [[_readVideoConfig(clip)
                       for clip in row] for row in video_clips_2d]
    max_duration = max(
        [clip.duration for row in video_clips_2d for clip in row])
    padded_clips_2d = [[_adjust_clip_duration(
        clip, max_duration) for clip in row] for row in video_clips_2d]

    # Arrange the clips in a grid
    final_clip = _clips_array(padded_clips_2d)
    return final_clip


def _adjust_clip_duration(clip: _VideoClip, max_duration: float) -> _VideoClip:
    if clip.duration < max_duration:
        black_clip = _ColorClip((clip.size[0], clip.size[1]), col=(
            0, 0, 0), duration=max_duration - clip.duration)
        return _concatenate_videoclips([clip, black_clip])
    else:
        return clip


def readVideoFiles(video_files: list[str]) -> list[_VideoClip]:
    return list(map(readVideoFile, video_files))


def readVideoFile(video_files: list[str]) -> _VideoClip:
    return _VideoFileClip(video_files, fps_source='fps')
