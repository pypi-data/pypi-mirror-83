from datetime import datetime

class long:
    def __init__(self, data):
        self.now_date = datetime.now()
        self.now = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
        self.time2 = ''
        self.dt_start = ''
        self.now2 = ''

    def seconds(self):
        self.time2 = datetime.now()
        self.now2 = self.time2.strftime("%Y-%m-%d %H:%M:%S")
        self.dt_start = datetime.strptime(self.now2, "%Y-%m-%d %H:%M:%S")
        self.time = self.dt_start - self.now
        self.time = int(self.time.total_seconds())
        return self.time

    def minutes(self):
        self.time2 = datetime.now()
        self.now2 = self.time2.strftime("%Y-%m-%d %H:%M:%S")
        self.dt_start = datetime.strptime(self.now2, "%Y-%m-%d %H:%M:%S")
        self.time = self.dt_start - self.now
        self.time = int(self.time.total_seconds() // 60)
        return self.time

    def hours(self):
        self.time2 = datetime.now()
        self.now2 = self.time2.strftime("%Y-%m-%d %H:%M:%S")
        self.dt_start = datetime.strptime(self.now2, "%Y-%m-%d %H:%M:%S")
        self.time = self.dt_start - self.now
        self.time = int(self.time.total_seconds() // 60) // 60
        return self.time

    def days(self):
        self.time2 = datetime.now()
        self.now2 = self.time2.strftime("%Y-%m-%d %H:%M:%S")
        self.dt_start = datetime.strptime(self.now2, "%Y-%m-%d %H:%M:%S")
        self.time = self.dt_start - self.now
        self.time = int((self.time.total_seconds() // 60) // 60) // 24
        return self.time

    def mounts(self):
        self.time2 = datetime.now()
        self.now2 = self.time2.strftime("%Y-%m-%d %H:%M:%S")
        self.dt_start = datetime.strptime(self.now2, "%Y-%m-%d %H:%M:%S")
        self.time = self.dt_start - self.now
        self.time = int(((self.time.total_seconds() // 60) // 60) // 24) // 30
        return self.time

    def years(self):
        self.time2 = datetime.now()
        self.now2 = self.time2.strftime("%Y-%m-%d %H:%M:%S")
        self.dt_start = datetime.strptime(self.now2, "%Y-%m-%d %H:%M:%S")
        self.time = self.dt_start - self.now
        self.time = int(((self.time.total_seconds() // 60) // 60) // 24) // 365
        return self.time

