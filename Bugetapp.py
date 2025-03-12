class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        balance = 0
        for item in self.ledger:
            balance += item["amount"]
        return balance

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def __str__(self):
        title = self.name.center(30, "*")
        items = ""
        for item in self.ledger:
            description = item["description"][:23].ljust(23)
            amount = "{:.2f}".format(item["amount"]).rjust(7)
            items += f"{description}{amount}\n"
        total = f"Total: {self.get_balance():.2f}"
        return f"{title}\n{items}{total}"


def create_spend_chart(categories):
    total_withdrawals = 0
    category_withdrawals = []

    for category in categories:
        withdrawals = 0
        for item in category.ledger:
            if item["amount"] < 0:
                withdrawals += abs(item["amount"])
        total_withdrawals += withdrawals
        category_withdrawals.append(withdrawals)

    percentages = []
    for withdrawal in category_withdrawals:
        if total_withdrawals == 0:
            percentages.append(0)
        else:
            percentages.append(int((withdrawal / total_withdrawals) * 100))

    chart = "Percentage spent by category\n"
    for i in range(100, -10, -10):
        chart += str(i).rjust(3) + "| "
        for percentage in percentages:
            if percentage >= i:
                chart += "o  "
            else:
                chart += "   "
        chart += "\n"

    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"

    category_names = [category.name for category in categories]
    max_length = max(len(name) for name in category_names)

    for i in range(max_length):
        chart += "     "
        for name in category_names:
            if i < len(name):
                chart += name[i] + "  "
            else:
                chart += "   "
        if i < max_length -1:
          chart+="\n"

    return chart
