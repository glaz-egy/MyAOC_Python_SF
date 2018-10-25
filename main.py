# -*- coding: utf-8 -*-

from copy import deepcopy
from numpy.random import *
import wx

ColorDict = {0: '',
            -1: 'green',
            -2: 'yellow',
            -100: 'black',
            -200: 'red'}

AntCanMove = (-15, -1, 15, 1)

class Ants:
    def __init__(self, AntsNum=40, DepartureNum=10):
        self.AntsNum = AntsNum
        self.DepartureNum = DepartureNum
        self.MaxPherom = 200

    def MoveAnts(self, MapData):
        for _ in range(self.DepartureNum):
            for _ in range(self.AntsNum):
                pass
        self.AntMoveing(MapData)
    
    def AntMoveing(self, MapData):
        MoveList = [16, ]
        OverLapList = []
        OverLapDict = {}
        Now = MapData.index(-1)
        CompFlag = False
        for i in range(len(MapData)):
            if not MapData[i] in (-200, -100, -1, -2):
                MapData[i] *= 0.5
        while MapData[MoveList[-1]] != -2 and not CompFlag:
            NextList = []
            temp = 0
            for Next in AntCanMove:
                if MapData[Now+Next] == -2:
                    MoveList.append(Now+Next)
                    CompFlag = True
                    break
                elif not MapData[Now+Next] in (-200, -100, -1) and not Now+Next == MoveList[-1]:
                    temp += MapData[Now+Next] if MapData[Now+Next] != 0 else 1
                    NextList.append([Now+Next, temp])
            if not CompFlag:
                NextRand = rand()*NextList[-1][1]
                for List in NextList:
                    if List[1] >= NextRand:
                        MoveList.append(List[0])
                        Now = List[0]
                        break
        Pherom = self.MaxPherom / (len(MoveList)-2)
        for i in MoveList:
            if not MapData[i] in (-200, -100, -1, -2):
                if not i in OverLapList:
                    OverLapList.append(i)
                    OverLapDict[i] = 1
                    MapData[i] += Pherom
                else:
                    OverLapDict[i] += 1
                    MapData[i] = (Pherom / OverLapDict[i])
        self.Coloring(MapData)
        print(MapData)

    def Coloring(self, MapData):
        PheromMin = 255/max(MapData)
        for i in range(len(MapData)):
            if not MapData[i] in (-200, -100, -1, -2):
                Color = '{}ffff'.format(hex(255^int(PheromMin*MapData[i])))
                Color = Color.replace('0x', '')
                if len(Color) != 6:
                    Color = '0'+Color
                Color = '#'+Color
                print(Color)
                Field.Button[i].SetBackgroundColour(Color)
        print(Field.Button[46].GetBackgroundColour())

class FieldCtrl:
    def __init__(self, panel):
        self.panel = panel
        self.Button = []
        self.x = self.y = 15
        self.SetButton()
    
    def SetButton(self):
        global MapList
        global LinerMap
        sizer = wx.GridSizer(rows=self.x, cols=self.y, gap=(0, 0))
        for i in range(1, self.y+1):
            minMapList = []
            for j in range(1, self.x+1):
                minMapList.append(0)
                LinerMap.append(0)
                self.Button.append(wx.Button(self.panel, i*100+j, ' '))
                sizer.Add(self.Button[-1], 0, wx.GROW)
                if i == 1 or i == 15 or j == 1 or j == 15:
                    self.Button[-1].SetBackgroundColour('black')
                    minMapList[-1] = -100
                    LinerMap[-1] = -100
                if i == 2 and j == 2:
                    self.Button[-1].SetBackgroundColour('green')
                    minMapList[-1] = -1
                    LinerMap[-1] = -1
                if i == 14 and j == 14:
                    self.Button[-1].SetBackgroundColour('yellow')
                    minMapList[-1] = -2
                    LinerMap[-1] = -2
            MapList.append(minMapList)
        self.InitMapList = deepcopy(MapList)
        self.InitLinerMap = deepcopy(LinerMap)
        self.panel.SetSizer(sizer)
    
    def InitField(self):
        global MapList
        global LinerMap
        MapList = deepcopy(self.InitMapList)
        LinerMap = deepcopy(self.InitLinerMap)
        for y in range(len(self.InitMapList)):
            for x in range(len(self.InitMapList[y])):
                self.Button[PositionCalc((x, y), PositionToButton=True)].SetBackgroundColour(ColorDict[self.InitMapList[y][x]])

def PositionCalc(Num, XandY=False, PositionToButton=False):
    if not XandY and not PositionToButton:
        x, y = Num % 100, Num // 100
        return (15*(y-1))+(x-1)
    elif XandY:
        return ((Num % 100)-1, (Num // 100)-1)
    elif PositionToButton:
        x, y = Num
        return (15*y)+x

def PushButton(event):
    global MapList
    global LinerMap
    ID = event.GetId()
    if ID == 10000:
        AntAgent.MoveAnts(LinerMap)
    elif ID == 10001:
        Field.InitField()
    else:
        Position = PositionCalc(ID)
        if Field.Button[Position].GetBackgroundColour() in ('black', 'green', 'yellow'):
            pass
        elif Field.Button[Position].GetBackgroundColour() == 'red':
            Field.Button[Position].SetBackgroundColour('')
            x, y = PositionCalc(ID, XandY=True)
            MapList[y][x] = 0
            LinerMap[Position] = 0
        else:
            Field.Button[Position].SetBackgroundColour('red')
            x, y = PositionCalc(ID, XandY=True)
            MapList[y][x] = -200
            LinerMap[Position] = -200


if __name__=='__main__':
    App = wx.App()
    AppName = '俺的蟻コロニー最適化アルゴリズムで迷路を解いてみた'
    Frame = wx.Frame(None, -1, title=AppName, size=(1400, 1000), pos=(0, 0))
    panel = wx.Panel(Frame, -1)
    MapBoard = wx.Panel(panel, -1, size=(100, 100))
    SetBoard = wx.Panel(panel, -1)
    MapList = []
    LinerMap = []
    Field = FieldCtrl(MapBoard)
    AntAgent = Ants()
    ButtonFont = wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
    StartButton = wx.Button(SetBoard, 10000, 'Start')
    StartButton.SetFont(ButtonFont)
    ResetButton = wx.Button(SetBoard, 10001, 'Reset')
    ResetButton.SetFont(ButtonFont)
    SettingSizer = wx.BoxSizer(wx.VERTICAL)
    SettingSizer.Add(StartButton, flag=wx.GROW)
    SettingSizer.Add(ResetButton, flag=wx.GROW)
    SetBoard.SetSizer(SettingSizer)
    BoxSizer = wx.BoxSizer(wx.HORIZONTAL)
    BoxSizer.Add(MapBoard, 8, flag=wx.SHAPED)
    BoxSizer.Add(SetBoard, 2)
    panel.SetSizer(BoxSizer)
    Frame.Bind(wx.EVT_BUTTON, PushButton)
    Frame.Show()
    App.MainLoop()