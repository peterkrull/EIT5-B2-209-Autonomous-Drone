import csv
import time

class logger:
    def __init__(self):
        self.start_time = time.time()
        self.data = []

    def log_data(self,data):
        self.data.append(data)

    def save_file(self,file_name = "data_exported"):
        with open(str(int(self.start_time))+"_"+file_name+".csv",'w',newline='',encoding='UTF8') as file:
            writer = csv.writer(file)
            writer.writerows(self.data)