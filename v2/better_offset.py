import numpy as np


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

    print('ravel_1 shape', ravel_1.shape, ravel_1)
    print('ravel_2 shape', ravel_2.shape, ravel_2)

    ravel_o = array_all[:max + predict_y - ravel_len] if predict_y > 0 else array_all[ravel_len * 2:]

    return np.hstack((np.vstack([
        ravel_1,
        ravel_2[::-1]
    ]).T.ravel(), ravel_o))


# for i in range(-6, 6):
#     print(f'--------{i}---------')
#     print(better_offset(6, i))
#     print('\n\n')
