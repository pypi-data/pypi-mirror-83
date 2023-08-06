import pathlib
import dateutils


def is_newer(path1, path2):
    p1 = pathlib.Path(paht1)
    p2 = pathlib.Path(path2)

    t1 = p1.stat().st_mtime
    t2 = p2.stat().st_mtime

    return t1 > t2
