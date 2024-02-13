from abc import ABCMeta, abstractmethod
import copy
from Processor import *
from Process import *

class CSchedule(metaclass=ABCMeta) : # 스케쥴링(프로세스 이동)
    def __init__(self) :
        self.CurrentTime = 0 # 현재시간
        self.ReadyQueue = [] # 레디큐
        self.processlist = [] # 프로세스리스트
        self.processorlist = [] # 프로세서리스트
        self.processorcount = 0 # 프로세서 개수
        self.processcount = 0 # 프로세스 개수
        self.timequantum = 0 # RR 타임퀀텀
        self.record = [] # 레디큐 기록
        self.finished_processlist = []

    def CreateProcessor(self, type): #processorallocate
        self.processorcount += 1 #프로세서 인덱스 지정
        self.processorlist.append(CProcessor(self.processorcount,type))
    
    def CreateProcess(self, AT, BT, PRIORITY=1):
        self.processcount += 1 #프로세스 인덱스 지정
        self.processlist.append(CProcess(self.processcount,AT,BT,PRIORITY))

    def ReadyQallocate(self) : #레디큐에 AT별 프로세스할당
        processindexlist = [] # 프로세스리스트 인덱스 리스트
        for i in range(len(self.processlist)):
            if self.CurrentTime == self.processlist[i].AT:
                self.ReadyQueue.append(self.processlist[i])
                processindexlist.append(i)
    # 리스트의 pop연산시 리스트에 있는 항목들의 인덱스값 바뀜 -> 인덱스 유지시킨 후 나중에 제거

        if len(self.processlist) > 0:
            for k in range(len(processindexlist)-1,-1,-1):
                i = processindexlist[k]
                self.processlist.pop(i)

    # 인덱스가 작은 거부터 제거하면 뒤의 모든 항목의 인덱스가 바뀜 -> 인덱스가 큰 거부터 제거하면
    #                                                                 앞의 항목의 인덱스는 안바뀜

    def working(self) : # working 정의
        for i in range(len(self.processorlist)) :
            if self.processorlist[i].isEmpty() is True : # 일을 안할 때
                self.processorlist[i].throughput.append(0) # 작업량 기록
                self.processorlist[i].runningtime.append(0) # 작업시간 기록
                self.processorlist[i].runningprocessid.append(0) #일안했음.프로세스id없음
            elif self.processorlist[i].process.RMT == 1 and self.processorlist[i].core == 'P' : # RMT가 1, P코어일때 
                self.processorlist[i].process.RMT -= 1 # RMT는 1 감소
                self.processorlist[i].throughput.append(1) # 작업량 기록
                self.processorlist[i].runningtime.append(1) # 작업시간 기록
                self.processorlist[i].runningprocessid.append(self.processorlist[i].process.id) #일했음.프로세스id 삽입.
            else : # 위의 상황을 제외한 나머지
                self.processorlist[i].process.RMT -= self.processorlist[i].performance # RMT는 코어의 성능만큼 감소
                self.processorlist[i].throughput.append(self.processorlist[i].performance)  # 작업량 기록
                self.processorlist[i].runningtime.append(1)  # 작업시간 기록
                self.processorlist[i].runningprocessid.append(self.processorlist[i].process.id) #일했음.프로세스id 삽입.

            if(self.processorlist[i].process is not None):
                if self.processorlist[i].process.RMT == 0 : # 남은 실행 시간이 0이면
                    self.processorlist[i].process.finishtime = self.CurrentTime +1 # 프로세스가 종료된 시간은 현재시간 + 1
                    self.processorlist[i].process.TT = self.processorlist[i].process.finishtime - self.processorlist[i].process.AT # TT계산
                    self.processorlist[i].process.NTT = float(self.processorlist[i].process.TT) / float(self.processorlist[i].process.BT) # NTT계산
                    self.finished_processlist.append(copy.deepcopy(self.processorlist[i].process)) # 종료된 프로세스는 finished_processlist에 저장
                    self.finished_processlist = sorted(self.finished_processlist, key=lambda x: x.id)        
            self.processorlist[i].clearprocess(self.CurrentTime) # RMT가 0인 프로세스 방출
        self.record.append(copy.deepcopy(self.ReadyQueue)) # 작업이 끝나면 레디큐 정보를 기록


# 작업이 끝난 프로세스리스트를 id순으로 정렬

#def get_WT() : # 스케줄링 종료 후 WT계산
#    for i in range(len(finished_processlist)):
#        finished_processlist[i].WT = 0 # 모든 프로세스의 WT 초기화
#        CountingRunning = 0
#        for j in range(len(test.processorlist)):
#            for k in range(finished_processlist[i].AT, finished_processlist[i].finishtime,1):
#                if (test.processorlist[j].runningprocessid[k] == finished_processlist[i].id):
#                    CountingRunning += 1
#        finished_processlist[i].WT = finished_processlist[i].TT-CountingRunning
