from functools import wraps
from typing import Dict, Any, Callable, List 

##############################################################################
# Easy
##############################################################################

## 1. Счетчик вызова функции. Реализовал в нескольких вариантах:

### Простой счетчик, реализованный через объявление глобальной переменной,
### увеличение которого происходит при выполнении функции. Отображение
### количества вызовов сделал в отдельной строке. Особую важность при такой
### реализации приобретает ключевое слово global, которое позволяет изменять
### переменную, объявленную вне функции. Без его использования мы бы получили
### UnboundLocalError: интерпретатор воспринял бы это как попытку изменить
### переменную, которая не объявлена в области видимости функции.

custom_sum1_counter = 0

def custom_sum_1(*args: int | float, **kwargs: Dict[Any, int | float]) -> int | float:
    global custom_sum1_counter
    custom_sum1_counter += 1
    if all(map(lambda x: type(x) in (int, float), (*args, *kwargs.values()))): 
        return sum((*args, *kwargs.values()))
    else:
        raise TypeError('В функцию необходимо передать целое или вещественное число.')
    
[print(custom_sum_1(1, 2, 3, 4, 5, 6)) for _ in range(10)]
print(f'\nФункция {custom_sum_1.__name__} была выполнена {custom_sum1_counter} раз(а).\n')


### Реализация счетчика через присвоение атрибута функции и его увеличение при
### выполнении функции. Строка с количеством вызовов функции также возвращается
### вместе с основным результатом ее работ в виде кортежа.

def custom_sum_2(*args: int | float, **kwargs: Dict[Any, int | float]) -> int | float:
    custom_sum_2.counter += 1
    if all(map(lambda x: type(x) in (int, float), (*args, *kwargs.values()))): 
        return (sum((*args, *kwargs.values())),
        f'\nФункция {custom_sum_2.__name__} была вызвана {custom_sum_2.counter} раз(а).\n')
    else:
        raise TypeError('В функцию необходимо передать целое или вещественное число.')

custom_sum_2.counter = 0

[print(custom_sum_2(1, 2, 3, 4, 5, 6)) for _ in range(10)]


### Реализация счетчика через декоратор. Здесь механизм работы схож с объявлением
### атрибута функции. В данном случае атрибут функции wrapper объявляется внутри
### функции counter, и уже внутри wrapper происходит увеличение счетчика.
### декоратор выгодно отличается тем, что его можно применить к любой другой 
### функции не изменяя код этой функции. 
def counter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.counter += 1
        res = func(*args, **kwargs)
        print(f'\nФункция {func.__name__} была запущена {wrapper.counter} раз(а).\n')
        return res
    wrapper.counter = 0
    return wrapper

@counter
def custom_sum_3(*args: int | float, **kwargs: Dict[Any, int | float]) -> int | float:
    if all(map(lambda x: type(x) in (int, float), (*args, *kwargs.values()))): 
        return sum((*args, *kwargs.values()))
    else:
        raise TypeError('В функцию необходимо передать целое или вещественное число.')    

[print(custom_sum_3(1, 2, 3, 4, 6, 7, 8, 9, 10)) for _ in range(10)]

##############################################################################
# Medium
##############################################################################

# 1. Объявлены 4 простые функции


def greet(name: str) -> str:
    """Приветствует пользователя по имени, возвращает строку."""

    return f'Здравствуйте, {name}!'


def check_even(coll: List[int]) -> bool:
    """Проверяет являются ли все числа в списке четными, возвращает bool."""
    res = all(map(lambda x: not x % 2, coll))
    return res


def invert_numbers(seq: List[int | float]) -> List[int | float]:
    """Меняет знак чисел в списке на противоположный: минус на плюс и наоборот.
    Возвращает список."""
    return list(map(lambda x: abs(x) if x < 0 else -x, seq))


def is_palindrome(s: str) -> bool:
    """Проверяет является ли строка палиндромом, рекурсивная. Возвращает bool."""
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return is_palindrome(s[1:-1])

# 1.1. Для каждой из функций применяются способы подсчета количества их вызовов,
# по аналогии с задачей 1 из Easy

##############################################################################
# 1.1.1. Первая функция
# Через глобальную переменную
GREET_COUNTER = 0


def greet_gl_cnt(name: str) -> str:
    """Приветствует пользователя по имени, возвращает строку."""
    global GREET_COUNTER
    GREET_COUNTER += 1
    return f'Здравствуйте, {name}!'


names = ['Анна', 'Владимир', 'Антон', 'Валерий', 'Анастасия', 'Василий',
         'Алексей', 'Вениамин', 'Алла', 'Варвара']
[print(greet_gl_cnt(names[i])) for i in range(0, 10)]

print(
    f'\nФункция {greet_gl_cnt.__name__} была вызвана {GREET_COUNTER} раз(а).\n')

# Через атрибут функции


