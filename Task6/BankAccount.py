class BankAccount:
    def __init__(self,account_no,balance=0.0):
        self.account_no=account_no
        self.balance=balance

    def deposit(self,amount):
        if amount>0:
          self.balance+=amount
          print(f"Balance after deposit is ${self.balance}")

    def withdraw(self,amount):
        if(amount<=self.balance):
          self.balance-=amount
          print(f"Balance after withdraw is ${self.balance}")

    def balanceInquiry(self):
        return self.balance

class SavingsAccount(BankAccount):
    def __init__(self,account_no,balance=0.0,interest_rate=0.2):
        super().__init__(account_no,balance)
        self.interest_rate=interest_rate

    def calculateInterest(self):
        total_interest=self.interest_rate *self.balance
        self.balance+=total_interest
        print(f"Interest calculated is ${total_interest} updated balance is ${self.balance}")


class DepositAccount(BankAccount):
    def __init__(self, account_no, balance=0.0, interest_rate=0.3):
        super().__init__(account_no, balance)
        self.interest_rate = interest_rate

    def calculateInterest(self):
        total_interest = self.interest_rate * self.balance
        self.balance += total_interest
        print(f"Interest calculated is ${total_interest} updated balance is ${self.balance}")


s1=SavingsAccount("101",10000)
s1.deposit(130000)
s1.calculateInterest()
print(BankAccount.balanceInquiry(s1))