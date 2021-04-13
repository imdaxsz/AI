import sys
import time
import msvcrt
import random
import math
from tkinter import *
import copy

def ResultScreen(solution):
    root = Tk()
    root.title("NQueens")
    x = len(solution)
    screensize = str(x*30+10) + "x" + str(x*30+10) + "+100+100"
    root.geometry(screensize)
    root.resizable(True, True)

    canvas = Canvas(root, width=200, height=150, bg="white", bd=2)
    canvas.pack(fill="both", expand=True)

    for i in range(x):
        for j in range(x):
            if (i+j)%2 == 0:
                canvas.create_rectangle(5+j*30, 5+30*i, 35+j*30, 35+i*30, fill="white")
            else:
                canvas.create_rectangle(5+j*30, 5+30*i, 35+j*30, 35+i*30, fill="lightgray")
    r=10
    i=0
    for j in solution:
        canvas.create_oval(20-r+30*(j-1), 20-r+30*i, 20+r+30*(j-1), 20+r+30*i)
        i=i+1

    root.mainloop()

def getkey(): # 단일키 입력 받기
    return msvcrt.getch()

def Validate(ary):
    for i in range(len(ary)-1):
        row1 = ary[i]
        for j in range(i+1, len(ary)):
            row2 = ary[j]
            if row1 == (row2+(j-i)):
                return False
            if row1 == (row2-(j-i)):
                return False
    return True

def ViolateCount(ary):
    count = 0
    for i in range(len(ary)-1):
        row1 = ary[i]
        for j in range(i+1, len(ary)):
            row2 = ary[j]
            if row1 == (row2+(j-i)) or row1 == (row2-(j-i)):
                count += 1
    return count

def GetExeClockTime(inital_clock):
    current_clock = time.time()
    return current_clock - inital_clock

def next_permutation(a):
    for i in reversed(range(len(a)-1)):
        if a[i] < a[i+1]:
            break
    else:
        return False
    j = next(j for j in reversed(range(i+1, len(a))) if a[i]<a[j])
    a[i], a[j] = a[j], a[i]

    a[i+1:] = reversed(a[i+1:])
    return True

def main():
    queen_count = (int)(sys.argv[1])
    print(">>>",queen_count,"-queens problem")
    search_method = (int)(sys.argv[2])
    exe_time = (int)(sys.argv[3])

    if search_method == 1:
        for i in range(5):
            ExhaustiveSearch(queen_count, exe_time)
    elif search_method == 2:
        for i in range(5):
            HillClimbingSearch(queen_count, exe_time)
    elif search_method == 3:
        for i in range(5):
            SimpleHillClimbingSearch(queen_count, exe_time)
    elif search_method == 4:
        for i in range(5):
            SimulatedAnnealing(queen_count, exe_time)
    elif search_method == 5:
        for i in range(5):
            StochasticHCSearch(queen_count, exe_time)
    elif search_method == 6:
        for i in range(5):
            RandomRestartHCSearch(queen_count, exe_time)
    print("종료 : 아무 키나 누르세요.")
    getch = getkey()
    sys.exit()

def ExhaustiveSearch(queen_count, exe_time):
    print(">>> Exhaustive Search")
    initial_clock = time.time()
    solution = []
    for i in range(queen_count):
        solution.append(i+1)

    best_obj_value = 2147483647

    while True:
        obj_value = ViolateCount(solution)
        if obj_value == 0:
            if(Validate(solution)):
                PrintResult(solution, queen_count, initial_clock)
            else:
                print("성공으로 나왔으나 결과 이상!!!")
            break
        elif obj_value < best_obj_value:
            best_obj_value = obj_value
            print(best_obj_value)
        if(GetExeClockTime(initial_clock)>exe_time):
            print("시간 초과 해 도출 실패!!!")
            break

        if next_permutation(solution) == False:
            break

def PrintResult(solution, queen_count, inital_clock):
    print("queen 개수 : ", queen_count)
    for i in range(queen_count):
        print(solution[i])
    print("수행 시간 : ", GetExeClockTime(inital_clock))
    ResultScreen(solution)

def GenInitSolutionRandom(solution, queen_count):
    for i in range(queen_count):
        solution.append(i+1)
    random.shuffle(solution)
    cur_obj_value = ViolateCount(solution)
    print("초기값 : ", cur_obj_value)

    return cur_obj_value

def GenSolutionRandom(solution, queen_count):
    for i in range(queen_count):
        solution.append(i+1)
    random.shuffle(solution)
    cur_obj_value = ViolateCount(solution)

    return cur_obj_value

