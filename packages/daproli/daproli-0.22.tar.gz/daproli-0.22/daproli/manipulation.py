from .utils import _get_return_type


def windowed(data, size, step=1, ret_type=None):
    '''
    dp.windowed applies a window function to a collection of data items.

    Parameters
    -----------
    :param data: an iterable collection of data
    :param size: the window size
    :param step: the window step
    :param ret_type: if provided the used return type, otherwise ret_type(data)
    :return: the windowed data list

    Examples
    -----------
    >>> import daproli as dp
    >>> numbers = range(10)
    >>> dp.windowed(numbers, 2, step=2)
    [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]
    '''
    if ret_type is None: ret_type = _get_return_type(data)
    return [ret_type(data[i:i+size]) for i in range(0, len(data)-(size-1), step)]


def flatten(data, ret_type=None):
    '''
    dp.flatten applies a flatten function to a collection of data items.

    Parameters
    -----------
    :param data: an iterable collection of data
    :param ret_type: if provided the used return type, otherwise ret_type(data)
    :return: the flattened data collection

    Examples
    -----------
    >>> import daproli as dp
    >>> dp.flatten([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    '''
    if ret_type is None: ret_type = _get_return_type(data)
    return ret_type([item for sub in data for item in sub])