def greet_attr_cnt(name: str) -> str:
    """Приветствует пользователя по имени, возвращает строку."""
    greet.counter += 1
    return f'Здравствуйте, {name}!'


greet.counter = 0

[print(greet_attr_cnt(names[i])) for i in range(0, 10)]
print(
    f'\nФункция {greet_attr_cnt.__name__} была вызвана {greet.counter} раз(а).\n')

# Через декоратор

def greet_deco(name: str) -> str:
    """Приветствует пользователя по имени, возвращает строку."""

    return f'Здравствуйте, {name}!'


greet_deco = counter(greet_deco)

[print(greet_deco(names[i])) for i in range(0, 10)]

##############################################################################
# 1.1.2. Вторая функция

## Через глобальную переменную

CHECK_EVEN_COUNTER = 0


def check_even_gl_cnt(coll: List[int]) -> bool:
    """Проверяет являются ли все числа в списке четными, возвращает bool."""
    global CHECK_EVEN_COUNTER
    res = all(map(lambda x: not x % 2, coll))
    CHECK_EVEN_COUNTER += 1
    return res


check_seq = [[2, 2, 2, 2, 2, 2], [i for i in range(100)], [1, 1, 1, 1, 1, 1],\
             [i for i in range(0, 101, 2)]]

[print(check_even_gl_cnt(check_seq[i])) for i in range(0, 4)]

print(f'''\nФункция {check_even_gl_cnt.__name__} была вызвана 
    {CHECK_EVEN_COUNTER} раз(а).\n''')

## Через атрибут

def check_even_attr_cnt(coll: List[int]) -> bool:
    """Проверяет являются ли все числа в списке четными, возвращает bool."""
    res = all(map(lambda x: not x % 2, coll))
    check_even_attr_cnt.counter += 1
    return res

check_even_attr_cnt.counter = 0

[print(check_even_attr_cnt(check_seq[i])) for i in range(0, 4)]

print(f'''\nФункция {check_even_attr_cnt.__name__} была вызвана
 {check_even_attr_cnt.counter} раз(а).\n''')

## Через декоратор 

def check_even_deco(coll: List[int]) -> bool:
    """Проверяет являются ли все числа в списке четными, возвращает bool."""
    res = all(map(lambda x: not x % 2, coll))
    return res

check_even_deco = counter(check_even_deco)

[print(check_even_deco(check_seq[i])) for i in range(0, 4)]

##############################################################################
# 1.1.3. Третья функция

## Через глобальную переменную
INVERT_NUMBERS_CNT = 0

def invert_numbers_gl_cnt(seq: List[int | float]) -> List[int | float]:
    """Меняет знак чисел в списке на противоположный: минус на плюс и наоборот.
    Возвращает список."""
    global INVERT_NUMBERS_CNT
    INVERT_NUMBERS_CNT += 1
    return list(map(lambda x: abs(x) if x < 0 else -x, seq))

invert_seq = [-1, 2, 3, -5, 3.6, -9, 32, 78, -214, 233]

print(invert_numbers_gl_cnt(invert_seq))
print(f'''Функция {invert_numbers_gl_cnt.__name__} была вызвана
    {INVERT_NUMBERS_CNT} раз(а).''')

## Через атрибут функции

def invert_numbers_attr_cnt(seq: List[int | float]) -> List[int | float]:
    """Меняет знак чисел в списке на противоположный: минус на плюс и наоборот.
    Возвращает список."""
    invert_numbers_attr_cnt.counter += 1
    return list(map(lambda x: abs(x) if x < 0 else -x, seq))

invert_numbers_attr_cnt.counter = 0

print(invert_numbers_attr_cnt(invert_seq))
print(f'Функция {invert_numbers_attr_cnt.__name__} была вызвана \
    {invert_numbers_attr_cnt.counter} раз(а).')

## Через декоратор 

def invert_numbers_deco(seq: List[int | float]) -> List[int | float]:
    """Меняет знак чисел в списке на противоположный: минус на плюс и наоборот.
    Возвращает список."""
    return list(map(lambda x: abs(x) if x < 0 else -x, seq))

invert_numbers_deco = counter(invert_numbers_deco)

print(invert_numbers_deco(invert_seq))

##############################################################################
# 1.1.4. Четвертая функция
# Четвертая функция рекурсивная. Решил, что нужно использовать рекурсивную функцию
# для разонообразия.)) И только в процессе внедрения счетчиков понял, что поведение
# такой функции может отличаться, в зависимости от того, в какой строке внутри
# функции производитcя инкрементирование счетчика. Такое поведение наблюдается 
# при использовании любого из варинатов счетчика (глобальная переменная, атрибут, декоратор).

## Через глобальную переменную

IS_PALINDROME_COUNTER = 0

def is_palindrome_gl_cnt(s: str) -> bool:
    """Проверяет является ли строка палиндромом, рекурсивная. Возвращает bool."""
    global IS_PALINDROME_COUNTER
    IS_PALINDROME_COUNTER += 1
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return is_palindrome_gl_cnt(s[1:-1])

