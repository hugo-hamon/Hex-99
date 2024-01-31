def hex_neighbors(hexagon: tuple[int,int], size: tuple[int,int]) -> list[tuple[int,int]]:
    """
    Returns the neighbors of a hexagon
    """
    x, y = hexagon
    res = []
    if not (x == 0):
        res.append((x - 1, y))
    if not (x == size[0] - 1):
        res.append((x + 1, y))
    if not (y == 0):
        res.append((x, y - 1))
    if not (y == size[1] - 1):
        res.append((x, y + 1))
    if not (x == 0) and not (y == size[1] - 1):
        res.append((x - 1, y + 1))
    if not (x == size[0] - 1) and not (y == 0):
        res.append((x + 1, y - 1))
    return res