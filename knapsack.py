import random
from simanneal import Annealer

class KnapsackData:        # 데이터 처리 클래스
    def __init__(self):
        infile = open("knapsack_data1.txt", "r")
        data = infile.read().split()
        data = [eval(x) for x in data]
        self.item_count = data[0]
        data.pop(0)
        self.max_weight = data[0]
        data.pop(0)
        self.item_data = []
        for i in range(0, len(data), 2):
            temp = [data[i], data[i + 1]]
            self.item_data.append(temp)
        infile.close()

class Knapsack(Annealer):
    def __init__(self, state):
        super().__init__(state)

    def move(self):
        pos = random.randint(0, len(self.state) - 1)
        self.state[pos] = (self.state[pos] + 1) % 2

    def energy(self):
        global best_value, best_weight

        value = 0.0
        weight = 0.0

        for i in range(len(self.state)):
            if self.state[i] == 1:
                value += knapsack.item_data[i][0]
                weight += knapsack.item_data[i][1]

        if weight > knapsack.max_weight:
            value -= (weight - knapsack.max_weight) * 10
            if value < 0:
                value = 0

        if value > best_value:
            best_value = value
            best_weight = weight

        return value

knapsack = KnapsackData()
best_value = 0.0
best_weight = 0.0

def main():
    zero_one = [0, 1]
    init_state = [random.choice(zero_one) for i in range(knapsack.item_count)]
    print(init_state)

    sa_knapsack = Knapsack(init_state)
    #sa_knapsack.Tmax = 0.5              # 최대 온도
    #sa_knapsack.Tmin = 0.001            # 최소 온도
    sa_knapsack.set_minmax("maximize")
    sa_knapsack.steps = 1000000
    sa_knapsack.updates = 10
    sa_knapsack.copy_strategy = "slice"
    #auto_schedule = sa_knapsack.auto(minutes = 2)
    #sa_knapsack.set_schedule(auto_schedule)
    state, obj = sa_knapsack.anneal()

    print(state)
    print("obj :", obj)
    print("최대값 :", best_value)
    print("무게합 :", best_weight, " 최대무게 :", knapsack.max_weight)

main()
