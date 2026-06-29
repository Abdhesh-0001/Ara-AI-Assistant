def calculate_average(numbers):
    total = 0
    for num in numbers:
        total = total + num
    average = total / len(numbers)
    return average

result = calculate_average([10, 20, 30])
print(result)  # Works fine

result2 = calculate_average([])
print(result2)  # What happens?