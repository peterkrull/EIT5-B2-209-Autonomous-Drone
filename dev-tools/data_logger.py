import csv
import time

class logger:
    def __init__(self,file_name):
        self.file_name = file_name
        self.start_time = time.time()
        self.data = []

    def log_data(self,data):
        self.data.append(data)

    def save_file(self):
        with open(str(int(self.start_time))+"_"+self.file_name+".csv",'w',newline='',encoding='UTF8') as file:
            writer = csv.writer(file)
            writer.writerows(self.data)