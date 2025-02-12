from typing import Any
from .const import DICT_STU, DICT_RANK

def get_stu_id(source: Any) -> int:
    """Return int student id by either id or name."""
    if isinstance(source, int):
        return source
    if source.isdigit():
        return int(source)
    for id, name in DICT_STU.items():
        if name == source:
            return id
    return 0

def get_stu_name(source: Any) -> str:
    """Return str student name by either id or name."""
    if isinstance(source, str):
        if not source.isdigit():
            return source
        source = int(source)
    for id, name in DICT_STU.items():
        if id == source:
            return name
    return str(source)

def get_total_rank(level: int, exp: int) -> int:
    """Return int total rank by level and exp."""
    return DICT_RANK.get(level, 0) + exp

def get_level_by_rank(value: int) -> tuple:
    """Return int level and exp by rank."""
    for level in sorted(DICT_RANK.keys(), reverse=True):
        rank = DICT_RANK[level]
        if value >= rank:
            return level, value - rank
    return 0, 0