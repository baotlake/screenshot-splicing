import math
import numpy as np


# 列采样函数
def col_sampling(img_array: np.ndarray, sample_cols=None):
    w = img_array.shape[1]
    default_cols = [
        np.linspace(20, w/4, 3, dtype='int'),
        np.linspace(w/2, 5 * w / 8, 3, dtype='int'),
        np.linspace(6 * w / 8, 7 * w / 8, 3, dtype='int')
    ]

    sample_cols = sample_cols or default_cols
    return np.stack(list(np.average(img_array[:, cols], axis=1) for cols in sample_cols), axis=1)


# 根据预测值,生成一个最佳的偏移序列
def predict_offset(max: int, p: int):
    p = max if p > max else -max if p < -max else p
    positive_range = np.arange(1, max + 1, 1, dtype=np.int16)
    negative_range = np.arange(-max, 0, 1, dtype=np.int16)

    full = np.hstack((negative_range, positive_range))

    r_1 = full[2 * p:p+max][::-1] if p > 0 else full[0: max+p][::-1]
    r_2 = full[max+p: 2*max] if p > 0 else full[max+p:2 * (max+p)]
    r_3 = full[0: 2*p][::-1] if p > 0 else full[2*(max+p):]

    r_1_2 = np.stack([r_1, r_2], axis=1).reshape([-1])

    return np.hstack([[0], r_1_2, r_3])


# 根据采样计算两张图片的重合位置
def diff_overlap(cols: np.ndarray, cols2: np.ndarray, predict=0, approx_diff=0.2, min_overlap=100):
    approach_i = 0
    min_diff = (0, 255)

    max = cols.shape[0] - min_overlap
    for i in predict_offset(max, predict):
        diff = np.abs(cols - cols2) if i == 0 else np.abs(cols[i:] - cols2[:-i]) \
            if i > 0 else np.abs(cols[:i] - cols2[-i:])

        avg = np.average(diff)
        if avg < min_diff[1]:
            min_diff = (i, avg)

        if min_diff[1] < approx_diff:
            approach_i += 1
            if approach_i > 10:
                return min_diff
            elif avg < approx_diff / 4:
                return min_diff

    return min_diff


# 计算预测值 (frame_count, offset_y, diff)[]
def predict(history: list, expect_offset, max_step=3):
    if len(history) < 1:
        return 1, 0
    if len(history) == 1:
        return 1, history[0][1]

    pre_data = history[-2]
    data = history[-1]

    offset_per_frame = data[1] / (data[0] - pre_data[0])
    if offset_per_frame == 0:
        if pre_data[1] == 0:
            return max_step, 0
        else:
            return 1, pre_data[1]

    frame_distance = math.floor(expect_offset / abs(offset_per_frame * 1))
    step = max(min(frame_distance, max_step), 1)
    predict_y = int(step * offset_per_frame)
    return step, predict_y


# 计算视频邻近帧之间的重合位置
def calc_overlaps(
        frames: np.ndarray, crop_top: int, crop_bottom: int, expect_offset: int,
        sample_cols=None, verbose=False, approx_diff=0.2, min_overlap=100
):
    n = frames.shape[0]
    img = frames[0][0]
    img2 = None
    cols = col_sampling(img[crop_top: -crop_bottom], sample_cols)
    cols2 = None

    results = []
    i = 1

    while i < n:
        img2 = frames[i][0]
        cols2 = col_sampling(img2[crop_top: -crop_bottom], sample_cols)

        step, p = predict(results[-3:], expect_offset)
        offset, diff = diff_overlap(cols, cols2, p, approx_diff, min_overlap)
        results.append((i, offset, diff))

        i += step
        cols = cols2
        img = img2
        if verbose:
            print(f'diff  {i}\t{offset}\t{p}\t{diff}')

    return results


# 拼接长图
def splice(frames: np.ndarray, results: list, crop_top: int, crop_bottom: int, seam_width=0):
    full_h, w = frames[0][0].shape
    h = full_h - crop_top - crop_bottom

    top = 0
    top_i = 0
    bottom = 0
    bottom_i = 0
    c = 0
    for (i, offset, diff) in results:
        c += offset
        if c > bottom:
            bottom = c
            bottom_i = i
        if c < top:
            top = c
            top_i = i

    def get_frame(i):
        return np.dstack((frames[i][0], frames[i][1], frames[i][2]))

    tamplate = np.zeros((bottom - top + full_h, w, 3), dtype=np.int8)
    y = crop_top if top == 0 else -top + crop_top
    tamplate[y: y+h] = get_frame(0)[crop_top: -crop_bottom]
    tamplate[0: crop_top] = get_frame(top_i)[0: crop_top]
    tamplate[-crop_bottom:] = get_frame(bottom_i)[-crop_bottom:]

    for (i, offset, diff) in results:
        y += offset
        image = get_frame(i)[crop_top: -crop_bottom]
        if seam_width > 0:
            image[0: seam_width] = [76,  84, 255]
        tamplate[y: y + h] = image

    return tamplate
