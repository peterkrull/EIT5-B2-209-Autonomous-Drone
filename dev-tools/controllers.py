import time

class control:

    """
    Class that allows for PID control. Methods are the `proportional` gain,
    `derivative` and `integral` functions. The derivative and integral methods
    automatically calculate the time difference. The `PID` method allows
    for complete PID control, either using all of PID or parts, such as P, PI, PD
    and so on.
    """

    # Proportional gain
    class proportional:
        def __init__(self,K):
            self.K = K

        def update(self,error):
            return error*self.K

    # Derivative gain
    class derivative:
        def __init__(self,K):
            self.K = K
            import time
            self.time = time.time
            self.prev_time = self.time()

        def start(self):
            self.prev_time = self.time()
            self.prev_erro = 0

        def update(self,error):
            derivative = ((error-self.prev_erro)*self.K)/(self.time()-self.prev_time)
            self.prev_time = self.time()
            self.prev_erro = error
            return derivative
            
    # Integral gain
    class integral:
        def __init__(self,K):
            self.K = K
            import time
            self.time = time.time
            self.prev_time = self.time()
            
        def start(self):
            self.prev_time = self.time()
            self.integral = 0

        def update(self,error):
            self.integral += ((error)*self.K)*(self.time()-self.prev_time)
            self.prev_time = self.time()
            return self.integral

    # Combined P, I and/or D controller.
    class PID:

        def __init__(self,Kp = None, Ki = None,Kd = None,form = "parallel") -> object:
            """
            Complete PID controller complete PID control, with ability to use
            any combination of P, I and D and user-defined Kp, Ki and Kd constants.


            Args:
                Kp (float) : Proportional constant
                Ki (float) : Integral constant
                Kd (float) : Derivative constant
                form (str) : Output form, supports 'parallel' and 'ideal', see below

            More about 'form' output
                parallel : P + I + D
                ideal  : P * ( 1 + I + D )
            
            """
            self.form = form
            self.Kp,self.Ki,self.Kd = Kp,Ki,Kd
            if self.Kp:
                #print("Setting P gain to : {}".format(Kp))
                self.p = control.proportional(Kp)
            if self.Ki:
                #print("Setting I gain to : {}".format(Ki))
                self.i = control.integral(Ki)
            if self.Kd:
                #print("Setting D gain to : {}".format(Kd))
                self.d = control.derivative(Kd)

        def start(self):
            """
            Starts the controller (only applicable to controllers using
            `integral` or `derivative`)
            """
            if self.Ki:
                self.i.start()
            if self.Kd:
                self.d.start()

        def update(self,error):
            """
            Updates the controllers with a new error 
            and calculates the appropriate correction.

            Args:
                error (float) : error to correct

            Returns (float) : correction

            """
            P,I,D = 1,0,0
            if self.Kp:
                P = self.p.update(error)
            if self.Ki:
                I = self.i.update(error)
            if self.Kd:
                D = self.d.update(error)

            if self.form == "parallel":
                return P + I + D
            if self.form == "ideal":
                return P * ( 1 + I + D )


    class lead_lag_comp():
        """
        Discrete time lead-lag compensator of the form k*(s+a)/(s+b)

        Args:
            a (float) : Location of zero
            b (float) : Location of pole
            k (float) : Amount of gain
        """
        def __init__(self,a = 0,b = 0,k = 1):
            self.a = a
            self.b = b
            self.k = k

        def start(self):
            """
            Starts the controller
            """
            self.prev_time = time.time()
            self.prev_error = 0
            self.prev_output = 0

        def update(self,error):
            """
            Updates the controllers with a new error 
            and calculates the appropriate correction.

            Args:
                error (float) : error to correct

            Returns (float) : correction

            """
            T = time.time()-self.prev_time
            #output = (self.k/((1/T)*self.b))*(((error-self.prev_error)/T)+self.a*(error))+(1/(1+(T*self.b)))*self.prev_output
            #output = (self.k/((1/T)+self.b))*(((error-self.prev_error)/T)+(self.a*error))+(self.prev_output/(1+(T*self.b)))
            output = (self.k*(error*(1+self.a*T)-self.prev_error)+self.prev_output)/(1+self.b*T)
            self.prev_output = output
            self.prev_error = error
            return output

    def limiter(value,min,max):
        """
        Limit filter to set some `value` to equal to `min` or `max` if out of bounds
        """
        if value < min:
            return min
        elif value > max:
            return max
        else:
            return value