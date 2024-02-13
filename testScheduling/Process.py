class CProcess : #프로세스
    def __init__(self,id,AT,BT,PRIORITY = 1) : # 생성자
        self.id = id # 프로세스 id
        self.AT = AT # 도착 시간
        self.BT = BT # 실행 시간
        self.RMT = BT # 남은 실행 시간
        self.WT = 0 # 기다린 시간
        self.HRRN_WT = 0 # HRRN WT
        self.TT = 0 # 반환 시간
        self.ResponseRatio = 0 # HRRN ResponseRatio
        self.PRIORITY = PRIORITY # 1~6의 값을 가짐 => 1:실시간 2:높음 3:높은 우선 순위 4: 보통 5:낮은우선순위 6:낮음
        self.PriorityRatio = 1
        self.waitingcount = 0 # APN 기다린 시간 카운트
        self.NTT = 0; # 정규화된 반환 시간
        self.finishtime = 0; # 프로세스가 끝난 시간

    def calc_WT(self) :
        self.WT = self.TT - self.BT

    def HRRN_calc_WT(self, CurrentTime) : # HRRN WT계산
        self.HRRN_WT = CurrentTime  - self.AT

    def calc_ResponseRatio(self) : # HRRN ResponseRatio계산
        self.ResponseRatio = (self.HRRN_WT + self.BT)/ self.BT
