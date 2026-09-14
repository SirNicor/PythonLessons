
import math
import random

def main():
    while(True):
        numberScores = []
        print("Проверка на случайных данных - 1, ввод собственных данных - 2")
        change = checkTryCatch()
        if change == 1:
            numberStudents = random.randint(0, 100)
            input(f"Количества студентов: {numberStudents}")
            for i in range(0, numberStudents):
                randomNumber = random.randint(0, 101)
                numberScores.append(randomNumber)
                print(f"Баллы студента {i+1} - {randomNumber}")
        else:
            numberStudents = int(input("Введите количество студентов: "))
            print("""Вводите далее данные студентов через enter.
            Ограничения: положительно целое число в диапозоне от 0 до 100, где 0 - не сдал.""")
            for i in range(0, numberStudents):
                while(True):
                    try:
                        inputNumber = int(input(f"Введите баллы студента {i+1}:"))
                        if not(isinstance(inputNumber, int)):
                            raise TypeError
                        if not(inputNumber in range(0, 101)):
                            raise IndexError
                    except (TypeError, ValueError):
                        print(f"Вы ввели не тот тип данных")
                    except IndexError:
                        print(f"Не входит в диапозон от 0 до 100")
                    else:
                        break
                numberScores.append(inputNumber)
        average = avg(numberScores)
        maxResult = max(numberScores) 
        minResult = min(numberScores)
        countPassed = checkCountPassed(numberScores)
        percentPassed = countPassed/len(numberScores)*100
        countAboveAverageResult = checkCountAboveAverageResult(numberScores)
        input(f"""Average scores: {average}, 
        max: {maxResult}, 
        min: {minResult},
        count of passed: {countPassed}, 
        percent of passed: {percentPassed}, 
        count above average result: {countAboveAverageResult}""")
        print("Если вы хотите повторить программу введите 1, иначе 2")
        change = checkTryCatch()
        if change == 2: break


def avg(numberScores):
    return sum(numberScores)/len(numberScores)
    
def checkCountPassed(numberScores):
    count = 0
    for i in numberScores:
        if i != 0:
            count += 1
    return count

def checkCountAboveAverageResult(numberScores):
    average = avg(numberScores)
    count = 0
    for i in numberScores:
        if i>average:
            count+=1
    return count

def checkTryCatch():
    while(True):
        try:
            change = int(input())
            if not(isinstance(change, int)):
                raise TypeError
            if not(change in range(0, 101)):
                    raise IndexError
        except (TypeError, ValueError):
            print(f"Вы ввели не тот тип данных")
        except IndexError:
            print(f"Не 1 и не 2")
        else:
            break
    return change

if __name__ == "__main__":
    main()
