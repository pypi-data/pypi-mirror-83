def size(mx):
    h = w = 0
    if mx and (h := len(mx)):
        if (row := mx[0]) is not None:
            w = len(row)
    return h, w
