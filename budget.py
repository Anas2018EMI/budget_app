from unittest import main
from math import floor
import re


class Category:
    def __init__(self, name: str) -> None:
        self.name = name.title()
        self.ledger = []

    def check_funds(self, amount):
        sum = 0
        # [sum += record["amount"] for record in self.ledger]
        if self.ledger != []:
            for record in self.ledger:
                sum += record["amount"]

            if amount > sum:
                return False
            else:
                return True

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):

        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        else:
            return False

    def get_balance(self):
        sum = 0
        for record in self.ledger:
            sum += record["amount"]
        return sum   #

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        else:
            return False

    def __str__(self):

        output = ""
        # Formatting the title:
        half_numb_of_schar = (30-len(self.name))//2
        title = '*'*half_numb_of_schar + \
            f"{self.name}"+'*'*half_numb_of_schar+'*'*((30-len(self.name)) % 2)
        # print(title)
        output += title+'\n'
        # Formatting the records
        sum = 0
        for record in self.ledger:
            sum += record['amount']
            amount = round(record['amount'], 2)
            if not '.' in str(amount):
                amount = str(amount)+'.00'
            elif not re.search(r".*\...", str(amount)):
                amount = str(amount)+'0'
            else:
                amount = str(amount)

            if len(record['description']) >= 23:
                item = record['description'][0:23] + ' '*(7-len(amount))+amount
            else:
                item = record['description']+' ' * \
                    (23-len(record['description'])) + \
                    ' '*(7-len(amount))+amount

            # print(item)
            output += item+'\n'
        # Formatting the total
        # print(f"Total: {round(sum,2)}")
        output += f"Total: {round(sum,2)}"
        return output

####################### Plotting a bars chart  ###############


def create_spend_chart(categories: list):
    # Formatting the upper part of the graph
    output = ""
    chart_bars = []
    categories_withdrawals = []
    total_withdrawals = 0
    for category in categories:
        withdrawals = 0
        for record in category.ledger:
            if record['amount'] < 0:
                total_withdrawals += abs(record['amount'])
                withdrawals += abs(record['amount'])

        categories_withdrawals += [withdrawals]

    for category in categories:

        # expenditures_percentages = round(
        #     categories_withdrawals[categories.index(category)]/total_withdrawals, 1)*100
        expenditures_percentages = floor(
            categories_withdrawals[categories.index(category)]/total_withdrawals*10)*10

        bar = []
        # bar_chart = [char += "o" for i in range(0, 1.1, 0.1) if expenditures_ratio >= i]
        for i in range(0, 110, 10):
            if expenditures_percentages >= i:
                bar += ["o"]

        bar += ' '*(11-len(bar))
        bar.reverse()
        chart_bars += [bar]

    # print("Percentage spent by category")
    output += "Percentage spent by category"+'\n'
    y_axis = ["100|", " 90|", " 80|", " 70|", " 60|",
              " 50|", " 40|", " 30|", " 20|", " 10|", "  0|"]
    bars = []

    for i in range(0, 11):
        line = ""
        for bar in chart_bars:
            line += bar[i]+'  '

        line = ' '+line
        bars += [line]

    for i in range(0, 11):
        print(y_axis[i]+bars[i])
        output += y_axis[i]+bars[i]+'\n'

    # Printing the separation line
    print("    "+'-'*len(chart_bars)*3+'-')
    output += "    "+'-'*len(chart_bars)*3+'-'+'\n'
    # Printing the lower part of the graph (vertical names)
    bar_names = []
    max_len = 0
    for category in categories:
        bar_name = [char for char in category.name]
        if len(category.name) > max_len:
            max_len = len(category.name)

        bar_names += [bar_name]

    for bar_name in bar_names:
        if len(bar_name) < max_len:
            for i in range(max_len-len(bar_name)):
                bar_name += [' ']
    lower_part = []
    for i in range(max_len):
        line = ""
        for name in bar_names:
            line += name[i]+'  '

        line = '     '+line
        lower_part += [line]

    for line in lower_part:
        print(line)
        output += line+'\n'
    output = output[:-1]
    # print(output)
    return output


# Run unit tests automatically
# main(module='test_module', exit=False)


food = Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")
print(food.get_balance())
clothing = Category("Clothing")
food.transfer(50, clothing)
clothing.withdraw(25.55)
clothing.withdraw(100)
auto = Category("Auto")
auto.deposit(1000, "initial deposit")
auto.withdraw(15)


print(food)
print(clothing)
