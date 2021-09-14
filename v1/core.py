
# 计算重合部分差异绝对值之和
def calc_average_absolute_deviation(list1: list, list2: list, shift: int) -> tuple:
    sum_diff = 0
    for j in range(shift, len(list1)):
        sum_diff += abs(list1[j] - list2[j - shift])

    return shift, (sum_diff // (len(list1) - shift))


# 查找重合位置
def find_coincide(list1: list, list2: list) -> tuple:
    sum_diff_list = []
    for i in range(0, len(list1)):
        diff = calc_average_absolute_deviation(list1, list2, i)
        sum_diff_list.append(diff)

    # 查找"平均绝对差"最小的值， mix_diff = （<偏移值>，<平均绝对差>）
    mix_diff = sum_diff_list[0]
    for diff in sum_diff_list:
        if diff[1] < mix_diff[1]:
            mix_diff = diff

    print(mix_diff)
    return mix_diff[0]
