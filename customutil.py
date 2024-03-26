def map_value(current_min: int, current_max: int,
              new_min: int, new_max: int, value: float)->float:
    """Remap value from one range to another"""
    current_range = current_max - current_min
    new_range = new_max - new_min

    ratio = (value-current_min)/current_range
    return (new_min + new_range) * ratio

