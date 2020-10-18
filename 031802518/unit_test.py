import copy
import unittest
import random
from cut_picture import *
import http.client
http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'
#交换图片的元素
step = 2
swap = [3, 4]
def swap_position(stat,swap):
    newStat = copy.deepcopy(stat)  # stat是一个3*3列表
    idex_i = swap[0]  # 待交换的i和j
    idex_j = swap[1]
    ri = (idex_i-1) // 3
    rj = (idex_j-1) // 3
    i = (idex_i-1) % 3
    j = (idex_j-1) % 3
    tmp0=stat[rj][j]
    tmp = stat[ri][i]  # tmp用于记录要被和白块交换的数字
    # 由于移动白块后新的状态只是在原来状态的基础上改变了tmp和0，所以其他数值保持不变
    newStat[rj][j] = tmp
    newStat[ri][i] = tmp0
    return newStat

# 棋盘的类，实现移动和扩展状态
class grid:
    def __init__(self, stat,target):
        self.pre = None
        # 目标状态
        self.target = target
        # stat是一个二维列表
        self.stat = stat  # stat是一个列表
        self.find0()
        self.update()

    # 更新启发函数的相关信息
    def update(self):
        self.fH()  # H是估计值，不同的H会影响算法效率
        self.fG()  # G是步数，即深度
        self.fF()  # F是启发式函数，不同的函数会影响该算法的性能

    # G是深度，也就是走的步数
    def fG(self):
        if (self.pre != None):  # self.pre是open表中的一个结点，即一个grid对象，如果不等于0，说明不是第一步
            self.G = self.pre.G + 1
        else:
            self.G = 0  # 起步

    # H是和目标状态距离之和
    # 采用的是曼哈顿距离算法
    def fH(self):
        self.H = 0
        for i in range(3):
            for j in range(3):
                targetX = self.target[i][j]  # targetX这个位置他原来应该是什么数
                nowP = self.findx(targetX)  # nowP是targetX这个数现在在什么位置
                # 曼哈顿距离之和 d(i,j)=|xi-xj|+|yi-yj|
                # i是这个数现在的位置，nowP是这个数目标的位置
                self.H += abs(nowP[0] - i) + abs(nowP[1] - j)

    # F是启发函数，F=G+H
    def fF(self):
        self.F = self.G + self.H

    # 以三行三列的形式输出当前状态
    def see(self):
        for i in range(3):
            print(self.stat[i])
        print("F=", self.F, "G=", self.G, "H=", self.H)
        print("-" * 10)

    # 查看找到的解是如何从头移动的
    def seeAns(self):
        answer=""
        ans = []
        ans.append(self)
        p = self.pre
        while (p):
            ans.append(p)
            p = p.pre
        ans.reverse()  # 上面ans的顺序是从结果开始记录的，而这边正好反过来，因此可以使得ans从头开始就可以从一开始的情况来输出
        #print("ans",ans),ans[i]是grid对象
        x2,y2=0,0
        for i in ans:
                for x in range(0,3):
                    for y in range(0,3):
                        if i.stat[x][y] == 0:
                            x1 = x
                            y1 = y
                            flag1=1
                        if(i.G!=0):
                            if i.pre.stat[x][y]==0:
                                x2=x
                                y2=y
                print("x2,y2", x2, y2)
                print("x1,y1", x1, y1)
                # x1,y1是当前状态的0的位置
                # x2,y2是前一个状态的0的位置

                if x1 == (x2 - 1) and y1 == y2:
                    answer=answer+'w'
                elif x1 == (x2+1) and y1 == y2:
                    answer=answer+'s'
                elif x1 == x2 and y1 == (y2 - 1):
                    answer=answer+'a'
                elif x1 == x2 and y1 == (y2 + 1):
                    answer=answer+'d'
                i.see()
        l=len(answer)
        print("answer:",answer[1:l])

    # 找到数字x的位置
    def findx(self, x):
        for i in range(3):
            # 这边是3的原因是，stat是二维数组，所以每一次循环判断的是3个数，所以总共还是判断了9个数
            if (x in self.stat[i]):
                j = self.stat[i].index(x)  # index x是找value=x的数的下标，
                # 这里就是为什么上面是range（3），而不是range（9），因为range（3）可以直接取出y下标
                return [i, j]

    # 找到0，也就是空白格的位置
    def find0(self):
        self.zero = self.findx(0)  # self.zero表示的是空白格的位置[i,j]

    # 扩展当前状态，也就是上下左右移动。返回的是一个状态列表，也就是包含stat的列表
    def expand(self):
        # i,j分表表示空白格位置的x和y值
        i = self.zero[0]
        j = self.zero[1]
        gridList = []  # 相当于一个open表，表中的每一项都是一个结点，是一个grid对象，这个对象包含F,G,H等信息
        if (j == 2 or j == 1):  # 这四个if考虑了边界情况，同时代表的是添加open表
            gridList.append(self.left())
        if (i == 2 or i == 1):
            gridList.append(self.up())
        if (i == 0 or i == 1):
            gridList.append(self.down())
        if (j == 0 or j == 1):
            gridList.append(self.right())
        return gridList

    # deepcopy多维列表的复制，防止指针赋值将原列表改变
    # move只能移动行或列，即row和col必有一个为0
    # 向某个方向移动
    def move(self, row, col):  # 得到update即白块移动后的状态
        # 实现了交换白块和要被和白块交换的数字
        newStat = copy.deepcopy(self.stat)  # stat是一个3*3列表
        tmp = self.stat[self.zero[0] + row][self.zero[1] + col]  # tmp用于记录要被和白块交换的数字
        # 由于移动白块后新的状态只是在原来状态的基础上改变了tmp和0，所以其他数值保持不变
        newStat[self.zero[0]][self.zero[1]] = tmp
        newStat[self.zero[0] + row][self.zero[1] + col] = 0
        return newStat

    def up(self):
        return self.move(-1, 0)

    def down(self):
        return self.move(1, 0)

    def left(self):
        return self.move(0, -1)

    def right(self):
        return self.move(0, 1)


