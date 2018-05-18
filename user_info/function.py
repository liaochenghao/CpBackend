# coding: utf-8
def get_constellation(month, day):
    """
    根据生日计算星座
    :param month: 月份
    :param day: 天数
    :return: 
    """
    dates = (21, 20, 21, 21, 22, 22, 23, 24, 24, 24, 23, 22)
    constellations = ("摩羯", "水瓶", "双鱼", "白羊", "金牛", "双子", "巨蟹", "狮子", "处女", "天秤", "天蝎", "射手", "摩羯")
    if day < dates[month - 1]:
        return constellations[month - 1]
    else:
        return constellations[month]
