from moviepy.editor import VideoClip as _VideoClip, \
    clips_array as _clips_array, \
    VideoFileClip as _VideoFileClip, \
    concatenate_videoclips as _concatenate_videoclips, \
    ColorClip as _ColorClip

from glob import glob as _glob


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
    assert len(video_clips_2d) > 0, "video_clips_2d must have at least one row"
    assert len(video_clips_2d[0]) > 0, "video_clips_2d must have at least one column"
    assert all([len(row) == len(video_clips_2d[0]) for row in video_clips_2d]), "video_clips_2d must have the same number of columns in each row"
    
    from utils import readVideoConfig as _readVideoConfig
    video_clips_2d = [[clip if isinstance(clip, _VideoClip) else _readVideoConfig(clip)
                       for clip in row] for row in video_clips_2d]
    max_duration = max(
        [clip.duration for row in video_clips_2d for clip in row])
    padded_clips_2d = [[_adjust_clip_duration(
        clip, max_duration) for clip in row] for row in video_clips_2d]

    # Arrange the clips in a grid
    final_clip = _clips_array(padded_clips_2d)
    return final_clip


def makeGrid(*, video_clips, grid_size: tuple[int, int]) -> _VideoClip:
    from utils import readVideoConfig as _readVideoConfig
    if isinstance(video_clips, dict):
        video_clips = _readVideoConfig(video_clips)

    assert len(video_clips) == grid_size[0] * \
        grid_size[1], "video_clips must have the same number of clips as the grid size"
    assert len(video_clips) > 0, "video_clips must have at least one clip"
    assert grid_size[0] > 0 and grid_size[1] > 0, "grid_size must be positive"
    video_clips_2d = []
    for i in range(grid_size[0]):
        row = []
        for j in range(grid_size[1]):
            row.append(video_clips[i * grid_size[1] + j])
        video_clips_2d.append(row)
    return makeGridView(video_clips_2d)


def _adjust_clip_duration(clip: _VideoClip, max_duration: float) -> _VideoClip:
    if clip.duration < max_duration:
        black_clip = _ColorClip((clip.size[0], clip.size[1]), col=(
            0, 0, 0), duration=max_duration - clip.duration)
        return _concatenate_videoclips([clip, black_clip])
    else:
        return clip


def readVideoFile(video_files: list[str]) -> _VideoClip:
    return _VideoFileClip(video_files, fps_source='fps')


def readVideoFiles(video_files: list[str]) -> list[_VideoClip]:
    return list(map(readVideoFile, video_files))


def readVideoFilePattern(video_file_pattern: str) -> _VideoClip:
    return readVideoFiles(_glob(video_file_pattern))
