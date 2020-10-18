import numpy as np
import sys

class State:
    def __init__(self, state, directionFlag=None, parent=None, depth=0):
        self.state = state
        # state is a ndarray with a shape(3,3) to storage the state
        self.direction = ['up', 'down', 'right', 'left']
        if directionFlag:
            self.direction.remove(directionFlag)
            # record the possible directions to generate the sub-states
        self.symbol = 0
        self.parent = parent
        self.answer = np.array([[1,2,3], [4,5,6], [7,8,0]])
        self.depth = depth
        # calculate the num of elements which are not in the proper position
        num = 0
        for i in range(len(state)):
            for j in range(len(state)):
                if self.state[i, j] != 0 and self.state[i, j] != self.answer[i, j]:
                    num += 1
        self.cost = num + self.depth

    def getDirection(self):
        return self.direction

    def showInfo(self):
        for i in range(3):
            for j in range(3):
                if self.state[i, j] == 0:
                    print(self.symbol, end='  ')
                else:
                    print(self.state[i, j], end='  ')
            print("\n")
        print('------>')
        return

    def getEmptyPos(self):
        postion = np.where(self.state == 0)
# np.where(condition,x,y) 满足条件condition时，输出x;若x,y省略时，则输出满足条件元素的位置，输出tuple维度与输入相同
        return postion
    def generateSubStates(self):
        if not self.direction:
            return []
        subStates = []
        # the maximum of the x,y
        row, col = self.getEmptyPos()
        if 'left' in self.direction and col > 0:
        #it can move to left place
            s = self.state.copy()
            temp = s.copy()
            s[row, col] = s[row, col-1]
            s[row, col-1] = temp[row, col]
            news = State(s, directionFlag='right', parent=self, depth=self.depth+1)
            subStates.append(news)
        if 'up' in self.direction and row > 0:
        #it can move to upper place
            s = self.state.copy()
            temp = s.copy()
            s[row, col] = s[row-1, col]
            s[row-1, col] = temp[row, col]
            news = State(s, directionFlag='down', parent=self, depth=self.depth+1)
            subStates.append(news)
        if 'down' in self.direction and row < 2:
            #it can move to down place
            s = self.state.copy()
            temp = s.copy()
            s[row, col] = s[row+1, col]
            s[row+1, col] = temp[row, col]
            news = State(s, directionFlag='up', parent=self, depth=self.depth+1)
            subStates.append(news)
        if self.direction.count('right') and col < 2:
            #it can move to right place
            s = self.state.copy()
            temp = s.copy()
            s[row, col] = s[row, col+1]
            s[row, col+1] = temp[row, col]
            news = State(s, directionFlag='left', parent=self, depth=self.depth+1)
            subStates.append(news)
        return subStates
    def solve(self):
        # generate a empty openTable
        openTable = []
        # generate a empty closeTable
        closeTable = []
        # append the origin state to the openTable
        openTable.append(self)
        # denote the steps it travels
        steps = 0
        while len(openTable) > 0:     # start the loop
            n = openTable.pop(0)
            closeTable.append(n)
            subStates = n.generateSubStates()
            path = []
            for s in subStates:
                if (s.state == s.answer).all():  #iterable.all() iterable所有元素均不为0，空，FALSE
                    while s.parent and s.parent != self :
                        path.append(s.parent)
                        s = s.parent
                    path.reverse()
                    return path, steps+1
                # for t in openTable:
                #     if (s.state == t.state).all() and s.cost<t.cost:
                #         openTable.remove(t)

                # for t in closeTable:
                #     if (s.state == t.state).all() and s.cost<t.cost:
                #         closeTable.remove(t)

            openTable.extend(subStates)
            # sort the openTable in terms of the cost
            openTable.sort(key=lambda x: x.cost)
            steps += 1
        return None, None

def can_rate(State):
    number=0
    re_state=[]
    re_state=[y for x in State.state for y in x]
    for i in range(1,9):
        for j in range(i):
            if re_state[j]<re_state[i]:
                number+=1
    return number

if __name__ == '__main__':
    # the symbol representing the empty place
    # set the origin state of the puzzle
    originState = State(np.array([[1, 3, 2], [4, 0, 5], [6, 7, 8]]))
    answerState = State(np.array([[1, 2, 3], [4, 0, 5], [6, 7, 8]]))
    m = can_rate(originState)
    n = can_rate(answerState)
    if not m%2==n%2:
        sys.exit(0)
    s1 = State(state=originState.state)
    s1.answer = answerState.state
    path, steps = s1.solve()
    if path:                        # if find the solution
        for node in path:
                # print the path from the origin to final state
                node.showInfo()
        answerState.showInfo()
        print("Total steps is %d" % steps)