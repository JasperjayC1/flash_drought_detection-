sm = [42,
           45,
           90,
           62,
           22,
           40,
           25,
           17,
           15,
           12,
           13,
           33,
           38
           ]
sm

# 定义一个子程序来识别骤旱事件，根据土壤湿度百分位数
# 参考文献：
# 1. Yuan, X., L. Wang, P. Wu, P. Ji, J. Sheffield, and M. Zhang, 2019: 
# Anthropogenic shift towards higher risk of flash drought over China. 
# Nature Communications, 10, 4661, 
# https://doi.org/10.1038/s41467-019-12692-7
# 2. Yuan, X., Y. Wang, P. Ji, P. Wu, J. Sheffield, J. Otkin, 2023: A 
# global transition to flash droughts under climate change. Science, 
# https://doi.org/10.1126/science.abn6301

import numpy as np

def flashdrought(n,a,b,drt):
    # n，一年内的五日数
    # a(n)，五日土壤湿度百分位数 [0-100] 
    # b(1)，骤旱事件的数量
    # b(2)，骤旱事件的平均持续时间
    # b(3)，骤旱事件的平均严重程度
    # b(4)，骤旱事件的平均速度
    # drt，1-骤旱开始，2-骤旱恢复，0-无骤旱
    thresh = 40   # 骤旱开始阈值 [百分位数]
    thresh1 = 20  # 骤旱结束阈值 [百分位数]
    speed = 5     # 骤旱速度阈值 [百分位数]
    td = 4        # 骤旱持续时间阈值 [五日]
    cnt = 0       # 骤旱事件计数器
    flag = 0      # flag=1，开始识别骤旱事件
    si = 0        # si是骤旱开始时间
    odur = [0] * n   # 每个骤旱事件的总持续时间
    osev = [0] * n   # 每个骤旱事件的总严重程度
    ospd = [0] * n   # 每个骤旱事件的开始速度
    tmin = 99     # 最小土壤湿度百分位数
    flag1 = 0     # flag1=1，开始一个新的骤旱事件
    flag2 = 0     # flag2=1，开始期；flag2=0，恢复期
    drt = [0] * n # 骤旱状态数组

    for i in range(n): # 判断输入数据的正确性，如存在负值该数据丢弃
        if a[i] < 0:
            print('error, stop')
            print(a)
            return

    for j in range(1,n):
        if a[j] < thresh:          # 土壤湿度低于阈值
            if flag == 0:          # 骤旱开始
                flag1 = 1          
                if j > 0:
                    if a[j-1] < thresh:
                        flag1 = 0
                if flag1 == 1:
                    flag = 1
                    flag2 = 1      # 开始期
                    cnt += 1       # 骤旱计数器加一
                    si = j         # 记录骤旱开始时间
                    osev[cnt] = thresh - a[j]   # 计算严重程度
                    odur[cnt] = 1               # 计算持续时间
                    ospd[cnt] = thresh - a[j]   # 计算速度
                    drt[j] = 1                  # 记录骤旱状态为开始
                    if a[j] < tmin:
                        tmin = a[j]
            else:
                if flag2 == 1:     # 开始期
                    if thresh - a[j] >= (j - si + 1) * speed:   # 土壤湿度下降速度满足条件
                        if tmin <= thresh1:    # 进入低于thresh1的区域（例如，<20%）
                            if a[j] >= a[j-1]: # 土壤湿度不再下降
                                flag2 = 0      # 结束开始期
                                if a[j] <= thresh1:  # 进入恢复期
                                    osev[cnt] = osev[cnt] + (thresh - a[j])  # 计算严重程度
                                    odur[cnt] = odur[cnt] + 1                # 计算持续时间
                                    drt[j] = 2                              # 记录骤旱状态为恢复
                                    if a[j] < tmin:
                                        tmin = a[j]
                                else:           # 没有恢复期
                                    flag = 0    # 结束骤旱识别
                                    tmin = 99
                                    if odur[cnt] < td:   # 如果持续时间小于阈值，则不算骤旱事件
                                        osev[cnt] = 0
                                        odur[cnt] = 0
                                        ospd[cnt] = 0
                                        drt[si:j] = [0] * (j - si)
                                        cnt -= 1
                            else:               # 土壤湿度继续下降，继续开始期
                                osev[cnt] = osev[cnt] + (thresh - a[j])  # 计算严重程度
                                odur[cnt] = odur[cnt] + 1                # 计算持续时间
                                ospd[cnt] = (thresh - a[j]) / (j - si + 1)   # 计算速度
                                drt[j] = 1                                  # 记录骤旱状态为开始
                                if a[j] < tmin:
                                    tmin = a[j]
                        else:                   # 在进入thresh1之前，继续开始期
                            osev[cnt] = osev[cnt] + (thresh - a[j])  # 计算严重程度
                            odur[cnt] = odur[cnt] + 1                # 计算持续时间
                            ospd[cnt] = (thresh - a[j]) / (j - si + 1)   # 计算速度
                            drt[j] = 1                                  # 记录骤旱状态为开始
                            if a[j] < tmin:
                                tmin = a[j]
                    else:           # 土壤湿度下降速度不满足条件，结束开始期
                        flag2 = 0
                        if tmin <= thresh1:
                            if a[j] <= thresh1:  # 进入恢复期
                                osev[cnt] = osev[cnt] + (thresh - a[j])  # 计算严重程度
                                odur[cnt] = odur[cnt] + 1                # 计算持续时间
                                drt[j] = 2                              # 记录骤旱状态为恢复

                            else:               # 没有恢复期
                                flag = 0        # 结束骤旱识别
                                tmin = 99
                                if odur[cnt] < td:   # 如果持续时间小于阈值，则不算骤旱事件
                                    osev[cnt] = 0
                                    odur[cnt] = 0
                                    ospd[cnt] = 0
                                    drt[si:j] = [0] * (j - si)
                                    cnt -= 1
                        
                        else:  # tmin>thresh1, does not meet drought criterion 
                            drt[si:j] = [0] * (j - si)
                            osev[cnt] = 0
                            odur[cnt] = 0
                            ospd[cnt] = 0
                            cnt -= 1
                            flag=0
                            tmin=99

                else:                   # 恢复期(flag2=0)
                    if a[j] > thresh1:  # 土壤湿度高于阈值，结束恢复期
                        flag = 0        # 结束骤旱识别
                        tmin = 99
                        if odur[cnt] < td:   # 如果持续时间小于阈值，则不算骤旱事件
                            osev[cnt] = 0
                            odur[cnt] = 0
                            ospd[cnt] = 0
                            drt[si:j] = [0] * (j - si)
                            cnt -= 1
                    else:               # 土壤湿度低于阈值，继续恢复期
                        osev[cnt] = osev[cnt] + (thresh - a[j])  # 计算严重程度
                        odur[cnt] = odur[cnt] + 1                # 计算持续时间
                        drt[j] = 2                              # 记录骤旱状态为恢复
                        
            if j==n and flag==1:
                if odur[cnt]<td or tmin>thresh1:
                    osev[cnt] = 0
                    odur[cnt] = 0
                    ospd[cnt] = 0
                    drt[si:j+1] = [0] * (j - si + 1)
                    cnt -= 1  
        else:                       # 土壤湿度高于阈值，无骤旱事件发生
            if flag == 1:          # 如果之前有骤旱事件发生，结束骤旱识别
                flag = 0        
                tmin = 99              
                if odur[cnt] < td or tmin > thresh1:   # 如果持续时间小于阈值，则不算骤旱事件
                    osev[cnt] = 0    
                    odur[cnt] = 0    
                    ospd[cnt] = 0    
                    drt[si:j+1] = [0] * (j - si + 1)
                    cnt -= 1

    # b[0] = cnt                     # 骤旱事件的数量
    # b[1] = np.mean(odur[:cnt+1])     # 骤旱事件的平均持续时间
    # b[2] = np.mean(osev[:cnt+1])     # 骤旱事件的平均严重程度
    # b[3] = np.mean(ospd[:cnt+1])     # 骤旱事件的平均速度

    if cnt > 0:
        b[0] = float(cnt)                                # 骤旱事件的数量
        b[1] = float(sum(odur[0:cnt+1])) / float(cnt)    # 骤旱事件的平均持续时间
        b[2] = sum(osev[0:cnt+1]) / float(cnt)           # 骤旱事件的平均严重程度
        b[3] = sum(ospd[0:cnt+1]) / float(cnt)           # 骤旱事件的平均速度
    else:
        b = 0

