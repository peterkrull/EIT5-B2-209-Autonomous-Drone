import time
import random

prev_time = time.time()

prev_error0 = 0
prev_output0 = 0

prev_error1 = 0
prev_output1 = 0

prev_error2 = 0
prev_output2 = 0

a = 0.1
b = 1
k = 10

def update0(error):
    global prev_time,prev_error0,prev_output0,a,b,k
    T = time.time()-prev_time
    output = (k/((1/T)+b))*(((error-prev_error0)/T)+a*(error))+(1/(1+(T*b)))*prev_output0
    prev_output0 = output
    prev_error0 = error
    return output

def update1(error):
    global prev_time,prev_error1,prev_output1,a,b,k
    T = time.time()-prev_time
    output = (k/((1/T)+b))*(((error-prev_error1)/T)+(a*error))+(prev_output1/(1+(T*b)))
    prev_output1 = output
    prev_error1 = error
    return output

def update2(error):
    global prev_time,prev_error2,prev_output2,a,b,k
    T = time.time()-prev_time
    output = (k*(error*(1+a*T)-prev_error2)+prev_output2)/(1+b*T)
    prev_output2 = output
    prev_error2 = error
    return output

for i in range(10):
    err = random.randrange(0,1000)
    E0 = update0(err)
    E1 = update1(err)
    E2 = update2(err)
    print(f"Errors : E0 <> {round(E0,4)} : E1 <> {round(E1,4)} : E2 <> {round(E2,4)}")
    time.sleep(random.randrange(0,1000)/1000)
