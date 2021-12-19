#!/usr/bin/env python3

def isint(s):
    try: 
        int(s) 
        return True
    except ValueError:
        return False

print (isint('10'))
print (isint ('a')) # не десятичная цифра
print (isint('²')) # верхний индекс
print (isint('১')) # Bengali (Unicode)

## 

a = 1

print("The type 'c' is : ",type(a))
b = '2'
print ("The type 'b' is :", type(b))
#c = a + b
print ("The type 'c' is :", type(c))

#Какое значение будет присвоено переменной c? в исходном варианте c не будет объявлена, т.к. при выполнении операции сложения произойдёт ошибка, python воспримет первую переменную как число, вторую как строку
#Как получить для переменной c значение 12?
#Как получить для переменной c значение 3?


a = 1
print (a)
b = '2'
print (b)
print (isint (b), b)
c = a + int(b)
print (c)


#joke
d='১'
e = int(d)+a
print (d.isdigit())

