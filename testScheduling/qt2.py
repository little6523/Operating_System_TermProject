import sys
import os
from PyQt5 import QtWidgets,QtGui,uic
from PyQt5.QtWidgets import *
from FCFS import *
from RR import *
from SPN import *
from SRTN import *
from HRRN import *
from RPN import *
from Processor import *

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('qt2.ui')
form_class = uic.loadUiType(form)[0]
test=CSchedule()

class MainClass(QMainWindow, form_class):

    process_color=[
        {'color1':255,'color2':153,'color3':153},{'color1':204,'color2':230,'color3':255},
        {'color1':255,'color2':102,'color3':102},{'color1':255,'color2':153,'color3':204},
        {'color1':230,'color2':255,'color3':153},{'color1':153,'color2':204,'color3':255},
        {'color1':153,'color2':153,'color3':255},{'color1':0,'color2':255,'color3':128},
        {'color1':230,'color2':204,'color3':255},{'color1':64,'color2':255,'color3':0},
        {'color1':102,'color2':255,'color3':179},{'color1':153,'color2':179,'color3':255},
        {'color1':255,'color2':153,'color3':255},{'color1':204,'color2':255,'color3':242},
        {'color1':255,'color2':217,'color3':236},{'color1':255,'color2':255,'color3':255}    ]
    process_record=[]
    process_init=[]
    rowCount=0
    ColumnCount=0
    processor_number=0
    time=0
    algo=''

    def __init__(self) :
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton_add_process.clicked.connect(self.add)
        self.pushButton_add_processor.clicked.connect(self.add_processor)
        self.pushButton_reset.clicked.connect(self.reset)
        self.pushButton_prev.clicked.connect(self.prev)
        self.pushButton_next.clicked.connect(self.next)
        self.pushButton_start.clicked.connect(self.start)
        self.comboBox_Alist.currentIndexChanged.connect(self.select)
        self.lineEdit_quantum.setEnabled(False)
        self.comboBox_Priority.setEnabled(False)

    def select(self): # 알고리즘 선택
        self.algo = self.comboBox_Alist.currentText()
        if self.algo=='RR':
            self.lineEdit_quantum.setEnabled(True)
            self.comboBox_Priority.setEnabled(False)
            self.test = RR()
        elif self.algo=='FCFS': 
            self.lineEdit_quantum.setEnabled(False)
            self.comboBox_Priority.setEnabled(False)
            self.test = FCFS()
        elif self.algo=='HRRN': 
            self.lineEdit_quantum.setEnabled(False)
            self.comboBox_Priority.setEnabled(False)
            self.test = HRRN()
        elif self.algo=='SRTN': 
            self.lineEdit_quantum.setEnabled(False)
            self.comboBox_Priority.setEnabled(False)
            self.test = SRTN()
        elif self.algo=='SPN': 
            self.lineEdit_quantum.setEnabled(False)
            self.comboBox_Priority.setEnabled(False)
            self.test = SPN()
        elif self.algo=='RPN': 
            self.lineEdit_quantum.setEnabled(False)
            self.test = RPN()
            self.comboBox_Priority.setEnabled(True)
        
    def ready_queue_display(self): # 레디큐 디스플레이
        time=self.time
        number=len(self.test.record[time])
        self.tableWidget_queue.setColumnCount(number)
        for i in range(number):
            item = QtWidgets.QTableWidgetItem(i)
            self.tableWidget_queue.setHorizontalHeaderItem(i, item)
            str1="P"+str(self.test.record[time][i].id)
            self.tableWidget_queue.setItem(0,i, QtWidgets.QTableWidgetItem(str1)) #내용 세팅
            id=self.test.record[time][i].id-1
            self.tableWidget_queue.item(0,i).setBackground(QtGui.QColor(self.process_color[id]['color1'],self.process_color[id]['color2'],self.process_color[id]['color3']))
        
    def gantt_display(self): #간트 디스플레이
        self.tableWidget_gantt.insertColumn(self.time) # 1 행추가 (1) ==> NEXT누를때마다 행추가 
        header_v=self.tableWidget_gantt.verticalHeader()
        for i in range(self.processor_number): # 프로세스 수 반복
            str1=""
            if self.test.processorlist[i].runningprocessid[self.time]!=0 :
                str1="P"+str(self.test.processorlist[i].runningprocessid[self.time]) # 여기에 현재 들어올 프로세스 입력
            if self.test.processorlist[i].core=='P' and self.test.processorlist[i].throughput[self.time]==1:
                str1="P"+str(self.test.processorlist[i].runningprocessid[self.time])+"     (1) "
            self.tableWidget_gantt.setItem(i,self.ColumnCount, QtWidgets.QTableWidgetItem(str1)) #str1 값대로 각 행에 입력
            id=int(self.test.processorlist[i].runningprocessid[self.time])-1
            self.tableWidget_gantt.item(i,self.ColumnCount).setBackground(QtGui.QColor(self.process_color[id]['color1'],self.process_color[id]['color2'],self.process_color[id]['color3']))
            for i in range(self.processor_number):
                header_v.resizeSection(i,int(190/self.processor_number+1))
            
    def result_display(self): #결과 디스플레이
        self.rowCount=0
        for j in range(len(self.test.finished_processlist)):
            str1="P"+str(self.test.finished_processlist[j].id)
            AT=self.test.finished_processlist[j].AT
            BT=self.test.finished_processlist[j].BT
            TT=self.test.finished_processlist[j].TT
            WT=self.test.finished_processlist[j].WT 
            NTT=round(self.test.finished_processlist[j].NTT, 2)
            self.tableWidget_result.insertRow(self.rowCount)
            self.tableWidget_result.setItem(self.rowCount,0,QtWidgets.QTableWidgetItem(str1))
            self.tableWidget_result.setItem(self.rowCount,1,QtWidgets.QTableWidgetItem(str(AT)))
            self.tableWidget_result.setItem(self.rowCount,2,QtWidgets.QTableWidgetItem(str(BT)))
            self.tableWidget_result.setItem(self.rowCount,3,QtWidgets.QTableWidgetItem(str(WT)))
            self.tableWidget_result.setItem(self.rowCount,4,QtWidgets.QTableWidgetItem(str(TT)))
            self.tableWidget_result.setItem(self.rowCount,5,QtWidgets.QTableWidgetItem(str(NTT)))
            id = self.test.finished_processlist[j].id-1
            self.tableWidget_result.item(self.rowCount,0).setBackground(QtGui.QColor(self.process_color[id]['color1'],self.process_color[id]['color2'],self.process_color[id]['color3']))
            self.rowCount+=1

    def get_WT(self) : # 스케줄링 종료 후 WT계산
        for i in range(len(self.test.finished_processlist)):
            self.test.finished_processlist[i].WT = 0 # 모든 프로세스의 WT 초기화
            CountingRunning = 0
            for j in range(len(self.test.processorlist)):
                for k in range(self.test.finished_processlist[i].AT, self.test.finished_processlist[i].finishtime,1):
                    if (self.test.processorlist[j].runningprocessid[k] == self.test.finished_processlist[i].id):
                        CountingRunning += 1
            self.test.finished_processlist[i].WT = self.test.finished_processlist[i].TT-CountingRunning

    def start(self): #레디큐 보여주기
        #cpu 입력받았을때만
        self.process_init=self.test.processlist.copy()
        self.tableWidget_queue.setRowCount(1)
        self.process_record=self.test.processlist.copy()
        self.test.run()
        self.get_WT()
        self.ready_queue_display()
        self.gantt_display()
        self.result_display()
        str1="Real time = "+str(self.time+1)+ " sec"
        self.label_time.setText(str1)
        WATT=0.0
        WATTA=0
        WATTB=0
        for j in range(len(self.test.processorlist)):
            tatalrun=0
            tatalrun += self.test.processorlist[j].runningtime[0]
            A=(tatalrun*self.test.processorlist[j].power_consumption)
            B=((self.time+1-tatalrun)*self.test.processorlist[j].waitingpower)
            WATTA+=A
            WATTB+=B
        WATT=WATTA+WATTB/10
        str1="소비전력 : "+str(WATT)+ " W "
        self.label_Watt.setText(str1)
        
    def add(self): # 프로세스 추가 (이름,at,bt)
        AT = self.lineEdit_AT.text()
        BT = self.lineEdit_BT.text()
        PRIORITY=1
        if self.algo=='RPN':
            str1=self.comboBox_Priority.currentText()
            if str1=='실시간' :
                PRIORITY=1
            elif str1=='높음' :
                PRIORITY=2
            elif str1=='높은우선순위' :
                PRIORITY=3
            elif str1=='보통' :
                PRIORITY=4
            elif str1=='낮은우선순위' :
                PRIORITY=5
            elif str1=='낮음' :
                PRIORITY=6   
        if self.rowCount<15:
            self.test.CreateProcess(int(AT),int(BT),PRIORITY)
        if AT and BT is not None and self.rowCount<15:
            self.tableWidget_Timetable.insertRow(self.rowCount)
            if self.algo=='RPN':
                str1="P"+str(self.rowCount+1)+"     "+str1
            else: str1="P"+str(self.rowCount+1)
            self.tableWidget_Timetable.setItem(self.rowCount,0,QtWidgets.QTableWidgetItem(str1))
            self.tableWidget_Timetable.setItem(self.rowCount,1,QtWidgets.QTableWidgetItem(AT))
            self.tableWidget_Timetable.setItem(self.rowCount,2,QtWidgets.QTableWidgetItem(BT))
            if self.algo=='RPN':
                self.tableWidget_Timetable.setItem(self.rowCount,3,QtWidgets.QTableWidgetItem(PRIORITY))
            self.tableWidget_Timetable.item(self.rowCount, 0).setBackground(QtGui.QColor(self.process_color[self.rowCount]['color1'],self.process_color[self.rowCount]['color2'],self.process_color[self.rowCount]['color3']))
            self.rowCount+=1
        
    def add_processor(self):
        self.processor_type = self.lineEdit_Type.text()
        if self.algo=='RR':
            self.Quantum = int(self.lineEdit_quantum.text())
            self.test.settimequantum(self.Quantum)
        if not (self.processor_type=='P' or self.processor_type=='E') : return
        self.processor_number+=1
        if self.processor_number>4: return
        self.test.CreateProcessor(self.processor_type)
        self.tableWidget_gantt.setRowCount(self.processor_number) #열설정
        header_v=self.tableWidget_gantt.verticalHeader() 
        for i in range(self.processor_number-1,self.processor_number): # i는 0~프로세서 수
            str1="CPU"+str(i+1)+"("+self.processor_type+")"
            item=QtWidgets.QTableWidgetItem(str1)
            self.tableWidget_gantt.setVerticalHeaderItem(i, item)
        for i in range(self.processor_number):
            header_v.resizeSection(i,int(220/self.processor_number+1))

    def prev(self):
        if self.time!=0 :
            self.time-=1
        str1="Real time = "+str(self.time+1)+ " sec"
        self.label_time.setText(str1)
        self.ready_queue_display()
        if self.ColumnCount>0 : self.ColumnCount-=1
        self.tableWidget_gantt.removeColumn(self.time+1) 
        WATT=0
        WATTA=0
        WATTB=0
        for i in range(len(self.test.processorlist)):
            tatalrun=0
            for j in range(self.time+1):
                tatalrun += self.test.processorlist[i].runningtime[j]      
            A=(tatalrun*self.test.processorlist[i].power_consumption)
            B=((self.time+1-tatalrun)*self.test.processorlist[i].waitingpower)
            WATTA+=A
            WATTB+=B
        WATT=WATTA+WATTB/10
        str1="소비전력 : "+str(WATT)+ " W "
        self.label_Watt.setText(str1)
    
    def next(self):
        if self.test.CurrentTime>self.time+1:
            self.time+=1
            str1="Real time = "+str(self.time+1)+ " sec"
            self.label_time.setText(str1)
        else: return
        self.ready_queue_display()
        self.ColumnCount+=1
        self.gantt_display()
        WATT=0
        WATTA=0
        WATTB=0
        for i in range(len(self.test.processorlist)):
            tatalrun=0
            for j in range(self.time+1):
                tatalrun += self.test.processorlist[i].runningtime[j]      
            A=(tatalrun*self.test.processorlist[i].power_consumption)
            B=((self.time+1-tatalrun)*self.test.processorlist[i].waitingpower)
            WATTA+=A
            WATTB+=B
        WATT=WATTA+WATTB/10
        str1="소비전력 : "+str(WATT)+ " W "
        self.label_Watt.setText(str1)
       
    def reset(self): #초기화
        self.tableWidget_Timetable.setRowCount(0)
        self.tableWidget_queue.setRowCount(0)
        self.tableWidget_queue.setColumnCount(0)
        self.tableWidget_result.setRowCount(0)
        self.tableWidget_gantt.setRowCount(0)
        self.tableWidget_gantt.setColumnCount(0)
        self.rowCount=0
        self.test=CSchedule()
        self.processor_number=0
        self.process_record=[]
        self.process_init=[]
        self.ColumnCount=0
        self.time=0
        
    
if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    window = MainClass() 
    window.show()
    app.exec_()