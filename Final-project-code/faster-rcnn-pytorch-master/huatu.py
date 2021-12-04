import matplotlib.pyplot as plt

txt = open(r'C:\Users\mjr\Desktop\txt.md')
data = txt.read()

Train_Loss_list =[]
Valid_Loss_list =[]

#学习率
lr = []
#主函数分类损失
roi_cls = []
#主函数回归损失
roi_loc = []
#RPN分类损失
rpn_cls = []
#RPN回归损失
rpn_loc = []

list1 = data.split("Total Loss: ")
for i in range(1,101):
    list2 = list1[i].split(" || ")
    Train_Loss_list.append(list2[0])
Train_Loss_list = list(map(float,Train_Loss_list))

list1 = data.split("Val Loss: ")
for i in range(1,101):
    list2 = list1[i].split(" ")
    Valid_Loss_list.append(list2[0])
Valid_Loss_list = list(map(float,Valid_Loss_list))

list1 = data.split(" lr=")
for i in range(1,101):
    list2 = list1[i].split(",")
    lr.append(list2[0])
lr = list(map(float,lr))

list1 = data.split("roi_cls=")
for i in range(1,101):
    list2 = list1[i].split(",")
    roi_cls.append(list2[0])
roi_cls = list(map(float,roi_cls))

list1 = data.split("roi_loc=")
for i in range(1,101):
    list2 = list1[i].split(",")
    roi_loc.append(list2[0])
roi_loc = list(map(float,roi_loc))

list1 = data.split("rpn_cls=")
for i in range(1,101):
    list2 = list1[i].split(",")
    rpn_cls.append(list2[0])
rpn_cls = list(map(float,rpn_cls))

list1 = data.split("rpn_loc=")
for i in range(1,101):
    list2 = list1[i].split(",")
    rpn_loc.append(list2[0])
rpn_loc = list(map(float,rpn_loc))


plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置
x1 = range(100)
y1 = Train_Loss_list
y2 = Valid_Loss_list
y3 = lr
y4 = roi_cls
y5 = roi_loc
y6 = rpn_cls
y7 = rpn_loc
plt.subplot(221)
plt.plot(x1, y1, "-o")
plt.plot(x1, y2, "--o")
plt.ylabel('训练集（实）/验证集损失（虚）')
plt.xlabel('轮数')
plt.subplot(222)
plt.plot(x1, y3, "-o")
plt.ylabel('学习率')
plt.xlabel('轮数')
plt.subplot(223)
plt.plot(x1, y4, "-o")
plt.plot(x1, y5, "--o")
plt.ylabel('RoI分类（实）/回归损失（虚）')
plt.xlabel('轮数')
plt.subplot(224)
plt.plot(x1, y6, "-o")
plt.plot(x1, y7, "--o")
plt.ylabel('RPN分类（实）/回归损失（虚）')
plt.xlabel('轮数')
# # plt.plot(x1, y1, "-o") #实线
# # plt.plot(x1, y2, "--o") #虚线
# # plt.plot(x1, y3, "-.o") #虚点线
# # plt.plot(x, y4, ":o") # 点线
plt.show()