def HillClimbingSearch(queen_count, exe_time):
    print(">>> Hill-Climbing Search")
    initial_clock = time.time()

    solution = []
    cur_obj_value = GenInitSolutionRandom(solution, queen_count)
    if cur_obj_value == 0:
        return
    iterate_count = 0

    while True:
        iterate_count += 1

        best_next_solutions = []
        best_next_obj_value = cur_obj_value

        for i in range(queen_count-1):
            for j in range(i+1, queen_count):
                solution[i], solution[j] = solution[j], solution[i]

                tmp_solution = copy.deepcopy(solution)

                next_obj_value = ViolateCount(tmp_solution)
                if next_obj_value == 0:
                    if (Validate(solution)):
                        print("성공")
                        print("반복 횟수 : ", iterate_count)

                        PrintResult(solution, queen_count, initial_clock)
                    else:
                        print("성공으로 나왔으나 결과 이상!!!")
                    return

                elif next_obj_value < best_next_obj_value:
                    best_next_solutions.clear()
                    best_next_solutions.append(tmp_solution)

                    best_next_obj_value = next_obj_value
                    print("[", iterate_count, "]", best_next_obj_value)

                elif next_obj_value == best_next_obj_value:
                    best_next_solutions.append(tmp_solution)

                solution[i], solution[j] = solution[j], solution[i]

        if len(best_next_solutions) > 0:
            solution = best_next_solutions[random.randrange(len(best_next_solutions))]
            cur_obj_value = best_next_obj_value
        else:
            print("실패 : 현재해와 같거나 더 좋은 해가 존재하지 않음!")
            break

        if GetExeClockTime(initial_clock) > exe_time:
            break

def SimpleHillClimbingSearch(queen_count, exe_time):
    print(">>> Simple Hill-Climbing Search")
    initial_clock = time.time()

    solution = []
    cur_obj_value = GenInitSolutionRandom(solution, queen_count)
    if cur_obj_value == 0:
        return
    iterate_count = 0

    while True:
        iterate_count += 1
        i = random.randint(0, queen_count-1)
        j = random.randint(0, queen_count-1)

        solution[i], solution[j] = solution[j], solution[i]
        tmp_solution = copy.deepcopy(solution)

        next_obj_value = ViolateCount(tmp_solution)

        if next_obj_value == 0:
            if (Validate(solution)):
                print("성공!!!")
                print("반복 횟수 : ", iterate_count)
                PrintResult(solution, queen_count, initial_clock)
                return
            else:
                print("성공으로 나왔으나 결과 이상!!!")
                return
        elif next_obj_value <= cur_obj_value:
            if next_obj_value < cur_obj_value:
                cur_obj_value = next_obj_value
                print("[",iterate_count,"]", cur_obj_value)
            else:
                solution[i], solution[j] = solution[j], solution[i]
            if GetExeClockTime(initial_clock) > exe_time:
                break

def SimulatedAnnealing(queen_count, exe_time):
    print(">>> Simulated Annealing")
    initial_clock = time.time()

    solution = []
    cur_obj_value = GenInitSolutionRandom(solution, queen_count)

    if cur_obj_value == 0:
        return

    iterate_count = 0
    T = 1.0
    alpha = 0.999

    while True:
        iterate_count += 1
        i = random.randint(0, queen_count-1)
        j = random.randint(0, queen_count-1)
        solution[i], solution[j] = solution[j], solution[i]

        next_obj_value = ViolateCount(solution)

        if next_obj_value == 0:
            if (Validate(solution)):
                print("성공!!!")
                print("반복 횟수 : ", iterate_count)
                PrintResult(solution, queen_count, initial_clock)
                break
            else:
                print("성공으로 나왔으나 결과 이상!!!")
                break
        elif next_obj_value <= cur_obj_value:
            if next_obj_value < cur_obj_value:
                cur_obj_value = next_obj_value
                print("[", iterate_count, "]", cur_obj_value)
        else:
            delta_E = next_obj_value - cur_obj_value
            move_probability = math.exp(-(delta_E/T))
            if random.random() <= move_probability:
                cur_obj_value = next_obj_value
                print("[", iterate_count, "]", cur_obj_value,",",move_probability)
            else:
                solution[i], solution[j] = solution[j], solution[i]

            T = T * alpha
            if T < 0.01:
                T = 0.01

            if GetExeClockTime(initial_clock) > exe_time:
                break

