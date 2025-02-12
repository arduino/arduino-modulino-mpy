def map_value(x: float | int, in_min: float | int, in_max: float | int, out_min: float | int, out_max: float | int) -> float | int:
    """
    Maps a value from one range to another.

    Args:
        x: The value to map.
        in_min: The minimum value of the input range.
        in_max: The maximum value of the input range.
        out_min: The minimum value of the output range.
        out_max: The maximum value of the output range.

    Returns:
        The mapped value as a float or int depending on the input.                
    """
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def map_value_int(x: float | int, in_min: float | int, in_max: float | int, out_min: float | int, out_max: float | int) -> int:
    """
    Maps a value from one range to another and returns an integer.

    Args:
        x: The value to map.
        in_min: The minimum value of the input range.
        in_max: The maximum value of the input range.
        out_min: The minimum value of the output range.
        out_max: The maximum value of the output range.

    Returns:
        The mapped value as an integer.
    """
    return int(map_value(x, in_min, in_max, out_min, out_max))
