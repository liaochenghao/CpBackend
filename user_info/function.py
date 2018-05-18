# coding: utf-8
def get_constellation(month, day):
    """
    根据生日计算星座
    :param month: 月份
    :param day: 天数
    :return: 
    """
    dates = (21, 20, 21, 21, 22, 22, 23, 24, 24, 24, 23, 22)
    constellations = ("摩羯座", "水瓶座", "双鱼座", "白羊座", "金牛座", "双子座", "巨蟹座", "狮子座", "处女座", "天秤座", "天蝎座", "射手座", "摩羯座")
    if day < dates[month - 1]:
        return constellations[month - 1]
    else:
        return constellations[month]
