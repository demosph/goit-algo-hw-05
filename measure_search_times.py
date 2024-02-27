import timeit
import urllib.request

# Алгоритм Кнута-Моріса-Прата
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено

# Алгоритм Боєра-Мура
def build_shift_table(pattern):
    """Створити таблицю зсувів для алгоритму Боєра-Мура."""
    table = {}
    length = len(pattern)
    # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
    # Створюємо таблицю зсувів для патерну (підрядка)
    shift_table = build_shift_table(pattern)
    i = 0  # Ініціалізуємо початковий індекс для основного тексту

    # Проходимо по основному тексту, порівнюючи з підрядком
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1  # Починаємо з кінця підрядка

        # Порівнюємо символи від кінця підрядка до його початку
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1  # Зсуваємось до початку підрядка

        # Якщо весь підрядок збігається, повертаємо його позицію в тексті
        if j < 0:
            return i  # Підрядок знайдено

        # Зсуваємо індекс i на основі таблиці зсувів
        # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # Якщо підрядок не знайдено, повертаємо -1
    return -1

#  Алгоритм Рабіна-Карпа
def polynomial_hash(s, base=256, modulus=101):
    """
    Повертає поліноміальний хеш рядка s.
    """
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def rabin_karp_search(main_string, substring):
    # Довжини основного рядка та підрядка пошуку
    substring_length = len(substring)
    main_string_length = len(main_string)

    # Базове число для хешування та модуль
    base = 256
    modulus = 101

    # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)

    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(base, substring_length - 1) % modulus

    # Проходимо крізь основний рядок
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1

# Завантаження текстового файлу за URL
def load_text_from_url(url):
    with urllib.request.urlopen(url) as f:
        return f.read().decode('utf-8')

# Вимірювання часу виконання алгоритму для підрядка
def measure_algorithm_time(algorithm_function, text, pattern):
    start_time = timeit.default_timer()
    algorithm_function(text, pattern)
    end_time = timeit.default_timer()
    return end_time - start_time

# Вимірюємо час для різних алгоритмів пошуку
def measure_search_times(text_url, existing_pattern, fake_pattern):
    text = load_text_from_url(text_url)

    # Виконуємо вимірювання часу для кожного алгоритму пошуку
    time_kmp_existing = measure_algorithm_time(kmp_search, text, existing_pattern)
    time_kmp_fake = measure_algorithm_time(kmp_search, text, fake_pattern)
    time_bm_existing = measure_algorithm_time(boyer_moore_search, text, existing_pattern)
    time_bm_fake = measure_algorithm_time(boyer_moore_search, text, fake_pattern)
    time_rk_existing = measure_algorithm_time(rabin_karp_search, text, existing_pattern)
    time_rk_fake = measure_algorithm_time(rabin_karp_search, text, fake_pattern)

    # Виводимо результати
    print(f"KMP Search - Existing: {time_kmp_existing} seconds")
    print(f"KMP Search - Fake: {time_kmp_fake} seconds")
    print(f"Boyer-Moore Search - Existing: {time_bm_existing} seconds")
    print(f"Boyer-Moore Search - Fake: {time_bm_fake} seconds")
    print(f"Rabin-Karp Search - Existing: {time_rk_existing} seconds")
    print(f"Rabin-Karp Search - Fake: {time_rk_fake} seconds")
    print("\n")

text1_url = "https://drive.google.com/file/d/18_R5vEQ3eDuy2VdV3K5Lu-R-B-adxXZh/view?usp=sharing"
text2_url = "https://drive.google.com/file/d/13hSt4JkJc11nckZZz2yoFHYL89a4XkMZ/view?usp=sharing"

existing_pattern_1 = 'жадібні алгоритми'
fake_pattern_1 = 'серіалізація'
existing_pattern_2 = 'швидкість роботи'
fake_pattern_2 = 'террабайт'

measure_search_times(text1_url, existing_pattern_1, fake_pattern_1)
measure_search_times(text2_url, existing_pattern_2, fake_pattern_2)
