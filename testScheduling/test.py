from FCFS import *
from RR import *
from SPN import *
from SRTN import *
from HRRN import *
from RPN import *
from Processor import *


def get_WT() : # 스케줄링 종료 후 WT계산
    for i in range(len(finished_processlist)):
        finished_processlist[i].WT = 0 # 모든 프로세스의 WT 초기화
        CountingRunning = 0
        for j in range(len(test.processorlist)):
            for k in range(finished_processlist[i].AT, finished_processlist[i].finishtime,1):
                if (test.processorlist[j].runningprocessid[k] == finished_processlist[i].id):
                    CountingRunning += 1
        finished_processlist[i].WT = finished_processlist[i].TT-CountingRunning

test = FCFS()

test.CreateProcess(0,3)
test.CreateProcess(0,7)


#test.settimequantum(2) #타임퀀텀 받음

test.CreateProcessor('P')

#test.CreateProcessor('E')

for i in range (len(test.processlist)) :
    print(test.processlist[i].AT, test.processlist[i].BT)

for i in range (len(test.processorlist)) :
    if test.processorlist[i].process is not None:
        print(test.processorlist[i].process.RMT)
    elif test.processorlist[i].process is None:
        print(test.processorlist[i].id,"번 프로세서 : None")

print('현재시간', test.CurrentTime)

test.run()

for j in range(len(test.record)):
    if test.record[j] is not None:
        print('##',j,'초 레디큐')
        for i in range(len(test.record[j])):
                print('id : ', test.record[j][i].id ,'AT : ',test.record[j][i].AT,'RMT : ',test.record[j][i].RMT, 'PRIORITY : ' ,test.record[j][i].PRIORITY)

        print()

for j in range(len(test.processorlist)):
    print(j+1,'번 프로세서')
    for i in range(test.CurrentTime) :
        print(i+1, '초' ,' 프로세스id :' ,  test.processorlist[j].runningprocessid[i], end=' ')
        print('일한 양',test.processorlist[j].throughput[i],' ',end=' ')
        print()
    print()

for j in range(len(test.processorlist)):
    print(j+1,'번 프로세서 소비전력 = ',end = '')
    tatalrun = sum(test.processorlist[j].runningtime)
    print((tatalrun*test.processorlist[j].power_consumption) + ((test.CurrentTime-tatalrun)*test.processorlist[j].waitingpower ))
    
print()

finished_processlist = sorted(finished_processlist, key=lambda x: x.id)

get_WT()

for j in range(len(finished_processlist)):
    print(finished_processlist[j].id,'번 프로세스 :',end = '')
    print('AT : ',finished_processlist[j].AT,end = ' ')
    print('BT : ',finished_processlist[j].BT,end = ' ')
    print('TT : ',finished_processlist[j].TT,end = ' ')
    print('WT : ',finished_processlist[j].WT,end = ' ')
    print('NTT : ',round(finished_processlist[j].NTT, 2),end = ' ')
    print()


print()
print()
print()
print()
print('일이 끝난시간', test.CurrentTime,'초')
for i in range (len(test.processorlist)) :
    if test.processorlist[i].process is not None:
        print(test.processorlist[i].process.RMT)
    elif test.processorlist[i].process is None:
        print(test.processorlist[i].id,"번 프로세서", sum(test.processorlist[i].throughput),"만큼 일함", sum(test.processorlist[i].runningtime),"초 일함")