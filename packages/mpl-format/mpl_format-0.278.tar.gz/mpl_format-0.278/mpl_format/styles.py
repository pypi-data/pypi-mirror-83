from enum import Enum


class LineStyle(Enum):

    solid = 1
    dashed = 2
    dashdot = 3
    dotted = 4


class CapStyle(Enum):

    butt = 1
    round = 2
    projecting = 3


class JoinStyle(Enum):

    miter = 1
    round = 2
    bevel = 3
