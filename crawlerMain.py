# crawlerMain.py
# -------------------------
# Visual and interactive extension of Q-learning Crawler, based on the lectures
# and code from Introduction to Artificial Intelligence, UC Berkeley.
# http://inst.eecs.berkeley.edu/~cs188/

# This file does not contain solutions of the project.
# Qlearning functions are imported from qlearningAgentsDemo.pyc
# Plese customise the functions in qlearningAgents.py and import qlearningAgents

# -------------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# graphicsCrawlerDisplay.py
# -------------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

import tkinter
import sys
import crawlerEnv
import random
import pickle
import collections

# import qlearningAgents from qlearningAgentsDemo.pyc
# Python bytecode is cross-platform, not cross-version
import qlearningAgentsDemo as qlearningAgents
# customise the functions in qlearningAgents.py and import qlearningAgents
# import qlearningAgents


class Application:

    def __init__(self):

        self.LearningRate = 0.8
        self.Discount = 0.8
        self.Epsilon = 1

        self.stepCount = 0
        self.stepsToSkip = 0
        # # Init Gui
        self.pause = True
        self.manualAction = None

        self.__initGUI()

        # Init environment
        self.robot = crawlerEnv.CrawlingRobot(self.canvas)
        self.robotEnvironment = crawlerEnv.CrawlingRobotEnvironment(self.robot)


        # Init Agent
        actionFn = lambda state: \
          self.robotEnvironment.getPossibleActions(state)
        self.learner = qlearningAgents.QLearningAgent(actionFn=actionFn)

        self.learner.setEpsilon(self.Epsilon)
        self.learner.setLearningRate(self.LearningRate)
        self.learner.setDiscount(self.Discount)



    def __initGUI(self):
        # # Window ##

        win = tkinter.Tk()
        self.win = win

        win.title('Crawler GUI')
        win.resizable(0, 0)
        win.wm_attributes("-topmost", True)

        win.protocol('WM_DELETE_WINDOW', self.exitButton)

        # # Epsilon Button + Label ##
        # # Gamma Button + Label ##
        # # Alpha Button + Label ##
        self.setupTrainingParaters(win)
        self.setupRunOrPause(win)
        self.setupStateAndAction(win)
        self.setupQButtons(win)
        self.setupSkipButton(win)

        for child in win.winfo_children():
            child.grid_configure(padx=4, pady=1)


        # # Canvas ##
        self.canvas = tkinter.Canvas(win, height=620, width=1000)
        self.canvas.grid(row=4, columnspan=10)
        self.analysisY = 570


    def setParam(self, param):
        # print(self, param)
        strParam = getattr(self, param + 'Text').get()
        if strParam:
            floatParam = float(strParam)
            if floatParam >= 0 and floatParam <= 2:
                setattr(self, 'param', floatParam)
                getattr(self.learner, 'set' + param)(floatParam)
                # if custFunc:
                    # custFunc(floatParam)
                getattr(self, param + 'Label')['text'] = '%s: %.3f' % (param, floatParam)
        getattr(self, param + 'Text').delete(0, 'end')


    def setupTrainingParaters(self, win):

        parameters = ['LearningRate', 'Discount', 'Epsilon']
        paramRow = 1
        col = 6
        for param in parameters:
            paramLabel = tkinter.Label(win,
                    text='%s: %.3f' % (param, getattr(self, param)))
            setattr(self, param + 'Label', paramLabel)
            paramLabel.grid(row=paramRow, column=col, sticky=tkinter.E)

            paramText = tkinter.Entry(win, width=7, bd=3)
            setattr(self, param + 'Text', paramText)
            paramText.grid(row=paramRow, column=col + 1, sticky=tkinter.W)
            paramText.bind('<Return>', lambda event, p=param: self.setParam(p))

            paramRow += 1


    def setSkipSteps(self):
        strStep = self.textskip.get()
        if strStep:
            steps = int(strStep)
            if steps > 0:
                self.stepsToSkip = steps

        # self.textskip.delete(0, 'end')
        self.setSingleStep()


    def setupSkipButton(self, win):
        self.skipBut = tkinter.Button(win,
            text="Skip # steps", command=self.setSkipSteps)
        self.skipBut.grid(row=0, column=6, sticky=tkinter.E)
        self.manualButtons.append(self.skipBut)

        self.textskip = tkinter.Entry(win, width=7, bd=3)
        self.textskip.grid(row=0, column=7, sticky=tkinter.W)
        self.manualButtons.append(self.textskip)


    def stringPauseRun(self):
        if self.pause == True:
            text = ' Run '
        else:
            text = 'Pause'
        return text


    def setPauseRun(self):
        self.pause = not self.pause
        self.pauseRunBut['text'] = self.stringPauseRun()
        if self.pause == False:
            self.manualAction = None

        for i in self.manualButtons:
            i.config(state=self.getStatePauseOnly())


    def setSingleStep(self):
        self.manualAction = 'auto'
        self.pause = False


    def getStatePauseOnly(self):
        if self.pause == False:
            return tkinter.DISABLED
        else:
            return tkinter.NORMAL


    def setupRunOrPause(self, win):
        # run and pause
        self.manualButtons = []
        self.pauseRunBut = tkinter.Button(win, text=self.stringPauseRun(), command=self.setPauseRun)
        self.pauseRunBut.grid(row=0, column=0, sticky=tkinter.E)


        self.debugBut = tkinter.Button(win,
        text='Single Step', command=(lambda: self.setSingleStep()))
        self.debugBut.grid(row=0, column=1)
        self.manualButtons.append(self.debugBut)


    def updateState(self):
        strArm, strHand = self.textArm.get(), self.textHand.get()
        if strArm and strHand:
            arm, hand = int(strArm), int(strHand)
            if arm >= 0 and arm < self.robotEnvironment.nArmStates and hand >= 0 and hand < self.robotEnvironment.nHandStates:
                if hand - 1 >= 0:
                    self.robotEnvironment.setCurrentState((arm, hand - 1))
                    self.manualAction = 'hand-up'
                else:
                    self.robotEnvironment.setCurrentState((arm, hand + 1))
                    self.manualAction = 'hand-down'
                self.pause = False
        self.textArm.delete(0, 'end')
        self.textHand.delete(0, 'end')

    def updateAction(self, action):
        if action in self.robotEnvironment.getPossibleActions(self.robotEnvironment.getCurrentState()):
            self.manualAction = action
            self.pause = False



    def setupStateAndAction(self, win):


        # set state
        self.setStateBut = tkinter.Button(win, text='Set State', command=self.updateState)
        self.setStateBut.grid(row=1, column=0, sticky=tkinter.E)
        self.manualButtons.append(self.setStateBut)

        self.textArm = tkinter.Entry(win, width=5, bd=3)
        self.textArm.grid(row=1, column=1)
        self.manualButtons.append(self.textArm)

        self.textHand = tkinter.Entry(win, width=5, bd=3)
        self.textHand.grid(row=1, column=2, sticky=tkinter.W)
        self.manualButtons.append(self.textHand)


        # set action
        self.arm_minus = tkinter.Button(win,
        text="-", command=(lambda: self.updateAction('arm-down')))
        self.arm_minus.grid(row=2, column=0, sticky=tkinter.E)
        self.manualButtons.append(self.arm_minus)

        self.arm_label = tkinter.Label(win, text='Arm: -1')
        self.arm_label.grid(row=2, column=1)
        self.manualButtons.append(self.arm_label)

        self.arm_plus = tkinter.Button(win,
        text="+", command=(lambda: self.updateAction('arm-up')))
        self.arm_plus.grid(row=2, column=2, sticky=tkinter.W)
        self.manualButtons.append(self.arm_plus)

        self.hand_minus = tkinter.Button(win,
        text="-", command=(lambda: self.updateAction('hand-down')))
        self.hand_minus.grid(row=3, column=0, sticky=tkinter.E)
        self.manualButtons.append(self.hand_minus)

        self.hand_label = tkinter.Label(win, text='Hand: -1')
        self.hand_label.grid(row=3, column=1)
        self.manualButtons.append(self.hand_label)

        self.hand_plus = tkinter.Button(win,
        text="+", command=(lambda: self.updateAction('hand-up')))
        self.hand_plus.grid(row=3, column=2, sticky=tkinter.W)
        self.manualButtons.append(self.hand_plus)


    def dumpQvalues(self):
        fileName = self.textFileName.get()
        if fileName:
            with open(fileName , 'wb') as handle:
                pickle.dump(self.learner.qvalues, handle)



    def loadQvalues(self):
        fileName = self.textFileName.get()
        if fileName:
            with open(fileName, 'rb') as handle:
                self.learner.qvalues = pickle.loads(handle.read())
                self.learner.visited = collections.Counter()
                self.appDraw()

    def resetQvalues(self):
        self.learner.qvalues = collections.Counter()
        self.learner.visited = collections.Counter()
        self.appDraw()


    def setupQButtons(self, win):
        col = 4
        self.dumpQButton = tkinter.Button(win, text='Dump QValues', command=self.dumpQvalues)
        self.dumpQButton.grid(row=0, column=col)

        self.textFileName = tkinter.Entry(win, width=12, bd=3)
        self.textFileName.grid(row=1, column=col)
        self.textFileName.insert(tkinter.END, 'qvalue_%04d.log' % random.randint(0, 10000))

        self.loadQButton = tkinter.Button(win, text='Load QValues', command=self.loadQvalues)
        self.loadQButton.grid(row=2, column=col)

        self.resetQButton = tkinter.Button(win, text='Reset QValues', command=self.resetQvalues)
        self.resetQButton.grid(row=3, column=col)


    def start(self):
        self.win.mainloop()

    def appDraw(self):
        robot = self.robot
        robot.draw(self.stepCount)

        nArmStates = self.robotEnvironment.nArmStates
        nHandStates = self.robotEnvironment.nHandStates

        values = []
        for i in range(nArmStates):
            for j in range(nHandStates):
                s = (i, j)
                values.extend([self.learner.getQValue(s, a) for a in self.robotEnvironment.getPossibleActions(s)])


        minVal = min(values)
        maxVal = max(values)

        def getColor(val, minV, maxV, bgColor=True):
            r, g, b = 0.0, 0.0, 0.0
            if val < 0 and minV < 0:
                r = val * 0.65 / minV
            if val > 0 and maxV > 0:
                g = val * 0.65 / maxV
            if val == 0 and bgColor == True:
                return 'grey'
            else:
                return '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))

        def draw_poly(a, x, y, w, h, color, value):
            t = None
            fontColor = 'white' if abs(value) >= 0.1 else color
            text_settings = {'fill': fontColor, 'font':('Helvetica', 7)}
            half_w, half_h = w / 2, h / 2
            qualter_w, qualter_h = w / 4 - 2, h / 4 - 1
            if a == 'hand-down':
                # down
                p = self.canvas.create_polygon([(x, y + h), (x + w, y + h), (x + half_w, y + half_h)], fill=color, outline='')
                t = self.canvas.create_text(x + half_w, y + h - qualter_h, text='%.1f' % value, **text_settings)
            elif a == 'hand-up':
                # 'up'
                p = self.canvas.create_polygon([(x, y), (x + w, y), (x + half_w, y + half_h)], fill=color, outline='')
                t = self.canvas.create_text(x + half_w, y + qualter_h, text='%.1f' % value, **text_settings)
            elif a == 'arm-down':
                # left
                p = self.canvas.create_polygon([(x, y), (x, y + h), (x + half_w, y + half_h)], fill=color, outline='')
                t = self.canvas.create_text(x + qualter_w, y + half_h, text='%.1f' % value, **text_settings)
            elif a == 'arm-up':
                # right
                p = self.canvas.create_polygon([(x + w, y + h), (x + w, y), (x + half_w, y + half_h)], fill=color, outline='')
                t = self.canvas.create_text(x + w - qualter_w, y + half_h, text='%.1f' % value, **text_settings)
            return (p, t)


        x_0, y_0, w, h, g = 30, self.analysisY, 48, 32, 2

        if 'analysis_values' in dir(self):
            for j in range(nHandStates):
                for i in range(nArmStates):
                    value = self.learner.computeValueFromQValues((i, j))
                    color = getColor(value, minVal, maxVal)
                    self.canvas.itemconfig(self.analysis_values[j][i][0], fill=color , outline='black', width=1)
                    self.canvas.itemconfig(self.analysis_values[j][i][1], text='%.2f' % value)

                    for ai, a in enumerate (('hand-down', 'hand-up', 'arm-down', 'arm-up')):
                        value = self.learner.getQValue((i, j), a)
                        color = getColor(value, minVal, maxVal, self.learner.visited[((i, j), a)] == 0)
                        self.canvas.itemconfig(self.analysis_qvalues[j][i][ai][0], fill=color, outline='', width=1)
                        fontColor = 'white' if abs(value) >= 0.1 else color
                        self.canvas.itemconfig(self.analysis_qvalues[j][i][ai][1], text='%.1f' % value, fill=fontColor)

        else:
            self.analysis_values = [[0] * nArmStates for i in range(nHandStates)]

            y = y_0
            for j in range(self.robotEnvironment.nHandStates):
                x = x_0
                for i in range(self.robotEnvironment.nArmStates):
                    value = self.learner.computeValueFromQValues((i, j))
                    color = getColor(value, minVal, maxVal)
                    qr = self.canvas.create_rectangle(x, y, x + w, y + h, fill=color)
                    qt = self.canvas.create_text(x + w / 2, y + h / 2, text='%.2f' % value, fill='white')
                    self.analysis_values[j][i] = (qr, qt)
                    x += w + g
                y -= h + g


            self.analysis_qvalues = [[0] * nArmStates for i in range(nHandStates)]

            x_1 = x + 40
            y = y_0



            for j in range(self.robotEnvironment.nHandStates):
                x = x_1
                for i in range(self.robotEnvironment.nArmStates):
                    avalues = []
                    for a in ('hand-down', 'hand-up', 'arm-down', 'arm-up'):
                        value = self.learner.getQValue((i, j), a)
                        color = getColor(value, minVal, maxVal, self.learner.visited[((i, j), a)] == 0)
                        avalues.append(draw_poly(a, x, y, w, h, color, value))
                    self.analysis_qvalues[j][i] = avalues
                    x += w + g
                y -= h + g


        if self.stepCount > 0:
            r_i, r_j = self.robotEnvironment.getCurrentState()
            value = self.learner.computeValueFromQValues((r_i, r_j))
            self.canvas.itemconfig(self.analysis_values[r_j][r_i][0], fill='orange')
            self.canvas.itemconfig(self.analysis_values[r_j][r_i][1], text='%.2f' % value)
            l_i, l_j = self.robotEnvironment.lastState
            self.canvas.itemconfig(self.analysis_values[l_j][l_i][0], outline='orange', width=2)


            ai = ['hand-down', 'hand-up', 'arm-down', 'arm-up'].index(self.robot.nextAction)
            self.canvas.itemconfig(self.analysis_qvalues[r_j][r_i][ai][0], outline='orange', width=2)


            self.arm_label['text'] = 'Arm: %d' % r_i
            self.hand_label['text'] = 'Hand: %d' % r_j
            self.LearningRateLabel['text'] = 'LearningRate: %.3f' % self.learner.alpha


    def step(self, skip_drawing=False):

        # time1 = time.time()- self.timeNow
        # self.timeNow = time.time()
        self.stepCount += 1

        state = self.robotEnvironment.getCurrentState()

        # print(self.stepCount, self.learner.discount, self.manualAction)


        # manual mode: overwrite next action
        if self.manualAction == 'auto' or self.manualAction is None:
            if self.robot.nextAction == None:
                action = self.learner.getAction(state)
            else:
                action = self.robot.nextAction
        else:
            action = self.manualAction
            self.manualAction = 'auto'

        # record last State
        self.robotEnvironment.lastState = state

        if action == None:
            raise Exception('None action returned: Code Not Complete')
        nextState, reward = self.robotEnvironment.doAction(action)
        self.learner.observeTransition(state, action, nextState, reward)


        actions = self.robotEnvironment.getPossibleActions(nextState)
        if len(actions) == 0.0:
            self.robotEnvironment.reset()
            nextState = self.robotEnvironment.getCurrentState()
            actions = self.robotEnvironment.getPossibleActions(nextState)
            print('Reset!')

        self.robot.nextAction = self.learner.getAction(nextState)

        if skip_drawing == False:
            self.appDraw()


    def appRun(self):

        if not self.pause:
            for _ in range(self.stepsToSkip):
                self.step(skip_drawing=True)
            self.stepsToSkip = 0
            self.step()
            if self.manualAction is not None:
                self.pause = True
            afterTime = 100
        else:

            afterTime = 500

        self.win.after(afterTime, self.appRun)

    def exitButton(self):
        self.win.destroy()

def CrawlerRun():
    app = Application()
    app.win.after(100, app.appRun)
    app.start()
    print('system exiting')
    sys.exit(0)


if __name__ == '__main__':
    CrawlerRun()

