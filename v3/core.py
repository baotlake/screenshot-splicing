import numpy as np
import math

def sampling_yuv(array):
    w = array.shape[1]
    # 16 * 3->3均值
    return np.vstack((
        np.average(array[:, np.linspace(20, w / 4, 16, dtype='int')], axis=1),
        np.average(array[:, np.linspace(w / 2, 5 * w / 8, 16, dtype='int')], axis=1),
        np.average(array[:, np.linspace(6 * w / 8, 7 * w / 8, 16, dtype='int')], axis=1),
    )).T


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

    ravel_o = array_all[:max + predict_y - ravel_len] if predict_y > 0 else array_all[ravel_len * 2:]

    return np.hstack((np.vstack([
        ravel_1,
        ravel_2[::-1]
    ]).T.ravel(), ravel_o))


# 预测计算最佳偏移值
def predict_translation_y(column, column2, predict):
    min_avg_diff = 2
    approach_count = 0
    min_diff = (
        0,
        np.average(np.abs(column - column2))
    )

    if min_diff[1] < min_avg_diff:
        return min_diff

    max_offset = column.shape[0] - 220
    for i in better_offset(max_offset, predict):
        diff_array = np.abs(column[i:] - column2[:-i]) if i > 0 else np.abs(column[:i] - column2[-i:])
        average_diff = np.average(diff_array)
        if average_diff < min_diff[1]:
            min_diff = (i, average_diff)

        if min_diff[1] < min_avg_diff:
            approach_count += 1
            # return min_diff
            if approach_count > 10:
                return min_diff
            elif average_diff < min_avg_diff / 4:
                return min_diff

    return min_diff


# 计算预测值 (frame_count, offset_y, diff)[]
def predict(list, idea_offset):
    if len(list) < 1:
        return 0, 0
    elif len(list) == 1:
        return 0, list[0][1]

    pre_data = list[-2]
    data = list[-1]

    offset_per_frame = data[1] / (data[0] - pre_data[0])
    if offset_per_frame == 0:
        if pre_data[1] == 0:
            return 3, 0
        else:
            return 0, pre_data[1]

    frame_distance = math.floor(idea_offset / abs(offset_per_frame * 1.5))
    drop_frame = max(min(frame_distance - 1, 3), 0)
    predict_y = int((drop_frame + 1) * offset_per_frame)
    return drop_frame, predict_y
