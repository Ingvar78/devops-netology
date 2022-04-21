# Домашнее задание к занятию "7.5. Основы golang"

С `golang` в рамках курса, мы будем работать не много, поэтому можно использовать любой IDE. 
Но рекомендуем ознакомиться с [GoLand](https://www.jetbrains.com/ru-ru/go/).  

## Задача 1. Установите golang.
1. Воспользуйтесь инструкций с официального сайта: [https://golang.org/](https://golang.org/).
2. Так же для тестирования кода можно использовать песочницу: [https://play.golang.org/](https://play.golang.org/).

## Задача 2. Знакомство с gotour.
У Golang есть обучающая интерактивная консоль [https://tour.golang.org/](https://tour.golang.org/). 
Рекомендуется изучить максимальное количество примеров. В консоли уже написан необходимый код, 
осталось только с ним ознакомиться и поэкспериментировать как написано в инструкции в левой части экрана.  

## Задача 3. Написание кода. 
Цель этого задания закрепить знания о базовом синтаксисе языка. Можно использовать редактор кода 
на своем компьютере, либо использовать песочницу: [https://play.golang.org/](https://play.golang.org/).

1. Напишите программу для перевода метров в футы (1 фут = 0.3048 метр). Можно запросить исходные данные 
у пользователя, а можно статически задать в коде.
    Для взаимодействия с пользователем можно использовать функцию `Scanf`:
    ```
    package main
    
    import "fmt"
    
    func main() {
        fmt.Print("Enter a number: ")
        var input float64
        fmt.Scanf("%f", &input)
    
        output := input * 2
    
        fmt.Println(output)    
    }
    ```

```bash
iva@c9:~/go-project/hello $ go run .
Enter a number of meters: 5
5 meters is equal to 16.404199475065617 feet
iva@c9:~/go-project/hello $ go run .
Enter a number of meters: 6
6 meters is equal to 19.68503937007874 feet
iva@c9:~/go-project/hello $ cat hello.go 
package main

import ("fmt"
)

func main() {
    fmt.Print("Enter a number of meters: ")
    var input float64
    fmt.Scanf("%f", &input)

    output := input / 0.3048

    fmt.Println(input, "meters is equal to", output ,"feet")

}
```


1. Напишите программу, которая найдет наименьший элемент в любом заданном списке, например:
    ```
    x := []int{48,96,86,68,57,82,63,70,37,34,83,27,19,97,9,17,}
    ```

```bash
iva@c9:~/go-project/example $ go run .
Source array:  [48 96 86 68 57 82 63 70 37 34 83 27 19 97 9 17]
Min value:  9
____________________
Min value:  9
Max value:  97
iva@c9:~/go-project/example $ cat tets.go 
package main

import "fmt"

func main() {
    x := []int{48,96,86,68,57,82,63,70,37,34,83,27,19,97,9,17}
    min := x[0]
    fmt.Println("Source array: ", x)
    for _, value := range x[1:] {
    if value < min {
        min = value
    }

    }
    fmt.Println("Min value: ", min)
    fmt.Println("____________________")

    min, max := findMinAndMax(x)
    fmt.Println("Min value: ", min)
    fmt.Println("Max value: ", max)

}

func findMinAndMax(array []int) (int, int) {
    var max int = array[0]
    var min int = array[0]
    for _, value := range array {
        if max < value {
            max = value
        }
        if min > value {
            min = value
        }
    }
    return min, max
}

```


1. Напишите программу, которая выводит числа от 1 до 100, которые делятся на 3. То есть `(3, 6, 9, …)`.

В виде решения ссылку на код или сам код. 

```bash
iva@c9:~/go-project/example $ cat tets.go 
package main

import (
  "fmt"
)

func main(){
  fmt.Println("To return the remainder then assign the value: %")
  fmt.Println(div())

}
func div() []int {
    var numbers []int
    for i := 1; i <= 100; i++ {
    if i%3 == 0 {
        numbers = append(numbers, i)
//        fmt.Println(i, i%3, i/3)

}
}
    return numbers
}

iva@c9:~/go-project/example $ go run .
To return the remainder then assign the value: %
[3 6 9 12 15 18 21 24 27 30 33 36 39 42 45 48 51 54 57 60 63 66 69 72 75 78 81 84 87 90 93 96 99]

```

## Задача 4. Протестировать код (не обязательно).

Создайте тесты для функций из предыдущего задания. 

---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---

