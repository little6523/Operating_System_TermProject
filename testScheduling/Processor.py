import copy
 # 작업이 끝난 프로세스리스트
class CProcessor : # 프로세서
    def __init__(self,id,type) :
        self.id = id # 프로세서 id
        self.process = None # 작업중인 프로세스
        self.runningtime = [] # 작업시간
        self.throughput = [] # 처리량
        self.runningprocessid =[] # 단위시간당 처리된 프로세스의 id
        self.core = type # 코어 종류
        self.countquantum = 0 # RR 카운트
        finished_processlist = []
        if self.core == 'P':
            self.performance = 2 # 단위시간당 성능
            self.power_consumption = 3  # 소비전력
        elif self.core == 'E':
            self.performance = 1 # 단위시간당 성능
            self.power_consumption = 1  # 소비전력
        self.waitingpower= 1 #대기전력 0.1

    def allocateprocess(self, process): #프로세서에 프로세스 할당
        self.process = process 

    def isEmpty(self) : # 작업중인 프로세스가 있는지 검사
        if self.process is None : # 없으면 True 반환
            return True
        else : return False

    def clearprocess(self, CurrentTime) : # 남은 실행 시간이 0인 프로세스 처리
        if(self.process is not None):
            if self.process.RMT == 0 : # 남은 실행 시간이 0이면
                self.process = None
