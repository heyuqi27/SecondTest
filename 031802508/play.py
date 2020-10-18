# 本程序images目录下已经有用"樱桃小丸子.jpg"分解切出的9张小图片
# 可以用自己喜欢的图片进行替换（大小：450*450）
from tkinter import *
from tkinter.messagebox import *
import random
from PIL import Image, ImageTk
import tkinter.messagebox

root = Tk('Pingtu')  # 创建一个窗口
root.resizable(width=False, height=False)  # 禁止改变窗口大小
# root.iconbitmap('images/fklogo.ico') #可修改图标
root.title("images-拼图")  # 给窗口命名

# 定义常量
# 画布的尺寸
WIDTH = 450
HEIGHT = 450
# 图像块的边长
IMAGE_WIDTH = WIDTH // 3
IMAGE_HEIGHT = HEIGHT // 3
# 游戏的行/列数
ROWS = 3
COLS = 3
# 移动步数
steps = 0
# 保存所有图像块的列表
board = [[0, 1, 2],
         [3, 4, 5],
         [6, 7, 8]]
# 载入外部事先生成的9个小图像块
Pics = []
photo = 0

class Square:
    def __init__(self, orderID):
        self.orderID = orderID

    def draw(self, canvas, board_pos):
        img = Pics[self.orderID]
        canvas.create_image(board_pos, image=img)


# 将图像块打乱
def init_board():
    L = list(range(9))  # L列表中[0,1,2,3,4,5,6,7,8]
    random.shuffle(L)  # 随机排序
    # 填充拼图板
    for i in range(ROWS):
        for j in range(COLS):
            idx = i * ROWS + j
            orderID = L[idx]
            if orderID == 8:  # 8号拼块不显示,所以存为None
                board[i][j] = None
            else:
                board[i][j] = Square(orderID)


def drawBoard(canvas):
    # outline fill是对被扣掉的图块的颜色进行设置
    canvas.create_polygon((0, 0, WIDTH, 0, WIDTH, HEIGHT, 0, HEIGHT), width=1, outline='#e7f2f4', fill='#e7f2f4')
    # 画所有图像块
    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j] is not None:
                board[i][j].draw(canvas, (IMAGE_WIDTH * (j + 0.5),
                                          IMAGE_HEIGHT * (i + 0.5)))


def mouseclick(pos):
    global steps
    # 将单击位置换算成拼图板上的棋盘坐标
    r = int(pos.y // IMAGE_HEIGHT)
    c = int(pos.x // IMAGE_WIDTH)
    if r < 3 and c < 3:  # 单击位置在拼图板内才移动图片
        if board[r][c] is None:  # 单击空位置,什么也不移动
            return
        else:
            # 依次检查被单击当前图像块的上、下、左、右是否有空位置,如果有,就移动当前图像块
            current_square = board[r][c]
            if r - 1 >= 0 and board[r - 1][c] is None:  # 判断上面
                board[r][c] = None
                board[r - 1][c] = current_square
                steps += 1
            elif c + 1 <= 2 and board[r][c + 1] is None:  # 判断右面
                board[r][c] = None
                board[r][c + 1] = current_square
                steps += 1
            elif r + 1 <= 2 and board[r + 1][c] is None:  # 判断下面
                board[r][c] = None
                board[r + 1][c] = current_square
                steps += 1
            elif c - 1 >= 0 and board[r][c - 1] is None:  # 判断左面
                board[r][c] = None
                board[r][c - 1] = current_square
                steps += 1
            # print(board)
            b_step["text"] = "步数：" + str(steps)
            cv.delete('all')
            # 清除画布上的内容
            drawBoard(cv)
    if win():
        showinfo(title="恭喜", message="你成功了！")

# 对用户操作是否达到目标状态(即拼出完整图)进行设置
def win():
    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j] is not None and board[i][j].orderID != i * ROWS + j:
                return False
    return True


# 游戏开始
def play_game():
    global steps
    steps = 0
    init_board()  # 打乱图像块


# 鼠标点击“重新开始”响应函数
def callBack_start():
    print("重新开始")
    play_game()
    cv.delete('all')
    # 清除画布上的内容
    drawBoard(cv)

def select_pic():
    global photo
    global Pics
    # 载入画布左边正确的图片
    index = random.randint(1,21)
    path1 = r"design_img./"+str(index)+".jpg"
    image = Image.open(path1)  # 通过Image=photo设置要展示的图片
    photo = ImageTk.PhotoImage(image)  # 创建tkinter兼容的图片
    #切割选择的图片
    path2 = r"cut_img./"+str(index)+".jpg"
    im = Image.open(path2)
    dispose(im)
    # 载入生成的9个小图像块
    Pics = []
    for i in range(0, 9):
        filename = r"images./imag" + str(i) + ".png"
        Pics.append(PhotoImage(file=filename))
    #呈现正确图片
    b_pic = Label(root, image=photo, width=200)
    b_pic.place(x=30, y=0, width=220, height=220)
    callBack_start()

# 判断该图片是否为正方形
def dispose(im):
    if (im.width == im.height):
        imageList = cutNine(im)
    else:
        new_im = fillSquare(im)
        imageList = cutNine(new_im)
    save_images(imageList)

# 进行图片九等分
def cutNine(im):
    w = int(im.width / 3)
    boxList = []
    for i in range(0, 3):
        for j in range(0, 3):
            box = (j * w, i * w, (j + 1) * w, (i + 1) * w)
            boxList.append(box)
    imageList = [im.crop(box) for box in boxList]
    return imageList

# 进行图片填充
def fillSquare(im):
    w = im.width if im.width > im.height else im.height
    newImage = Image.new(im.mode, (w, w), color='white')
    if (im.width > im.height):
        newImage.paste(im, (0, int((w - im.height) / 2)))
    else:
        newImage.paste(im, (int((w - im.width) / 2, 0)))
    return newImage

# 完成切割
def save_images(imList):
    index = 0
    image_list = []
    for image in imList:
        image.save(r'images./imag' + str(index) + '.png', 'png')
        image_list.append(r'images./imag' + str(index) + '.png')
        index += 1
    return image_list

def call_help():
    tkinter.messagebox.showinfo('帮助', '点击RESTART重新开始游戏\n点击PICTURE随机切换图片\nSTEPS为当前移动步数总和')


if __name__ == '__main__':
    # 在画布左边填充颜色
    canvas_bottom = Canvas(root, width=280, height=HEIGHT, bg='#e7f2f4')
    # 在画布右边填充颜色
    cv = Canvas(root, width=WIDTH, height=HEIGHT, bg="#ccd7db")
    cv.pack()

    select_pic()
    # 设置“开始”按钮
    b_start = Button(root, activebackground="#de6e58", bg="#c24e35", text="重新开始",
                     font="宋体", command=callBack_start)
    b_replace = Button(root, activebackground="#fecf3b", bg="orange",
                       text="更换图片", font="宋体", command=select_pic)
    b_help = Button(root,activebackground="#b9be6e", bg="#6ab177", text="帮助",font=("宋体",12),command = call_help)
    b_step = Label(root, text="步数：" + str(steps), font=("宋体",12), fg="black", bg="#699db5")
    cv.bind("<Button-1>", mouseclick)
    cv.pack(side='right')

    canvas_bottom.pack()
    b_help.place(x=40, y=260, width=90, height=40)
    b_step.place(x=150, y=260, width=90, height=40)
    b_start.place(x=40, y=310, width=200, height=50)
    b_replace.place(x=40, y=370, width=200, height=50)
    canvas_bottom.pack()
    play_game()
    drawBoard(cv)
    root.mainloop()
