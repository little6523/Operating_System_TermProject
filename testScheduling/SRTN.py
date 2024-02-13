from Schedule import *
import copy

class SRTN(CSchedule) :

    def swapprocess(self) : # 실행중인 프로세스와 레디큐의 프로세스를 바꾸는 함수
        RunningCount = 0 # 실행중인 프로세스의 수
        Running_processor_list = [] # 실행중인 프로세서들의 리스트

        for i in range(len(self.processorlist)) :
            if self.processorlist[i].process is not None : # 레디큐에 있는 모든 프로세스의 waitingcount 1증가
                Running_processor_list.append(copy.deepcopy(self.processorlist[i]))

        # 실행중인 프로세스 중에서 레디큐로 보낼 프로세스를 쉽게 정하기 위해 RMT기준 내림차순 정렬
        Running_processor_list = sorted(Running_processor_list, key=lambda x: -x.process.RMT)

        for i in range(len(self.processorlist)) : # 일을 하고있는 프로세서의 개수 세기
            if self.processorlist[i].process is None :
                break
            else :
                RunningCount += 1

        for i in range(len(Running_processor_list)) : # 작업 중인 모든 프로세서와 레디큐를 비교 및 스왑 실행
            if len(self.ReadyQueue) > 0 :
                if Running_processor_list[i].process.RMT > self.ReadyQueue[0].RMT :
                    self.ReadyQueue.append(self.processorlist[(Running_processor_list[i].id)-1].process)
                    self.processorlist[(Running_processor_list[i].id)-1].process = self.ReadyQueue.pop(0)
            
        self.ReadyQueue = sorted(self.ReadyQueue, key=lambda x: x.RMT) # 레디큐를 RMT순으로 정렬

        # 실행중인 프로세스들 중에서 RMT가 가장 큰 프로세스와 레디큐에서 RMT가 가장 적은 프로세스를 비교하여
        # 바꿔야 하면 서로 스왑함. 이 때, 실행중이던 프로세스는 레디큐 맨 뒤에 삽입하고 마지막에 레디큐 한 번 정렬

    def run(self) : # run함수 재정의
        # 레디큐에 프로세스가 있거나 프로세스리스트에 프로세스가 남아있으면
        while(len(self.ReadyQueue)>0 or len(self.processlist)>0 ) :
            self.ReadyQallocate() # 프로세스리스트에서 현재시간과 AT를 비교하여 레디큐에 삽입
            self.ReadyQueue = sorted(self.ReadyQueue, key=lambda x: x.RMT)
            # 레디큐를 RMT가 낮은순으로 정렬
            for i in range(len(self.processorlist)) : # 프로세서 개수만큼 반복
                if self.processorlist[i].isEmpty() and len(self.ReadyQueue)>0 :
                    self.processorlist[i].allocateprocess(self.ReadyQueue.pop(0)) # 작업중이지 않은 프로세서에 프로세스 할당
                    print(self.processorlist[i].id,"번 프로세서에 레디큐프로세스 할당함")
            self.swapprocess() # swap할 프로세스 있으면 swap함
            self.working() # 작업실행
            for i in range(len(self.ReadyQueue)):
                print('#',i,'번째 레디큐원소','AT : ',self.ReadyQueue[i].AT,'RMT : ',self.ReadyQueue[i].RMT)
            print('                   현재시간',self.CurrentTime,'초 ')
            print()
            self.CurrentTime += 1 # 작업이 끝나면 현재시간 1 증가

        for i in range(len(self.processorlist)) : # 프로세서의 개수만큼 반복
            while(self.processorlist[i].isEmpty()==False): # i번째 프로세스가 일을 하는 중이면
                self.working() # 하던 일 마저 진행
                self.CurrentTime += 1 # 작업을 하고 스케줄링이 종료되므로 종료시간은 현재 시간 + 1