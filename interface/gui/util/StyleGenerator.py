def _clamp(val, minimum=0, maximum=255):
    """ helper function to make sure that the rgb color is within 
        the range 0 to 255 """
    if val < minimum:
        return minimum
    if val > maximum:
        return maximum
    return val

def colorScale(hexstr, scalefactor):
    """
    Scales a hex string by ``scalefactor``. Returns scaled hex string.
    To darken the color, use a float value between 0 and 1.
    To brighten the color, use a float value greater than 1.
    """

    hexstr = hexstr.strip('#')

    if scalefactor < 0 or len(hexstr) != 6:
        return hexstr

    r, g, b = int(hexstr[:2], 16), int(hexstr[2:4], 16), int(hexstr[4:], 16)

    r = int(_clamp(r * scalefactor))
    g = int(_clamp(g * scalefactor))
    b = int(_clamp(b * scalefactor))
 
    return "#%02x%02x%02x" % (r, g, b)
