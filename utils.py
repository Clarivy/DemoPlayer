from moviepy.editor import VideoClip
import json
import adjust
import functions


def readVideoConfigFile(config_file: str) -> VideoClip:
    assert isinstance(config_file, str), "config_file must be a string"

    with open(config_file) as f:
        config = json.load(f)

    return readVideoConfig(config)


def call_function(function_name: str, argument) -> VideoClip:
    assert isinstance(function_name, str), "function_name must be a string"
    assert hasattr(
        functions, function_name), "function_name must be a valid function name"
    video_function = getattr(functions, function_name)
    assert callable(
        video_function), "function_name must be a valid function name"
    if isinstance(argument, dict):
        return video_function(**argument)
    else:
        return video_function(argument)


def call_adjust(function_name: str, object, argument) -> VideoClip:
    assert isinstance(function_name, str), "function_name must be a string"
    assert hasattr(
        adjust, function_name), "function_name must be a valid function name"
    adjust_function = getattr(adjust, function_name)
    assert callable(
        adjust_function), "function_name must be a valid function name"
    return adjust_function(object, argument)


def readVideoConfig(config: dict) -> VideoClip:
    if isinstance(config, VideoClip):
        return config
    assert isinstance(config, dict), "config must be a dictionary"
    assert "function" in config, "config must have a function key"

    function = config["function"]
    argument = config["argument"] if "argument" in config else None
    result = call_function(function, argument)

    if config.get("adjust"):
        for key in config["adjust"]:
            result = call_adjust(key, result, config["adjust"][key])

    return result
