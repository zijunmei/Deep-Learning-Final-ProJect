import matplotlib.pyplot as plt

txt = open(r'C:/Users/User/Desktop/yolotxt.md')
data = txt.read()

Train_Loss_list =[]
Valid_Loss_list =[]

#学习率
lr = []


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


plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置
x1 = range(100)
y1 = Train_Loss_list
y2 = Valid_Loss_list
y3 = lr
plt.subplot(221)
plt.plot(x1, y1, "-o")
plt.ylabel('训练集损失')
plt.xlabel('轮数')
plt.subplot(222)
plt.plot(x1, y2, "-o")
plt.ylabel('验证集损失')
plt.xlabel('轮数')
plt.subplot(212)
plt.plot(x1, y3, "-o")
plt.ylabel('学习率lr')
plt.xlabel('轮数')
# # plt.plot(x1, y1, "-o") #实线
# # plt.plot(x1, y2, "--o") #虚线
# # plt.plot(x1, y3, "-.o") #虚点线
# # plt.plot(x, y4, ":o") # 点线
plt.show()