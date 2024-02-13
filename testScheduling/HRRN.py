from Schedule import *

class HRRN(CSchedule) : # HRRN 클래스

    def sortReadyQRR(self) : # RR(ResponseRatio)순으로 레디큐 정렬
        for i in range(len(self.ReadyQueue)):
            self.ReadyQueue[i].HRRN_calc_WT(self.CurrentTime) # WT 계산
            self.ReadyQueue[i].calc_ResponseRatio() # ResponseRatio 계산
            self.ReadyQueue = sorted(self.ReadyQueue, key=lambda x: -x.ResponseRatio)
            # ResponseRatio가 높은순으로 레디큐 정렬

    def run(self) : # run 재정의
        # 레디큐에 프로세스가 있거나 프로세스리스트에 프로세스가 남아있으면
        while(len(self.ReadyQueue)>0 or len(self.processlist)>0 ) :
            self.ReadyQallocate() # 프로세스리스트에서 현재시간과 AT를 비교하여 레디큐에 삽입
            self.sortReadyQRR() # RR(ResponseRatio)순으로 레디큐 정렬
            for i in range(len(self.processorlist)) : # 프로세서 개수만큼 반복
                if self.processorlist[i].isEmpty() and len(self.ReadyQueue)>0 :
                    self.processorlist[i].allocateprocess(self.ReadyQueue.pop(0)) # 작업중이지 않은 프로세서에 프로세스 할당
                    print(self.processorlist[i].id,"번 프로세서에 레디큐프로세스 할당함")

            for i in range(len(self.ReadyQueue)):
                print('#',i,'번째 레디큐원소','AT : ',self.ReadyQueue[i].AT,'RMT : ',self.ReadyQueue[i].RMT)
            self.working() # 작업실행
            print('                   현재시간',self.CurrentTime,'초 ')
            self.CurrentTime += 1 # 작업이 끝나면 현재시간 1 증가
        for i in range(len(self.processorlist)) : # 프로세서의 개수만큼 반복
            while(self.processorlist[i].isEmpty()==False): # i번째 프로세스가 일을 하는 중이면
                self.working() # 하던 일 마저 진행
                self.CurrentTime += 1 # 작업을 하고 스케줄링이 종료되므로 종료시간은 현재 시간 + 1