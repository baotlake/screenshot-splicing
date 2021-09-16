import numpy as np


# 采样函数
def sampling(array):
    shape = array.shape
    w = shape[1]
    # 瞎试
    # return np.dot(np.std(array, axis=1), [0.2989, 0.5870, 0.1140])

    # 全部比较 uint8
    # return np.average(array, axis=2).astype('uint8')

    #  全部比较
    # return np.dot(array, [0.2989, 0.5870, 0.1140])

    # 横向平均灰度值
    # return np.dot(np.average(array, axis=1), [0.2989, 0.5870, 0.1140])

    # 16 * 3->3均值
    return np.vstack((
        np.average(np.dot(array[:, np.linspace(20, w / 4, 16, dtype='int'), :], [0.2989, 0.5870, 0.1140]), axis=1),
        np.average(np.dot(array[:, np.linspace(w / 2, 5 * w / 8, 16, dtype='int'), :], [0.2989, 0.5870, 0.1140]),
                   axis=1),
        np.average(np.dot(array[:, np.linspace(6 * w / 8, 7 * w / 8, 16, dtype='int'), :], [0.2989, 0.5870, 0.1140]),
                   axis=1),
    )).T

    # 8->1均值
    return np.average(np.dot(array[:, [113, 135, 167, 199, 201, 223, 265, 297], :], [0.2989, 0.5870, 0.1140]), axis=1)

    # x=213, 灰度值
    return np.dot(array[:, 213, :], [0.2989, 0.5870, 0.1140])


# 根据预测值,生成一个最佳的偏移序列
def better_offset(max, predict_y):
    array_positive = np.arange(1, max + 1, 1)
    array_negative = np.arange(-max, 0, 1)
    array_all = np.hstack((array_negative, array_positive))

    if predict_y == 0:
        return np.vstack((
            array_all[: max][::-1],
            array_all[max:]
        )).T.ravel()

    ravel_len = max - abs(predict_y) + 1 if predict_y > 0 else \
        max - abs(predict_y)
    # 正向
    ravel_1 = array_all[max + predict_y - 1:] if predict_y > 0 else \
        array_all[max - abs(predict_y): ravel_len * 2]
    # 负向
    ravel_2 = array_all[max + predict_y - 1 - ravel_len: max + predict_y - 1] if predict_y >= 0 else \
        array_all[: ravel_len]

    # print('ravel_1 shape', ravel_1.shape, ravel_1)
    # print('ravel_2 shape', ravel_2.shape, ravel_2)

    ravel_o = array_all[:max + predict_y - ravel_len] if predict_y > 0 else array_all[ravel_len * 2:]

    return np.hstack((np.vstack([
        ravel_1,
        ravel_2[::-1]
    ]).T.ravel(), ravel_o))


# 计算最佳偏移值
def translation_y(column, column2):
    min_diff_y = (
        0,
        np.average(np.abs(column - column2))
    )
    if min_diff_y[1] < 1:
        return min_diff_y

    max = column.shape[0]

    for i in np.arange(1, max - 400):
        diff_array = np.abs(column[i:] - column2[:-i])
        average_diff = np.average(diff_array)
        # print('diff ', average_diff)
        if average_diff < 1:
            # print('break ', i)
            return i, average_diff
        if average_diff < min_diff_y[1]:
            min_diff_y = (i, average_diff)

        # -----逆向滑动 比较---
        diff_array = np.abs(column[:-i] - column2[i:])
        average_diff = np.average(diff_array)
        # print('diff ', average_diff)
        if average_diff < 1:
            # print('break ', i)
            return -i, average_diff
        if average_diff < min_diff_y[1]:
            min_diff_y = (-i, average_diff)

    return min_diff_y


# 预测计算最佳偏移值
def predict_translation_y(column, column2, predict):
    min_diff_y = (
        0,
        np.average(np.abs(column - column2))
    )

    if min_diff_y[1] < 2:
        return min_diff_y

    max = column.shape[0] - 400
    for i in better_offset(max, predict):
        if i > 0:
            diff_array = np.abs(column[i:] - column2[:-i])
            average_diff = np.average(diff_array)
            # print('diff ', average_diff)
            if average_diff < 2:
                # print('break ', i)
                return i, average_diff
            if average_diff < min_diff_y[1]:
                min_diff_y = (i, average_diff)
        else:
            diff_array = np.abs(column[:i] - column2[-i:])
            average_diff = np.average(diff_array)
            # print('diff ', average_diff)
            if average_diff < 2:
                # print('break ', i)
                return i, average_diff
            if average_diff < min_diff_y[1]:
                min_diff_y = (i, average_diff)

    return min_diff_y
