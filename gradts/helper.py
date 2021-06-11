
def time_to(time, rtn_fmt="frames", fps=30):
    if isinstance(time, tuple) or isinstance(time, list):
        try:
            hours, minutes, seconds = time
        except ValueError:
            raise Exception("Invalid time format. ")
        if rtn_fmt in("frames", "seconds"):
            if rtn_fmt == "frames":
                return ((hours * (60 ** 2)) + (minutes * 60) + seconds) * fps
            elif rtn_fmt == "seconds":
                return (hours * (60 ** 2)) + (minutes * 60) + seconds
        else:
            raise Exception("Invalid return format.")
    elif isinstance(time, int):
        seconds = time // fps
        hours = seconds // (60 ** 2)
        minutes = (seconds // 60) % 60
        remaining_seconds = seconds % 60
        return hours, minutes, remaining_seconds
