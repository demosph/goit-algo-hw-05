def bound(arr, target):
    left, right = 0, len(arr) - 1
    iterations = 0

    while left <= right:
        mid = left + (right - left) // 2
        iterations += 1

        if arr[mid] == target:
            return iterations, arr[mid]
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    # Якщо не знайдено точного співпадіння, повертаємо верхню межу
    if right < 0:
        return iterations, arr[0]
    elif left >= len(arr):
        return iterations, arr[-1]
    else:
        return iterations, arr[left]

# Приклад використання:
arr = [1.1, 1.3, 2.5, 3.8, 4.6, 5.9]
result1 = bound(arr, 3.5)
result2 = bound(arr, 6.0)

print(result1)  # Виведе: (3, 3.8)
print(result2)  # Виведе: (3, 5.9)