def StochasticHCSearch(queen_count, exe_time):
    print(">>> Stochastic Hill-Climbing Search")
    initial_clock = time.time()

    solution = []
    cur_obj_value = GenInitSolutionRandom(solution, queen_count)
    if cur_obj_value == 0:
        return
    iterate_count = 0

    while True:
        iterate_count += 1

        better_next_solutions = []
        better_next_obj_value = cur_obj_value
        solutions_list = []
        N = queen_count*queen_count # obj_value에 따라 해의 이동 확률을 설정하기 위한 변수

        for i in range(queen_count-1):
            for j in range(i+1, queen_count):
                solution[i], solution[j] = solution[j], solution[i]

                tmp_solution = copy.deepcopy(solution)

                next_obj_value = ViolateCount(tmp_solution)
                if next_obj_value == 0:
                    if (Validate(solution)):
                        print("성공")
                        print("반복 횟수 : ", iterate_count)

                        PrintResult(solution, queen_count, initial_clock)
                    else:
                        print("성공으로 나왔으나 결과 이상!!!")
                    return

                elif next_obj_value < better_next_obj_value:
                    better_next_solutions.append(tmp_solution)
                    better_next_obj_value = next_obj_value
                    print("[", iterate_count, "]", better_next_obj_value)
                    for k in range(N-better_next_obj_value): # 최적해에 가까울수록 여러번 삽입하여 이동될 해로 나올 확률을 높게 함
                        solutions_list.append(tmp_solution)

                elif next_obj_value == better_next_obj_value:
                    better_next_solutions.append(tmp_solution)
                    for k in range(N-better_next_obj_value): # 최적해에 가까울수록 여러번 삽입하여 이동될 해로 나올 확률을 높게 함
                        solutions_list.append(tmp_solution)

                solution[i], solution[j] = solution[j], solution[i]

        if len(better_next_solutions) > 0:
            solution = random.choice(solutions_list) # 확률에 따라 이동
            cur_obj_value = ViolateCount(solution)
        else:
            print("실패 : 현재해와 같거나 더 좋은 해가 존재하지 않음!")
            break

        if GetExeClockTime(initial_clock) > exe_time:
            break

def RandomRestartHCSearch(queen_count, exe_time):
    print(">>> Random Restart Hill-Climbing Search")
    initial_clock = time.time()

    solution = []
    cur_obj_value = GenInitSolutionRandom(solution, queen_count)
    pass_solutions = [] # 이미 수행이 완료된 해를 저장하는 리스트
    if cur_obj_value == 0:
        return
    iterate_count = 0

    while True:
        iterate_count += 1

        if iterate_count > 1: # 랜덤한 곳에서 Restart
            temp = copy.deepcopy(solution)
            pass_solutions.append(temp)
            solution.clear()  # 다음 시작 지점을 무작위로 지정한다.
            cur_obj_value = GenSolutionRandom(solution, queen_count)
            if solution in pass_solutions == True:
                solution.clear()
                cur_obj_value = GenSolutionRandom(solution, queen_count)
            print("[", iterate_count, "]", cur_obj_value)
            if cur_obj_value == 0:
                if (Validate(solution)):
                    print("성공")
                    print("반복 횟수 : ", iterate_count)
                    PrintResult(solution, queen_count, initial_clock)
                else:
                    print("성공으로 나왔으나 결과 이상!!!")
                return

        best_next_solutions = []
        best_next_obj_value = cur_obj_value

        for i in range(queen_count-1):
            for j in range(i+1, queen_count):
                solution[i], solution[j] = solution[j], solution[i]

                tmp_solution = copy.deepcopy(solution)

                next_obj_value = ViolateCount(tmp_solution)
                if next_obj_value == 0:
                    if (Validate(solution)):
                        print("성공")
                        print("반복 횟수 : ", iterate_count)

                        PrintResult(solution, queen_count, initial_clock)
                    else:
                        print("성공으로 나왔으나 결과 이상!!!")
                    return

                elif next_obj_value < best_next_obj_value:
                    best_next_solutions.clear()
                    best_next_solutions.append(tmp_solution)

                    best_next_obj_value = next_obj_value
                    print("[", iterate_count, "]", best_next_obj_value)

                elif next_obj_value == best_next_obj_value:
                    best_next_solutions.append(tmp_solution)

                solution[i], solution[j] = solution[j], solution[i]


        if GetExeClockTime(initial_clock) > exe_time:
            break

main()