# 判断状态g是否在状态集合中，g是对象，gList是3*3对象列表
# 返回的结果是一个列表，第一个值是真假，如果是真则第二个值是g在gList中的位置索引
def isin(g, gList):
    gstat = g.stat
    statList = []
    for i in gList:
        statList.append(i.stat)
    if (gstat in statList):
        res = [True, statList.index(gstat)]
    else:
        res = [False, 0]
    return res


# 计算逆序数之和
def N(nums):
    N = 0
    for i in range(len(nums)):
        if (nums[i] != 0):
            for j in range(i):
                if (nums[j] > nums[i]):
                    N += 1
    return N


# 根据逆序数之和判断所给八数码是否可解
def judge(src, target):
    N1 = N(src)
    N2 = N(target)
    if (N1 % 2 == N2 % 2):
        return True
    else:
        return False
# Astar算法的函数
def Astar(startStat,ff,target):
    # open和closed存的是grid对象
    open = []
    closed = []
    # 初始化状态
    g = grid(startStat,target)
    # 接下来的代码是在有解的情况下讨论的
    open.append(g)
    # time变量用于记录遍历次数
    time = 0
    # 当open表非空时进行遍历
    while (open):
        # 根据启发函数值对open进行排序，默认升序
        # lambda的意思是按照G中G.F升序排序
        open.sort(key=lambda G: G.F)
        # 找出启发函数值最小的进行扩展
        minFStat = open[0]
        #进行强制转换，当强制转换后无解则进行用户交换
        if minFStat.G==step and ff==0:
                #该算法已经进行到step步要进行强制转换
                #number=0表示这是第一次所以要进行强制转换
                new_stat=swap_position(minFStat.stat,swap)
                print(new_stat)
                print("已进行强制交换！")
                # 检查是否有解
                flag=judge(new_stat, g.target)
                print(flag)
                if (flag != True):
                    print("所给图案强制交换后无解,进行用户交换！")
                    swap0=[1,1]
                    while(swap0[0]==swap0[1]):
                        n1=random.randint(1, 9)
                        n2=random.randint(1, 9)
                        swap0 = [n1,n2]
                    print("用户交换:swap:[",n1,",",n2,"]")
                    new_stat=swap_position(new_stat,swap0)
                    print(new_stat)
                return new_stat

        # 检查是否找到解，如果找到则从头输出移动步骤
        if (minFStat.H == 0):  # H=0说明所有的数字都在正确的位置上，这时候就是目标状态，找到答案了
            print("steps:", minFStat.G)
            minFStat.seeAns()
            break

        # 走到这里证明还没有找到解，对启发函数值最小的进行扩展
        open.pop(0)
        closed.append(minFStat)
        expandStats = minFStat.expand()
        # 遍历扩展出来的状态
        for stat in expandStats:
            # 将扩展出来的状态（二维列表）实例化为grid对象
            tmpG = grid(stat,target)
            # 指针指向父节点
            tmpG.pre = minFStat
            # 初始化时没有pre，所以G初始化时都是0
            # 在设置pre之后应该更新G和F
            tmpG.update()
            # 查看扩展出的状态是否已经存在与open或closed中
            # isin()判断状态g是否在状态集合中
            findstat = isin(tmpG, open)
            findstat2 = isin(tmpG, closed)
            # 在closed中,判断是否更新
            if (findstat2[0] == True and tmpG.F < closed[findstat2[1]].F):
                closed[findstat2[1]] = tmpG
                open.append(tmpG)
                time += 1
            # 在open中，判断是否更新
            if (findstat[0] == True and tmpG.F < open[findstat[1]].F):
                open[findstat[1]] = tmpG
                time += 1
            # tmpG状态不在open中，也不在closed中
            if (findstat[0] == False and findstat2[0] == False):
                open.append(tmpG)
                time += 1
    return target
