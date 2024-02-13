from Schedule import *

class RR(CSchedule) : # RR 클래스

    def settimequantum(self, quantum): # 타임퀀텀 설정
        self.timequantum = quantum

    def run(self) : # run함수 재정의
        # 레디큐에 프로세스가 있거나 프로세스리스트에 프로세스가 남아있으면
        while(len(self.ReadyQueue)>0 or len(self.processlist)>0 ) :
            self.ReadyQallocate() # 프로세스리스트에서 현재시간과 AT를 비교하여 레디큐에 삽입
            for i in range(len(self.processorlist)) : # 프로세서 개수만큼 반복
                # i번째 프로세서가 작업중이지 않고, 레디큐에 프로세스가 대기중이면
                if self.processorlist[i].isEmpty() and len(self.ReadyQueue)>0 :
                    self.processorlist[i].allocateprocess(self.ReadyQueue.pop(0)) # 작업중이지 않은 프로세서에 프로세스 할당
                    print(self.processorlist[i].id,"번 프로세서에 레디큐프로세스 할당함") # "~~~print문 삭제예정~~~"

            for i in range(len(self.ReadyQueue)):
                print('#',i,'번째 레디큐원소','AT : ',self.ReadyQueue[i].AT,'RMT : ',self.ReadyQueue[i].RMT)
            self.working() # 작업실행

            print('                   현재시간',self.CurrentTime,'초 ')
            self.CurrentTime += 1 # 작업이 끝나면 현재시간 1 증가
        for i in range(len(self.processorlist)) : # 프로세서의 개수만큼 반복
            while(self.processorlist[i].isEmpty()==False):  # i번째 프로세스가 일을 하는 중이면
                self.working() # 하던 일 마저 진행
                self.CurrentTime += 1 # 작업을 하고 스케줄링이 종료되므로 종료시간은 현재 시간 + 1


    def working(self) : # working 재정의
        for i in range(len(self.processorlist)) :
            if self.processorlist[i].isEmpty() is True : # 일을 안할 때
                self.processorlist[i].throughput.append(0) # 작업량 기록
                self.processorlist[i].runningtime.append(0) # 작업시간 기록
                self.processorlist[i].runningprocessid.append(0) #일안했음.프로세스id없음.
            elif self.processorlist[i].process.RMT == 1 and self.processorlist[i].core == 'P' : # RMT가 1, P코어일때 
                self.processorlist[i].process.RMT -= 1 # RMT는 1 감소
                self.processorlist[i].throughput.append(1) # 작업량 기록
                self.processorlist[i].runningtime.append(1) # 작업시간 기록
                self.processorlist[i].runningprocessid.append(self.processorlist[i].process.id) #일했음.프로세스id 삽입.
                self.processorlist[i].countquantum +=1 # countquantum 1증가
            else : # 위의 상황을 제외한 나머지
                self.processorlist[i].process.RMT -= self.processorlist[i].performance # RMT는 코어의 성능만큼 감소
                self.processorlist[i].throughput.append(self.processorlist[i].performance)  # 작업량 기록
                self.processorlist[i].runningtime.append(1)  # 작업시간 기록
                self.processorlist[i].runningprocessid.append(self.processorlist[i].process.id) #일했음.프로세스id 삽입.
                self.processorlist[i].countquantum +=1 # countquantum 1증가

            if self.processorlist[i].process is not None:
                if self.processorlist[i].process.RMT == 0 : # RMT가 0이 되면
                    self.processorlist[i].countquantum = 0 # countqauntum 초기화
            
            if(self.processorlist[i].process is not None):
                if self.processorlist[i].process.RMT == 0 : # 남은 실행 시간이 0이면
                    self.processorlist[i].process.finishtime = self.CurrentTime +1 # 프로세스가 종료된 시간은 현재시간 + 1
                    self.processorlist[i].process.TT = self.processorlist[i].process.finishtime - self.processorlist[i].process.AT # TT계산
                    self.processorlist[i].process.NTT = float(self.processorlist[i].process.TT) / float(self.processorlist[i].process.BT) # NTT계산
                    self.finished_processlist.append(copy.deepcopy(self.processorlist[i].process)) # 종료된 프로세스는 finished_processlist에 저장
                    self.finished_processlist = sorted(self.finished_processlist, key=lambda x: x.id)             
            self.processorlist[i].clearprocess(self.CurrentTime) # RMT가 0인 프로세스 방출


            if(self.processorlist[i].countquantum == self.timequantum and len(self.ReadyQueue)>0):
                #countquantum과 timequantum이 같고 레디큐에 대기 중인 프로세스가 있고
                if self.processorlist[i].process is not None: # i번째 프로세서가 작업 중이면
                    self.ReadyQueue.append(self.processorlist[i].process) # 작업중이던 프로세스를 레디큐에 삽입
                    self.processorlist[i].process = None # 작업중이던 프로세스를 제거
                self.processorlist[i].countquantum = 0 # 해당 프로세서의 countquantum 초기화
        self.record.append(copy.deepcopy(self.ReadyQueue)) # 작업이 끝나면 레디큐 정보를 기록
