from datetime import datetime as dt
import geocoder

class Account:
    """
    This class is the prototype for the subclasses
    param-self: constructs and initialize the object.
    param-filepath: is a .txt relative file path
    """
    def __init__(self,filepath):
        self.filepath = filepath
        now = dt.now()
        self.c_time = now.strftime(" on %h-%d, %Y at %H:%M:%S")

        try:   ##Try the internet connection to fetch the location of where the program is being run
            self.loc = geocoder.ip('me') #getting the physical address of the machine you're running python at.
            self.cty = self.loc.city
            self.state = self.loc.state
            self.cntry = self.loc.country
        except:
            self.cty = 'unknown'
            self.state = 'unknown'
            self.cntry = 'unknown'

        with open(filepath,'r') as file:
                self.balance = float(file.read())


    def actvty_tracker(self,filepath,act_type,am,loc,time):
        with open(filepath,'a+') as file:
            file.write("Activity type: "+str(act_type)+":: $"+str(am)+"::"+time+"::location: "+loc)
            file.write("\n-----------------------------------------------------------\n")

    def withdraw(self,amount):
        self.balance = self.balance - float(amount)
        self.actvty_tracker(filepath="statements.txt",act_type="Withdrawing",am=amount, loc=self.cty+','+self.state+','+self.cntry, time= self.c_time)

    def deposit(self,amount):
        self.balance = self.balance + float(amount)
        self.actvty_tracker(filepath="statements.txt",act_type="Deposit",am=amount, loc=self.cty+','+self.state+','+self.cntry, time=self.c_time)


    def commit(self):
        try:
            with open(self.filepath,'w') as file:
                file.write(str(self.balance))
            return True
        except:
            return False

class Checking(Account):
    """
    This class use the base class(Account) to build a checking acountself.
    param-self: constructs the checking instance methods and varible to the objectself.
    param-filepath: is a .txt relative file path
    param-fee:the deducted charge used in transfer method.
    """
    def __init__(self,filepath,fee):
        Account.__init__(self,filepath)
        self.fee = fee

    def transfer(self,amount):
        self.balance = self.balance - amount - self.fee
        self.transfer_amount = amount
        self.actvty_tracker(filepath="statements.txt",act_type="transferred from checking",am=amount,
        loc=self.cty+','+self.state+','+self.cntry, time= self.c_time)

class Saving(Account):
    """
    This class use the base class(Account) to initiantiate the saving acount.
    param-self: constructs and initialize the subclass class.
    param-filepath: is a .txt relative file path
    """
    def __init__(self,filepath):
        Account.__init__(self,filepath)
        with open(filepath,'r') as file:
            self.balance= float(file.read())
