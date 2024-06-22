import numpy as np
import pandas as pd 
import datetime as dt

class Alarm:
    def __init__(self, current_time, target_time):
        self.current_time= pd.to_datetime(current_time).time()
        self.current_day= pd.to_datetime(current_time).date()
        self.target_time= pd.to_datetime(target_time).time()
        self.target_day= self.target_day()
        
    
    def target_day(self):
        if self.current_time > self.target_time :
            target_day= self.current_day + pd.Timedelta(days= 1)
        else:
            target_day= self.current_day
        return target_day
    
    
    def datetime_distance(self):
        current_datetime= dt.datetime.combine(self.current_day, self.current_time)
        target_datetime= dt.datetime.combine(self.target_day, self.target_time)
        total_diff= (target_datetime - current_datetime).total_seconds()
        hour= np.floor(total_diff / (60*60))
        h2s= hour*(60*60)
        diff_1= total_diff- h2s 
        minute= np.floor(diff_1 / (60))
        m2s= minute* 60
        second= diff_1 - m2s
        
        result= pd.to_datetime("20240101000000")
        result+= pd.to_timedelta(hour, unit= 'h')
        result+= pd.to_timedelta(minute, unit= 'm')
        result+= pd.to_timedelta(second, unit= 's')
        final_result= str(result.time())
        return final_result


if __name__ == '__main__':
    alarm= Alarm(current_time= "20:29:21", target_time ="20:59:00")
    distance= alarm.datetime_distance()
    print(distance)

