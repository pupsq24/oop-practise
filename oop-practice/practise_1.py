"""Практика 1: иерархия сотрудников компании

Наследование: базовый класс Employee и дочерние классы Manager и 
Developer, каждый расчитывает зарплату по своим правилам.
"""


class Employee:
    """Базовый класс сотрудника компании.

    Attributes:
        name(str): Имя.
        base_salary(float): Базовый оклад в руб.
    """

    def __init__(self, name, base_salary):
        """Создает сотрудника.
        
        Args:
            name(str): Имя.
            base_salary(float): Базовый оклад в руб.
        """
        self.name = name 
        self.base_salary = base_salary

    def calculate_salary(self):
        """Рассчитывает зарплату сотрудника.

        Returns:
            float: Зарплата, равная базовому окладу.
        """
        return self.base_salary


class Manager(Employee):
    """Менеджер: получает бонус за каждого подчиненного.
    
    Attributes:
        team_size(int): Количество подчиненных.
        TEAM_BONUS_RATE(float): Доля оклада, начисляемого за каждого подчиненного.
    """
    TEAM_BONUS_RATE = 0.1

    def __init__(self, name, base_salary, team_size):
        """Создает менеджера.
                
        Args:
            name(str): Имя.
            base_salary(float): Базовый оклад в руб.
            team_size(int): Количество подчинённых.
        """
        super().__init__(name, base_salary)
        self.team_size = team_size

    def calculate_salary(self):
        """Рассчитывает зарплату с бонусом за размер команды.

        Формула: оклад + оклад * TEAM_BONUS_RATE * team_size.

        Returns:
            float: Зарплата менеджера.
        """
        base = super().calculate_salary()
        return base + base * self.TEAM_BONUS_RATE * self.team_size


class Developer(Employee):
    """Разработчик: зарплата зависит от грейда.

    Attributes:
        GRADE_MULTIPLIERS (dict[str, float]): Коэффициент оклада
            для каждого допустимого грейда.
        grade(str): Грейд разработчика.
    """

    GRADE_MULTIPLIERS = {
        'junior': 1.0,
        'middle': 1.2,
        'senior': 1.6
    }

    def __init__(self, name, base_salary, grade):
        """Создаёт разработчика.

        Args:
            name (str): Имя разработчика.
            base_salary (float): Базовый оклад в рублях.
            grade (str): Грейд: 'junior', 'middle' или 'senior'.

        Raises:
            ValueError: Если грейд не входит в GRADE_MULTIPLIERS.
        """
        super().__init__(name, base_salary)
        if grade not in self.GRADE_MULTIPLIERS:
            raise ValueError(
                f'Неизвестный грейд: {grade}. Допустимые: {list(self.GRADE_MULTIPLIERS)}'
            )
        self.grade = grade

    def calculate_salary(self):
        """Рассчитывает зарплату с учётом грейда.

        Формула: оклад * коэффициент грейда.

        Returns:
            float: Зарплата разработчика.
        """
        multiplier = self.GRADE_MULTIPLIERS[self.grade]
        return super().calculate_salary() * multiplier


if __name__ == '__main__':
    employee = Employee('Миша', 55000)
    manager = Manager('Светлана', 60000, 6)
    developer = Developer('Гриша', 57000, 'senior')

    print(employee.calculate_salary())
    print(manager.calculate_salary())
    print(developer.calculate_salary())

    try:
        developer_invalid = Developer('Вася', 50000, 'lead')
    except ValueError as e:
        print(e)