import control as con
import matplotlib.pyplot as plt
import numpy as np



s= con.tf('s')
G = (0.00000816)/(0.136*s+1)

t = np.linspace(0,10,10000)
# plt.figure("Plant-stepresponse")
# T,yout = con.step_response(G,T=t)
# plt.plot(t,yout)
# plt.grid()
# plt.xlabel('t')
# plt.ylabel('y')


G *= 1/(s*s)
print(G)
#PID-controller
k_p = 1
T_i = 0
T_d = 5
if T_i != 0:
    D = k_p*(1+1/(T_i*s)+T_d*s)
else:
    D = k_p*(1+T_d*s)

O = con.series(D,G)
print("PID and plant transfer function "); print(O)


#Lead-controller
k_lead = 100000
freq_a = 0
freq_b = 1
D_lead = k_lead*(s+freq_a)/(s+freq_b)


#Plots PID-controller+plant bodeplot and stepresponse (Not good, two poleas at 0)
plt.figure("PID-bodeplot")
mag,phase,omega = con.bode(O, dB = True)


plt.figure("PID-stepresponse")
T,yout = con.step_response(O,T=t)
plt.plot(t,yout)
plt.grid()
plt.xlabel('t')
plt.ylabel('y')


O = con.series(D_lead, G)
print("Lead and plant transfer function "); print(O)

#Plots lag-controller+plant bodeplot and stepresponse
plt.figure("Lead-bodeplot")
mag,phase,omega = con.bode(O, dB = True)

plt.figure("Lead-stepresponse")
T,yout = con.step_response(O/(1+O),T=t)
plt.plot(t,yout)
plt.grid()
plt.xlabel('t')
plt.ylabel('y')

plt.show()