def main_test():


    letter = ['A', 'a', 'b', 'B', 'c', 'd', 'D', 'e', 'F', 'g', 'h', 'H', 'J', 'k', 'm', 'M', 'n', 'o', 'O', 'p', 'P',
              'q', 'Q', 'r', 's', 't', 'u', 'U', 'v', 'W', 'x', 'X', 'y', 'Y', 'z', 'Z']
    image_dict = build_dictionary()  # 构建字典
    im = Image.open(r'./1.png')  # 读入乱序的图片
    image_List = dispose(im)  # 将要处理的图片进行切割
    image_nine, number = compare_images(image_dict, image_List)  # 将匹配的图片与正确图片进行匹配
    image_list, target, flag = tran_list(image_nine)  # 将字典转为数字列表1-8+空白块0
    print("The letter is '", letter[number], "'")
    print("target",target)
    # stat=image_list
    print("stat",image_list)
    stat = image_list
    new_stat=Astar(stat,0,target)
    #print(new_stat),可以输出
    new_target=Astar(new_stat,1,target)

class test_main(unittest.TestCase):
    def setUp(self):
        print("开始测试:")

    def tearDown(self):
        print("测试结束")

    def test_picswap(self):
        print("正在测试图片交换函数")
        stat=[[1, 5, 3], [6, 2, 0], [4, 7, 8]]
        swap=[1,6]
        swap_position(stat,swap)
    def test_main(self):
        print("正在测试A*算法")
        main_test()


if __name__ == '__main__':
    target=[[1, 2, 3], [4, 0, 5], [6, 7, 8]]
    stat=[[6, 7, 0], [2, 5, 3], [4, 8, 1]]
    unittest.main()