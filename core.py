# 最小序列的长度
min_sequence_len = 10


# 查找相同子序列
def find_same_subsequences(list1: list, list2: list) -> list:
    subsequences = []

    for i in range(0, len(list1)):
        sub_range = (0, 0, 0)
        j = i
        while j < len(list1):
            if abs(list1[j] - list2[j - i]) < 2:
                if sub_range[1] == 0:
                    sub_range = (j, j + 1, i)
                else:
                    sub_range = (sub_range[0], j + 1, i)
                j += 1
            else:
                length = sub_range[1] - sub_range[0]
                if length >= min_sequence_len:
                    subsequences.append(sub_range)
                    # print(sub_range, i, j)
                sub_range = (0, 0, 0)
                j += 1


    return subsequences


# 查找最大的子序列
def find_max_subsequence(list1: list, list2: list) -> tuple:
    subsequences = find_same_subsequences(list1, list2)
    # print('subsequences', subsequences)
    max_length = 0
    max_sequence = (0, 0, 0)
    for sub_range in subsequences:
        length = sub_range[1] - sub_range[0]
        if length > max_length:
            max_sequence = sub_range
            max_length = length

    return max_sequence

# (未实现) 查找最佳子序列
def find_best_subsequence(list1: list, list2: list) -> tuple:
    subsequences = find_same_subsequences(list1, list2)
    # nope

# 计算数据熵（混乱程度）
def calc_entropy(list: list) -> list:
    pass


# ---------------------------------------

# 计算重合部分差异绝对值之和
def calc_sum_diff(list1: list, list2: list, shif: int) -> tuple:
    sum_diff = 0
    for j in range(len(list1) - shif, len(list1)):
        sum_diff += abs(list1[j] - list2[j - shif])

    return shif, sum_diff

# 查找重合位置
def find_coincide(list1: list, list2: list) -> int:
    sum_diff = []
    for i in range(0, len(list1)):
        sum_diff.append(calc_sum_diff(list1, list2, i))

    print(sum_diff)
    return 0
