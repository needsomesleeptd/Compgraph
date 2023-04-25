def is_fully_visible(line_point_left, line_point_right, rect_point_left, rect_point_right):  # [0] -x, [1] - y
    if (line_point_left[0] < rect_point_left[0] or line_point_left[0] > rect_point_right[0]):
        return False
    elif (line_point_right[0] < rect_point_left[0] or line_point_right[0] > rect_point_right[0]):
        return False
    elif (line_point_right[1] < rect_point_left[1] or line_point_right[1] > rect_point_right[1]):
        return False
    elif (line_point_left[1] < rect_point_left[1] or line_point_left[1] > rect_point_right[1]):
        return False
    return True

def is_fully_invisible(line_point_left, line_point_right, rect_point_left, rect_point_right):  # [0] -x, [1] - y
    if (line_point_left[0] < rect_point_left[0] and line_point_right[0] < rect_point_left[0]):
        return True
    elif (line_point_left[0] > rect_point_right[0] and line_point_right[0] > rect_point_right[0]):
        return True
    elif (line_point_left[1] < rect_point_left[1] and line_point_right[0] < rect_point_left[1]):
        return True
    elif (line_point_left[1] > rect_point_right[1] and line_point_right[0] > rect_point_right[1]):
        return True
    return False



