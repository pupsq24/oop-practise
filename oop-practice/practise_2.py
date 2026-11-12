"""Практика 2: иерархия транспортных средств.

Модуль демонстрирует полиморфизм: дочерние классы Car,
Motorcycle и Truck переопределяют метод get_info() базового
класса Vehicle, и каждый возвращает собственное описание.
"""


class Vehicle:
    """Базовое транспортное средство.

    Attributes:
        model (str): Модель транспортного средства.
        year (int): Год выпуска.
        max_speed (int): Максимальная скорость в км/ч.
    """

    def __init__(self, model, year, max_speed):
        """Создаёт транспортное средство.

        Args:
            model (str): Модель транспортного средства.
            year (int): Год выпуска.
            max_speed (int): Максимальная скорость в км/ч.
        """
        self.model = model
        self.year = year
        self.max_speed = max_speed

    def get_info(self):
        """Возвращает общее описание транспортного средства.

        Returns:
            str: Модель, год выпуска и максимальная скорость.
        """
        return (
            f"Модель: {self.model}, "
            f"Год выпуска: {self.year}, "
            f"Максимальная скорость: {self.max_speed} км/ч"
        )


class Car(Vehicle):
    """Легковой автомобиль.

    Attributes:
        fuel_type (str): Тип топлива, например «Бензин».
    """

    def __init__(self, model, year, max_speed, fuel_type):
        """Создаёт автомобиль.

        Args:
            model (str): Модель автомобиля.
            year (int): Год выпуска.
            max_speed (int): Максимальная скорость в км/ч.
            fuel_type (str): Тип топлива.
        """
        super().__init__(model, year, max_speed)
        self.fuel_type = fuel_type

    def get_info(self):
        """Возвращает описание автомобиля.

        Returns:
            str: Общее описание с добавленным типом топлива.
        """
        base_info = super().get_info()
        return f"{base_info}, Тип топлива: {self.fuel_type}"


class Motorcycle(Vehicle):
    """Мотоцикл.

    Attributes:
        has_sidecar (bool): Есть ли у мотоцикла коляска.
    """

    def __init__(self, model, year, max_speed, has_sidecar):
        """Создаёт мотоцикл.

        Args:
            model (str): Модель мотоцикла.
            year (int): Год выпуска.
            max_speed (int): Максимальная скорость в км/ч.
            has_sidecar (bool): True, если есть коляска.
        """
        super().__init__(model, year, max_speed)
        self.has_sidecar = has_sidecar

    def get_info(self):
        """Возвращает описание мотоцикла.

        Returns:
            str: Общее описание с указанием наличия коляски.
        """
        base_info = super().get_info()
        sidecar_info = "с коляской" if self.has_sidecar else "без коляски"
        return f"{base_info}, {sidecar_info}"


class Truck(Vehicle):
    """Грузовик.

    Attributes:
        cargo_capacity (int): Грузоподъёмность в килограммах.
    """

    def __init__(self, model, year, max_speed, cargo_capacity):
        """Создаёт грузовик.

        Args:
            model (str): Модель грузовика.
            year (int): Год выпуска.
            max_speed (int): Максимальная скорость в км/ч.
            cargo_capacity (int): Грузоподъёмность в кг.
        """
        super().__init__(model, year, max_speed)
        self.cargo_capacity = cargo_capacity

    def get_info(self):
        """Возвращает описание грузовика.

        Returns:
            str: Общее описание с добавленной грузоподъёмностью.
        """
        base_info = super().get_info()
        return f"{base_info}, Грузоподъемность: {self.cargo_capacity} кг"


if __name__ == "__main__":
    vehicles = [
        Car("Toyota Camry", 2020, 200, "Бензин"),
        Motorcycle("Harley-Davidson", 2019, 180, True),
        Truck("Volvo FH", 2021, 120, 25000)
    ]

    for vehicle in vehicles:
        print(vehicle.get_info())
