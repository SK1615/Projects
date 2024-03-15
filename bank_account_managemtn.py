# Kiranganesh(201711361)
import random
import datetime

class BasicAccount:
    """shows a customer having a basic bank account"""
    Account_Counter = 0

    def __init__(self, ac_name, opening_balance):
        """initializing the account name, opening balance of basic bank account also creating card number"""
        BasicAccount.Account_Counter += 1
        self.name = ac_name
        self.ac_num = BasicAccount.Account_Counter
        self.balance = opening_balance
        self.card_num = self._generate_card_number()
        self.card_exp = self._generate_card_expiry()

    def __str__(self):
        """returning  string reperesentation of basic account holders name their account number and the balance in the account"""
        return f"Account Holder: {self.name}\nAccount Number: {self.ac_num}\nBalance: £{self.balance}"

    def deposit(self, amount):
        """ if the amount is greater than 0 then the balance amount gets incemented and new balance is shown as output else prints cannot deposit a particular amount"""
        if amount > 0:
            self.balance += amount
            print(f"Deposited £{amount}. New balance is £{self.balance}")
        else:
            print(f"Cannot deposit £{amount}")

    def withdraw(self, amount):
        """ creating a withdraw function and when condition passes it gives output as withdrawn amount and balance available else prints cannot withdraw the amount."""
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"{self.name} has withdrawn £{amount}. New balance is £{self.balance}")
        else:
            print(f"Cannot withdraw £{amount}")

    def get_available_balance(self):
        """gets the balance available amount"""
        return self.balance

    def get_balance(self):
        """gets the balance amount"""
        return self.balance

    def print_balance(self):
        """the function prints the balance amount"""
        print(f"Balance: £{self.balance}")

    def get_name(self):
        """function gets the name of account holder"""
        return self.name

    def get_ac_num(self):
        """the function gives the account holder's account number """
        return str(self.ac_num)

    def issue_new_card(self):
        """the function provides the new card number with its expiry date of the card"""
        self.card_num = self._generate_card_number()
        self.card_exp = self._generate_card_expiry()
        print(f"card number: {self.card_num}")
        print(f"card expriy date: {self.card_exp}")

    def close_account(self):
        """if the balance is greater of equal to 0 the function closes the account or the account cannot be closed it will withdraw the overdrawn amount"""
        if self.balance >= 0:
            self.withdraw(self.balance)
            return True
        else:
            print(f"Cannot close account due to the customer being overdrawn by £{abs(self.balance)}")
            return False

    def _generate_card_number(self):
        """the function will generate a 16 digit random card number"""
        return ''.join([str(random.randint(0, 9)) for _ in range(16)])

    def _generate_card_expiry(self):
        """ the function gives the card'sexpiry date , also shows card exprires in 3 years from issue date"""
        current_date = datetime.datetime.now()
        expiry_date = current_date + datetime.timedelta(days=365 * 3)
        return (expiry_date.month, expiry_date.year % 100)


class PremiumAccount(BasicAccount):
    """shows a customer having a premium bank account"""

    def __init__(self, ac_name, opening_balance, initial_overdraft):
        """the function initializes the premium bank account details like account name opening balance and overdraft limit"""
        super().__init__(ac_name, opening_balance)
        self.overdraft = True
        self.overdraft_limit = initial_overdraft

    def __str__(self):
        """ returning string representation of premium account also its overdraft limit"""
        return super().__str__() + f"\nOverdraft Limit: £{self.overdraft_limit}"

    def set_overdraft_limit(self, new_limit):
        """ the function sets a new overdraft limit  for the premium account"""
        self.overdraft_limit = new_limit

    def get_available_balance(self):
        """the function gets available balance of premium account also its overdraft limit"""
        return super().get_balance() + self.overdraft_limit

    def print_balance(self):
        """the function prints the account balance and overdraft limit of the premium account"""
        super().print_balance()
        print(f"Overdraft Limit: £{self.overdraft_limit}")

    def withdraw(self, amount):
        """it over rides the overdraft limits for withdrawals"""
        if 0 < amount <= (self.balance + self.overdraft_limit):
            self.balance -= amount
            print(f"{self.name} has withdrawn £{amount}. New balance is £{self.balance}")
        else:
            print(f"Cannot withdraw £{amount}. Insufficient funds and overdraft limit.")

    def close_account(self):
        """if the balance is greater of equal to 0 the function closes the premium account or the account cannot be closed it will withdraw the overdrawn amount"""
        total_amount = self.balance + self.overdraft_limit
        if total_amount >= 0:
            # Update the account number before withdrawing
            self.ac_num = BasicAccount.Account_Counter
            self.withdraw(self.balance)
            return True
        else:
            remaining_overdraft = abs(self.balance) if self.balance < 0 else 0
            print(f"Cannot close account due to the customer being overdrawn by £{remaining_overdraft}")
            return False

    def get_ac_num(self):
        """returns premium account number as string"""
        return str(self.ac_num)


class Main:
    """ the main class calls the basic and premium account class"""
    @staticmethod
    def main():
        """main function gives the usage of premium or basic account"""

        account_holder_name = input("Enter the account holder's name: ")
        """gets user input of account holder's name"""

        # code giving output for BasicAccount
        basic_account = BasicAccount(account_holder_name, 1000.0)
        print(basic_account)
        basic_account.deposit(float(input("enter the amount to be deposited: ",)))
        basic_account.withdraw(float(input("enter the amount to be withdrawn: ",)))
        basic_account.print_balance()
        basic_account.issue_new_card()
        print(basic_account)
        print("\n")
        overdraft_limit = 1000
        """overdraft limit for premium account is set as 1000 punds"""

        # code giving output for PremiumAccount
        premium_account = PremiumAccount(account_holder_name, 1500.0, overdraft_limit)
        print(premium_account)
        premium_account.deposit(float(input("enter the amount to be deposited in premium account: ",)))
        premium_account.withdraw(float(input("enter the amount to be withdrawn from premium account: ",)))
        premium_account.print_balance()
        print(f"Available balance in premium account: £{premium_account.get_available_balance()}")
        """check the available balance in premium account"""
        premium_account.set_overdraft_limit(overdraft_limit)
        print(premium_account)

        premium_account.close_account()

if __name__ == "__main__":
    Main.main()
