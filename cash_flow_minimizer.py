class Bank:
    def __init__(self, name, net_amount=0):
        self.name = name
        self.net_amount = net_amount
        self.types = set()

def get_min_index(banks):
    min_val = float('inf')
    min_index = -1
    for i, bank in enumerate(banks):
        if bank.net_amount == 0:
            continue
        if bank.net_amount < min_val:
            min_index = i
            min_val = bank.net_amount
    return min_index

def get_simple_max_index(banks):
    max_val = float('-inf')
    max_index = -1
    for i, bank in enumerate(banks):
        if bank.net_amount == 0:
            continue
        if bank.net_amount > max_val:
            max_index = i
            max_val = bank.net_amount
    return max_index

def get_max_index(banks, min_index, max_num_types):
    max_val = float('-inf')
    max_index = -1
    matching_type = None

    for i, bank in enumerate(banks):
        if bank.net_amount == 0 or bank.net_amount < 0:
            continue

        intersection = list(banks[min_index].types.intersection(bank.types))

        if intersection and max_val < bank.net_amount:
            max_val = bank.net_amount
            max_index = i
            matching_type = intersection[0]
    
    return max_index, matching_type

def print_ans(ans_graph, banks):
    print("\nThe transactions for minimum cash flow are as follows:\n")
    for i in range(len(banks)):
        for j in range(len(banks)):
            if i == j:
                continue
            
            if ans_graph[i][j][0] != 0 and ans_graph[j][i][0] != 0:
                if ans_graph[i][j][0] == ans_graph[j][i][0]:
                    ans_graph[i][j] = (0, "")
                    ans_graph[j][i] = (0, "")
                elif ans_graph[i][j][0] > ans_graph[j][i][0]:
                    ans_graph[i][j] = (ans_graph[i][j][0] - ans_graph[j][i][0], ans_graph[i][j][1])
                    ans_graph[j][i] = (0, "")
                    print(f"{banks[i].name} pays Rs {ans_graph[i][j][0]} to {banks[j].name} via {ans_graph[i][j][1]}")
                else:
                    ans_graph[j][i] = (ans_graph[j][i][0] - ans_graph[i][j][0], ans_graph[j][i][1])
                    ans_graph[i][j] = (0, "")
                    print(f"{banks[j].name} pays Rs {ans_graph[j][i][0]} to {banks[i].name} via {ans_graph[j][i][1]}")
            elif ans_graph[i][j][0] != 0:
                print(f"{banks[i].name} pays Rs {ans_graph[i][j][0]} to {banks[j].name} via {ans_graph[i][j][1]}")
            elif ans_graph[j][i][0] != 0:
                print(f"{banks[j].name} pays Rs {ans_graph[j][i][0]} to {banks[i].name} via {ans_graph[j][i][1]}")
            
            ans_graph[i][j] = (0, "")
            ans_graph[j][i] = (0, "")

def minimize_cash_flow(num_banks, banks, index_of, num_transactions, graph, max_num_types):
    list_of_net_amounts = banks[:]
    ans_graph = [[(0, "") for _ in range(num_banks)] for _ in range(num_banks)]

    num_zero_net_amounts = sum(bank.net_amount == 0 for bank in list_of_net_amounts)

    while num_zero_net_amounts != num_banks:
        min_index = get_min_index(list_of_net_amounts)
        max_index, matching_type = get_max_index(list_of_net_amounts, min_index, max_num_types)

        if max_index == -1:
            simple_max_index = get_simple_max_index(list_of_net_amounts)
            ans_graph[min_index][simple_max_index] = (abs(list_of_net_amounts[min_index].net_amount), next(iter(list_of_net_amounts[min_index].types)))
            ans_graph[simple_max_index][min_index] = (abs(list_of_net_amounts[min_index].net_amount), next(iter(list_of_net_amounts[simple_max_index].types)))

            list_of_net_amounts[simple_max_index].net_amount += list_of_net_amounts[min_index].net_amount
            list_of_net_amounts[min_index].net_amount = 0

            if list_of_net_amounts[min_index].net_amount == 0:
                num_zero_net_amounts += 1
            if list_of_net_amounts[simple_max_index].net_amount == 0:
                num_zero_net_amounts += 1
        else:
            transaction_amount = min(abs(list_of_net_amounts[min_index].net_amount), list_of_net_amounts[max_index].net_amount)
            ans_graph[min_index][max_index] = (transaction_amount, matching_type)
            list_of_net_amounts[min_index].net_amount += transaction_amount
            list_of_net_amounts[max_index].net_amount -= transaction_amount

            if list_of_net_amounts[min_index].net_amount == 0:
                num_zero_net_amounts += 1
            if list_of_net_amounts[max_index].net_amount == 0:
                num_zero_net_amounts += 1

    print_ans(ans_graph, banks)

def main():
    print("\n********************* Welcome to CASH FLOW MINIMIZER SYSTEM ***********************\n\n")
    print("This system minimizes the number of transactions among multiple banks in different corners of the world that use different modes of payment. There is one world bank (with all payment modes) to act as an intermediary between banks that have no common mode of payment.\n")
    
    num_banks = int(input("Enter the number of banks participating in the transactions: "))
    
    banks = []
    index_of = {}
    
    max_num_types = 0
    for i in range(num_banks):
        if i == 0:
            print("World Bank: ", end="")
        else:
            print(f"Bank {i}: ", end="")
        
        name, num_types, *types = input().split()
        bank = Bank(name)
        bank.types = set(types)
        index_of[name] = i

        if i == 0:
            max_num_types = len(bank.types)
        
        banks.append(bank)
    
    num_transactions = int(input("Enter number of transactions: "))
    graph = [[0] * num_banks for _ in range(num_banks)]

    for i in range(num_transactions):
        s1, s2, amount = input(f"Enter transaction {i + 1} (Debtor Bank, Creditor Bank, Amount): ").split()
        graph[index_of[s1]][index_of[s2]] = int(amount)
    
    minimize_cash_flow(num_banks, banks, index_of, num_transactions, graph, max_num_types)

if __name__ == "__main__":
    main()
