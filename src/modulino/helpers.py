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

def map_value_int(x: int, in_min: int, in_max: int, out_min: int, out_max: int, round_result: bool = False) -> int:
    """
    Maps an integer value from one range to another using integer arithmetic.

    Args:
        x: The integer value to map.
        in_min: The minimum value of the input range.
        in_max: The maximum value of the input range.
        out_min: The minimum value of the output range.
        out_max: The maximum value of the output range.
        round_result: If True, the result will be rounded to the nearest integer.

    Returns:
        The mapped integer value.
    """
    if in_max == in_min:
        raise ValueError("Input range cannot be zero.")

    # Work entirely with integers
    in_span : int = in_max - in_min
    out_span : int = out_max - out_min
    numerator : int = (x - in_min) * out_span

    if round_result:
        # Add half the divisor to get rounding instead of truncation
        numerator += in_span // 2 if numerator >= 0 else -(in_span // 2)

    return out_min + numerator // in_span

def constrain(value: float | int, min_value: float | int, max_value: float | int) -> float | int:
    """
    Constrains a value to be within a specified range.

    Args:
        value: The value to constrain.
        min_value: The minimum allowable value.
        max_value: The maximum allowable value.

    Returns:
        The constrained value.
    """
    return max(min_value, min(value, max_value))