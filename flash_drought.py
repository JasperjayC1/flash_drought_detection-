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

# 假设有一个变量sm存储了每五日的土壤水分百分位数据，是一个一维数组
# 定义一个函数来检测flash drought
def detect_flash_drought(sm):
  # 初始化一个空列表来存储flash drought的起始和结束日期
  flash_droughts = []
  # 初始化一个变量来记录当前是否处于flash drought状态
  in_flash_drought = False
  # 初始化一个变量来记录当前flash drought的开始日期
  start_date = None
  # 遍历sm数组中的每个元素和索引
  for i, s in enumerate(sm):
    # 如果当前不在flash drought状态
    if not in_flash_drought:
      # 检查是否满足flash drought的开始条件：土壤水分低于40分位数，并且下降率大于等于5%
      if s < 40 and (i == 0 or sm[i-1] - s >= 5):
        # 如果满足，更新状态为True，并记录开始日期为当前索引
        in_flash_drought = True
        start_date = i
    # 如果当前在flash drought状态
    else:
      # 检查是否满足flash drought的结束条件：土壤水分高于等于20分位数
      if s >= 20:
        # 如果满足，更新状态为False，并记录结束日期为当前索引
        in_flash_drought = False
        end_date = i
        # 判断是否满足flash drought的持续时间条件：至少15天
        if end_date - start_date >= 3:
          # 如果满足，将开始和结束日期作为一个元组添加到列表中
          flash_droughts.append((start_date, end_date))
  # 返回flash drought列表
  return flash_droughts

# 调用函数并打印结果
print(detect_flash_drought(sm))
