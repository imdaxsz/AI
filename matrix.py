import numpy as numpy
import random

while(1):
    x, y = input("첫 번재 행렬의 행, 열 개수 입력 : ").split(',')
    u, v = input("두 번재 행렬의 행, 열 개수 입력 : ").split(',')
    x = int(x)
    y = int(y)
    u = int(u)
    v = int(v)

    a = []
    b = []

    for i in range(x):
        list = []
        for i in range(y):
            list.append(random.randint(1,10))
        a.append(list)

    mat1 = numpy.array(a)

    for i in range(u):
        list = []
        for i in range(v):
            list.append(random.randint(1,10))
        b.append(list)

    mat2 = numpy.array(b)

    print("<첫번째 행렬>")
    print(mat1)
    print("<두번째 행렬>")
    print(mat2)

    if x==u and y==v:
        print("<+ 연산 결과>")
        print(mat1+mat2)
    elif (x==1 and y==v) or (y==1 and x==u) or (u==1 and y==v) or (v==1 and x==u):
        print("<+ 연산 결과>")
        print(mat1+mat2)
    else:
        print("+ 연산이 불가능합니다")
        
    if y==u:
        print("<행렬곱 연산 결과>")
        print(numpy.dot(mat1, mat2))
    else:
        print("행렬곱 연산이 불가능합니다.")

    if input("계속할까요? (예/아니오) : ") == "아니오":
        break


        
