from state_estimator import state_estimator
import csv
import numpy as np

file = 'C:\\Users\\bosto\\Documents\\GitHub\\EIT5-B2-209-Autonomous-Drone\\test-results\\onboard-sensor-drift\\1637063677_test_flyvning.csv'

with open(file, newline='') as csvFile:
    dataReader = csv.DictReader(csvFile, delimiter=",")
    testDataHeader = dataReader.fieldnames
    testData = list(csv.reader(csvFile,delimiter=","))
    testData = np.array(testData).astype(np.float)

print(testData)