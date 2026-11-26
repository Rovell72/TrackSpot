import re

_RANGE_RE = re.compile(r'^bytes=(\d*)-(\d*)$')


class RangeNotSatisfiable(Exception):
    pass


def parse_range(header, size):
    """Разбирает заголовок Range (один диапазон).

    Возвращает (start, end) включительно, либо None — если заголовка нет или он
    не поддерживается (тогда отдаём файл целиком). Бросает RangeNotSatisfiable -> 416.
    """
    if not header or size <= 0:
        return None
    m = _RANGE_RE.match(header.strip())
    if not m:
        return None
    first, last = m.groups()
    if not first and not last:
        return None
    if not first:                      # bytes=-N  (последние N байт)
        n = int(last)
        if n == 0:
            raise RangeNotSatisfiable
        return max(size - n, 0), size - 1
    start = int(first)
    end = int(last) if last else size - 1
    if start >= size or end < start:
        raise RangeNotSatisfiable
    return start, min(end, size - 1)
