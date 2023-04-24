cache = Cache()

def find_key(*args, **kwargs) -> str:
    pass


def cached_calc(func):
    def wrapper(*args, **kwargs):
        key = find_key(*args, **kwargs)
        if key not in cache:
            res = func(*args, **kwargs)
            cache[key] = res
        return cache[key]
    return wrapper
# arg11 = df
#
# df["time_window"] = [2022-01-01 00:00:00, 00-10:00,00-20:00,]
# 2022-01-01 00:00:00  2022-01-01 23:50:00
@cached_calc
def common_calc_1(
    arg11,
    arg12,
):
    pass

@cached_calc
def common_calc_2(
    arg21,
    arg22,
):
    pass

@cached_calc
def common_calc_3(
    arg31,
    arg32,
):
    pass

3 common calculation functions  minimal unit we can cache

2 kpi func1

#2 common calc is reused by two

def kpi_func1(
    arg1,
    arg2,
    arg3,
):

    arg1, arg2, arg3 -> arg11, arg12, arg21, arg22
    res1 = common_calc_1(
        arg11,
        arg12,
    )
    res2 = common_calc_2(
        arg21,
        arg22,
    )

def kpi_func2(
    arg4,
    arg5,
    arg6,
):
    arg4, arg5, arg6 -> arg21, arg22, arg31, arg32

    if coniditon1:
        common_calc_1_v1
    else:
        common_calc_1_v2

    res2 = common_calc_2(
        arg21,
        arg22,
    )
    res3 = common_calc_3(
        arg31,
        arg32,
    )


#
#
# """
# Compound Key =
#
# Project / Time Window <--> multiple Concept ID
#
# """
#
# "${site}----${concept}----{sequence-number}": status= 0
#
# 0 - t1 larger amound
#
# site, concept
#
# 2022-01-01 to 2022-01-02
# 2022-01-02 to 2022-01-03