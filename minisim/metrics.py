import math

def distance(history):
    dist = 0
    for i in range(1, len(history)):
        dx = history[i]['x'] - history[i - 1]['x']
        dy = history[i]['y'] - history[i - 1]['y']
        dist = dist + math.hypot(dx, dy)

    return dist

def summary(history):
    """返回一组指标；打印和文件保存交给实验层。"""
    if not history:
        raise ValueError("没有可统计的记录")
    dist = distance(history)
    time = history[len(history) - 1]['time'] - history[0]['time']
    if(time != 0): aver_sp = dist / time
    else: aver_sp = 0

    return {
        "total_distance": dist,
        "total_time": time,
        "average_speed": aver_sp,
    }
