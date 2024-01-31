def hex_neighbors(hexagon: tuple[int,int], size: tuple[int,int]) -> list[tuple[int,int]]:
    """
    Returns the neighbors of a hexagon
    """
    x, y = hexagon
    res = []
    isLeftEdge, isRightEdge = (x == 0, x == size[0] - 1)
    isTopEdge, isBottomEdge = (y == 0, y == size[1] - 1)
    if not isLeftEdge:
        res.append((x - 1, y))
        if not isTopEdge:
            res.append((x - 1, y - 1))
    if not isRightEdge:
        res.append((x + 1, y))
        if not isBottomEdge:
            res.append((x + 1, y + 1))
    if not isTopEdge:
        res.append((x, y - 1))
    if not isBottomEdge:
        res.append((x, y + 1))
    return res