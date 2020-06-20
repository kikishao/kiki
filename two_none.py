import numpy as np

def MessageComingEvent(t,T,T_init,mastercomputer,preprocess1,preprocess2,message_wait,message_loss):   # 信息到来事件
    if mastercomputer == 0:  # 主计算机有空闲
        mastercomputer = 1
        t = MessageSolveTime() + t
        if t in T_init:
            t = t + 0.01
        T.append(t)
        T = sorted(T)
    else:  # 主计算机无空闲
        if preprocess1 == 0 and preprocess2 == 0:   # 预处理机1有空闲
            preprocess1 = 1
            message_wait = message_wait + 1
        elif preprocess1 == 1 and preprocess2 == 0:  # 预处理机2有空闲
            preprocess2 = 1
            message_wait = message_wait + 1
        else:  # 信息丢失
            message_loss = message_loss + 1
    return T,mastercomputer,preprocess1,preprocess2,message_wait,message_loss

def MessageSolveTime():    # 信息处理时间
    serve = [13, 15, 17, 20, 21]
    ser_index = np.array([0.05, 0.55, 0.75, 0.95, 1])
    T_serve = serve[np.min(np.where((np.random.rand() - ser_index) < 0))]
    return T_serve

def MessageSolveEvent(t,T,T_init,message_serve,preprocess1,preprocess2):    # 信息处理事件
    mastercomputer = 0    # 主计算机释放
    message_serve = message_serve + 1
    if preprocess1 == 1:
        mastercomputer = 1
        t = MessageSolveTime() + t
        if t in T_init:
            t = t + 0.01
        T.append(t)
        T = sorted(T)
        preprocess1 = 0
        if preprocess2 == 1:
            preprocess1 = 1
            preprocess2 = 0
    return T,mastercomputer,preprocess1,preprocess2,message_serve

# 主程序
for total in np.array([600,800,1000,1200]):   # 仿真情报总数分别为600,800,1000,1200的实际情况
    T_arr = []                   # 情报到达时间间隔
    T_init = []                  # 情报累积到达时刻
    message = np.random.rand(total)
    arr_interval = [0, 5, 10, 15, 20, 30, 40]
    arr_index = np.array([0.12, 0.21, 0.34, 0.5, 0.69, 0.94, 1])
    for i in message:
        a = np.min(np.where(i - arr_index < 0))
        T_arr.append(arr_interval[a])
    T_init.append(T_arr[0])
    for i in range(1,len(T_arr)):
        T_init.append(T_arr[i]+T_init[i-1])
    T = T_init[:]                  # 事件表初始化

    t = 0                   # 系统时钟
    n = 0
    Tfree = T_init[0]               # 主机空闲的时间
    mastercomputer = 0      # 主计算机处于空闲状态
    preprocess1 = 0         # 预处理机1处于空闲状态
    preprocess2 = 0         # 预处理机2处于空闲状态
    time_master = 0         # 主计算机空闲的时间
    message_total = 0       # 工作时间内实际到达情报总数
    message_serve = 0       # 处理的情报总数
    message_loss = 0        # 丢失的情报总数
    message_wait = 0        # 等待的情报总数

    while 1:
        t = T[n]
        if t in T_init: # 情报到达
            message_total = message_total + 1
            T, mastercomputer, preprocess1, preprocess2, message_wait, message_loss = MessageComingEvent(t, T,T_init,
                                                                                                             mastercomputer,
                                                                                                             preprocess1,
                                                                                                             preprocess2,
                                                                                                             message_wait,
                                                                                                             message_loss)
        else: # 情报处理
            if isinstance(t,int):
                T, mastercomputer, preprocess1, preprocess2, message_serve = MessageSolveEvent(t, T, T_init, message_serve,
                                                                                           preprocess1, preprocess2)
                if mastercomputer == 0:
                    if n != len(T)-1:
                        Tfree = Tfree + T[n+1] - t
            else:
                t = int(t-0.01)
                T, mastercomputer, preprocess1, preprocess2, message_serve = MessageSolveEvent(t, T, T_init,message_serve,
                                                                                               preprocess1, preprocess2)
                if mastercomputer == 0:
                    if n != len(T) - 1:
                        Tfree = Tfree + T[n+1] - t
        n = n+1
        if n == len(T):
            break

        Tend = T[-1]

    print("到达情报总数：", message_total)
    print("情报损失总数:", message_loss)
    print("已处理情报总数:",message_serve)
    print("情报损失比率:", message_loss / message_total)
    print("情报等待百分比：", message_wait / (message_total - message_loss))
    print("每项情报平均处理时间：", (Tend - Tfree) / message_serve)
    print("主机空闲率：", Tfree / Tend)
    print("系统的平均效率：", message_serve / Tend)
    print("- - - - - - - - - - - - - - - -")