check_for_palindrome = ['123454321', 'aasdasdasf', 'aaaaaaaa', 'bbbmmmnnn']

[print(is_palindrome_gl_cnt(check_for_palindrome[i])) for i in
 range(len(check_for_palindrome))]

print(f'''\nФункция {is_palindrome_gl_cnt.__name__} была вызвана
    {IS_PALINDROME_COUNTER} раз(а).\n''')

# Через атрибут


def is_palindrome_attr_cnt(s: str) -> bool:
    """Проверяет является ли строка палиндромом, рекурсивная. Возвращает bool."""
    is_palindrome_attr_cnt.counter += 1
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return is_palindrome_attr_cnt(s[1:-1])


is_palindrome_attr_cnt.counter = 0


[print(is_palindrome_attr_cnt(check_for_palindrome[i])) for i in
 range(len(check_for_palindrome))]

print(f'\nФункция {is_palindrome_attr_cnt.__name__} была вызвана \
    {is_palindrome_attr_cnt.counter} раз(а).\n')

# Через декоратор

def is_palindrome_deco(s: str) -> bool:
    """Проверяет является ли строка палиндромом, рекурсивная. Возвращает bool."""
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return is_palindrome_deco(s[1:-1])


is_palindrome_deco = counter(is_palindrome_deco)

[print(is_palindrome_deco(check_for_palindrome[i])) for i in
 range(len(check_for_palindrome))]

##############################################################################
# 2. Функция, которая объявляет внутри себя функцию суммирования и возвращает ее в 
# качестве результата работы.

def external_func(*args, **kwargs) -> Callable:
    def custom_sum(*args: int | float, **kwargs: Dict[Any, int | float])\
            -> int | float:
        if all(map(lambda x: type(x) in (int, float), (*args, *kwargs.values()))): 
            return sum((*args, *kwargs.values()))
        else:
            raise TypeError('В функцию необходимо передать целое или вещественное число.')
    return custom_sum

# 3. Присвеоение функции, содержащей функцию суммирования переменной и печать
# переменной

test_func = external_func

print(test_func(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))

# -> <function external_func.<locals>.custom_sum at 0x7f185d0108b0>

# На экран выведено текстовое представление возвращаемой функции. Для того чтобы
# функция сумирования, объявленная внутри другой функции сработала необходимо 
# вызвать ее иным образом - добавить еще одни скобки

# 4. Вызов функции суммирования из объявленной переменной:

print(test_func()(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))

# -> 55

##############################################################################
# Hard
##############################################################################

# Глобальный счетчик перенесен в пространство объемлющей функции
# Такой код работать не будет, т.к.функция суммирования не имеет доступа
# к переменной, объявленной внутри объемлющей функции. В итоге получим
# ошибку UnboundLocalError

def external_func(*args, **kwargs) -> Callable:
    '''Определяет и возвращает функцию суммирования'''  
    ext_func_counter = 0
    def custom_sum(*args: int | float, **kwargs: Dict[Any, int | float])\
            -> int | float:
        '''Суммирует переданные целые или вещественные числа, возвращает соответствующие числа'''
        ext_func_counter += 1
        if all(map(lambda x: type(x) in (int, float), (*args, *kwargs.values()))): 
            return sum((*args, *kwargs.values()))
        else:
            raise TypeError('В функцию необходимо передать целое или вещественное число.')
    print(f'Функция {external_func.__name__} вызвана {ext_func_counter} раз(а).')
    return custom_sum

print(external_func()([i for i in range(1, 11)]))

# -> UnboundLocalError: local variable 'ext_func_counter' referenced before assignment

# Чтобы код заработал внутри функции custom_sum необходимо объявить nonlocal
# переменную ext_func_counter, что сделает ее доступной для вложенной функции,
# в том числе и для изменения этой переменной. Но здесь теряется логика счетчика
# переменная, определенная внутри объемлющей функции каждый раз при ее вызове
# перезаписывается. Получается, что каждый раз при вызове функции мы обнуляем 
# счетчик, который посчитает только один вызов функции.

def external_func(*args, **kwargs) -> Callable:
    '''Определяет и возвращает функцию суммирования'''
    ext_func_counter = 0
    def custom_sum(*args: int | float, **kwargs: Dict[Any, int | float])\
            -> int | float:
        '''Суммирует переданные целые или вещественные числа, возвращает соответствующие числа'''
        nonlocal ext_func_counter
        ext_func_counter += 1
        if all(map(lambda x: type(x) in (int, float), (*args, *kwargs.values()))): 
            return sum((*args, *kwargs.values()))
        else:
            raise TypeError('В функцию необходимо передать целое или вещественное число.')
    res = custom_sum(*args, **kwargs)
    print(f'Функция {external_func.__name__} вызвана {ext_func_counter} раз(а).')
    return res

for i in range(10):
    print(external_func(*list(range(0, i + 5))))
