import re


def fetch_number(string: str):
    """
    提取字符串中的数字

    可以提取的数字格式(优先级从高到低)：
    [0-9,.]+(?=亿)
    [0-9,.]+(?=万)
    [0-9,]+
    [0-9,.]+

    :param string 目标字符串
    :return: <float/int> 提取的数字
    """
    if pattern := re.search("[0-9,.]+(?=亿)", string):
        return int(float(pattern.group().replace(",", "")) * 10000 * 10000)
    elif pattern := re.search("[0-9,.]+(?=万)", string):
        return int(float(pattern.group().replace(",", "")) * 10000)
    elif pattern := re.search("[0-9,]+", string):
        return int(pattern.group().replace(",", ""))
    elif pattern := re.search("[0-9,.]+", string):
        return float(pattern.group().replace(",", ""))
    else:
        return None
