import numpy as np

# 自定义结构
persontype = np.dtype({
    'names': ['name', 'chinese', 'math', 'english'],
    'formats': ['S32','i', 'i', 'i']})
# 初始化数据
peoples = np.array([('ZhangFei', 66, 65, 30),
                    ('GuanYu', 95, 85, 98), ('ZhaoYun', 93, 92, 96),
                    ('HuangZhong', 90, 88, 77), ('DianWei', 80, 90, 90)],
                   dtype=persontype)

chineses = peoples[:]['chinese']  # 语文分数数组
maths = peoples[:]['math']        # 数学分数数组
englishs = peoples[:]['english']  # 英语分数数组

print(f"语文 最高分:{np.amax(chineses)} 最低分:{np.amin(chineses)} 平均分:{np.mean(chineses)} 标准差:{np.std(chineses)} 方差:{np.var(chineses)}")
print(f"数学 最高分:{np.amax(maths)} 最低分:{np.amin(maths)} 平均分:{np.mean(maths)} 标准差:{np.std(maths)} 方差:{np.var(maths)}")
print(f"英语 最高分:{np.amax(englishs)} 最低分:{np.amin(englishs)} 平均分:{np.mean(englishs)} 标准差:{np.std(englishs)} 方差:{np.var(englishs)}")
ranking = sorted(peoples, key=lambda x: x[1]+x[2]+x[3], reverse=True) # 按总分排序
for item in ranking:
    print(item)


