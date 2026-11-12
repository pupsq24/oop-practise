import random


class CrewMember:
    """Член экипажа космического корабля.

    Attributes:
        ROLES (tuple[str, ...]): Допустимые роли в команде.
        name (str): Имя члена экипажа.
        role (str): Роль в команде.
        health (int): Здоровье от 0 до 100.
        skills (list[str]): Навыки члена экипажа.
    """

    ROLES = ('Pilot', 'Engineer', 'Scientist', 'Medic', 'Soldier')

    def __init__(self, name, role, health=100, skills=None):
        """Создаёт члена экипажа.

        Args:
            name (str): Имя члена экипажа.
            role (str): Роль, одна из ROLES.
            health (int): Начальное здоровье от 0 до 100.
            skills (list[str] | None): Навыки. По умолчанию пусто.

        Raises:
            ValueError: Если роль недопустима или здоровье
                вне диапазона от 0 до 100.
        """
        if role not in self.ROLES:
            raise ValueError(
                f'Неизвестная роль: {role}. Допустимые: {list(self.ROLES)}'
            )
        if not (0 <= health <= 100):
            raise ValueError("Здоровье должно быть в диапазоне от 0 до 100.")
        self.name = name
        self.role = role
        self.health = health
        self.skills = skills or []

    def is_alive(self):
        """Проверяет, жив ли член экипажа.

        Returns:
            bool: True, если здоровье больше нуля.
        """
        return self.health > 0

    def take_damage(self, amount):
        """Наносит урон. Здоровье не опускается ниже нуля.

        Args:
            amount (int): Величина урона, не меньше нуля.

        Raises:
            ValueError: Если урон отрицательный.
        """
        if amount < 0:
            raise ValueError("Урон не может быть отрицательным.")
        self.health = max(0, self.health - amount)

    def heal(self, amount):
        """Восстанавливает здоровье, но не выше 100.

        Args:
            amount (int): Величина лечения, не меньше нуля.

        Raises:
            ValueError: Если величина лечения отрицательная.
        """
        if amount < 0:
            raise ValueError("Исцеление не может быть отрицательным.")
        self.health = min(100, self.health + amount)

    def __str__(self):
        """Возвращает имя, роль и здоровье для вывода."""
        return f'{self.name} ({self.role}) - Здоровье: {self.health}'


class SpaceShip:
    """Космический корабль с экипажем.

    Attributes:
        FUEL_PER_SPEED (float): Расход топлива на единицу ускорения.
        name (str): Название корабля.
        crew (list[CrewMember]): Экипаж.
        fuel_level (float): Запас топлива от 0 до 100.
        speed (int): Текущая скорость: расстояние за один ход.
        durability (int): Прочность корпуса от 0 до 100.
    """

    FUEL_PER_SPEED = 0.5

    def __init__(self, name, crew=None, fuel_level=100,
                 speed=0, durability=100):
        """Создаёт корабль.

        Args:
            name (str): Название корабля.
            crew (list[CrewMember] | None): Начальный экипаж.
            fuel_level (float): Начальный запас топлива.
            speed (int): Начальная скорость.
            durability (int): Начальная прочность корпуса.
        """
        self.name = name
        self.crew = crew or []
        self.fuel_level = fuel_level
        self.speed = speed
        self.durability = durability

    def add_crew_member(self, crew_member):
        """Добавляет члена экипажа на борт.

        Args:
            crew_member (CrewMember): Новый член экипажа.

        Raises:
            TypeError: Если передан объект не класса CrewMember.
        """
        if not isinstance(crew_member, CrewMember):
            raise TypeError("Можно добавлять только объекты CrewMember.")
        self.crew.append(crew_member)

    def accelerate(self, amount):
        """Увеличивает скорость, расходуя топливо.

        Расход топлива: amount * FUEL_PER_SPEED.

        Args:
            amount (int): Прирост скорости, не меньше нуля.

        Raises:
            ValueError: Если прирост скорости отрицательный.
            RuntimeError: Если топлива недостаточно.
        """
        if amount < 0:
            raise ValueError("Ускорение не может быть отрицательным.")
        fuel_needed = amount * self.FUEL_PER_SPEED
        if fuel_needed > self.fuel_level:
            raise RuntimeError("Недостаточно топлива для ускорения.")
        self.speed += amount
        self.fuel_level -= fuel_needed

    def refuel(self, amount):
        """Заправляет корабль, но не выше 100.

        Args:
            amount (float): Количество топлива, не меньше нуля.

        Raises:
            ValueError: Если количество отрицательное.
        """
        if amount < 0:
            raise ValueError("Количество топлива не может быть отрицательным.")
        self.fuel_level = min(100, self.fuel_level + amount)

    def take_damage(self, amount):
        """Наносит урон корпусу. Прочность не опускается ниже нуля.

        Args:
            amount (int): Величина урона, не меньше нуля.

        Raises:
            ValueError: Если урон отрицательный.
        """
        if amount < 0:
            raise ValueError("Урон не может быть отрицательным.")
        self.durability = max(0, self.durability - amount)

    def is_operational(self):
        """Проверяет, может ли корабль продолжать полёт.

        Returns:
            bool: True, если корпус цел, есть топливо
                и жив хотя бы один член экипажа.
        """
        return (
            self.durability > 0
            and self.fuel_level > 0
            and any(m.is_alive() for m in self.crew)
        )

    def has_role(self, role):
        """Проверяет, есть ли на борту живой член экипажа с ролью.

        Args:
            role (str): Искомая роль, например 'Pilot'.

        Returns:
            bool: True, если такой живой член экипажа есть.
        """
        return any(
            member.role == role and member.is_alive()
            for member in self.crew
        )

    def __str__(self):
        """Возвращает название корабля и размер экипажа."""
        return f'Корабль: {self.name}, Экипаж: {len(self.crew)} членов'


class Mission:
    """Миссия корабля: цель, расход ресурсов и случайные события.

    События:
        * астероид - урон корпусу и случайному члену экипажа,
          пилот вдвое снижает урон корпусу;
        * неисправность - урон корпусу, инженер её устраняет;
        * спокойный полёт - медик лечит экипаж.

    Attributes:
        ASTEROID_DAMAGE (int): Урон корпусу от астероида.
        MALFUNCTION_DAMAGE (int): Урон корпусу от неисправности.
        FUEL_PER_TURN (int): Расход топлива за ход.
        VICTIM_DAMAGE (int): Урон члену экипажа от астероида.
        CALM_HEAL (int): Лечение экипажа медиком за ход.
        name (str): Название миссии.
        ship (SpaceShip): Корабль, выполняющий миссию.
        target_distance (int): Расстояние до цели.
        current_distance (int): Пройденное расстояние.
        log (list[str]): Журнал событий миссии.
    """

    ASTEROID_DAMAGE = 20
    MALFUNCTION_DAMAGE = 15
    FUEL_PER_TURN = 5
    VICTIM_DAMAGE = 10
    CALM_HEAL = 5

    def __init__(self, name, ship, target_distance):
        """Создаёт миссию.

        Args:
            name (str): Название миссии.
            ship (SpaceShip): Корабль для миссии.
            target_distance (int): Расстояние до цели.

        Raises:
            TypeError: Если ship не является объектом SpaceShip.
        """
        if not isinstance(ship, SpaceShip):
            raise TypeError("ship должен быть объектом SpaceShip.")
        self.name = name
        self.ship = ship
        self.target_distance = target_distance
        self.current_distance = 0
        self.log = []

    def _asteroid(self):
        """Событие: столкновение с астероидом."""
        damage = self.ASTEROID_DAMAGE
        if self.ship.has_role('Pilot'):
            damage //= 2
        self.ship.take_damage(damage)
        victim = random.choice(self.ship.crew)
        victim.take_damage(self.VICTIM_DAMAGE)
        self.log.append(
            f"Астероид! Корпус -{damage}. "
            f"{victim.name} получил урон {self.VICTIM_DAMAGE}."
        )

    def _malfunction(self):
        """Событие: неисправность систем корабля."""
        damage = self.MALFUNCTION_DAMAGE
        if self.ship.has_role('Engineer'):
            damage = 0
            self.log.append("Инженер исправил неисправность без ущерба.")
        else:
            self.log.append(f"Неисправность! Корпус -{damage}.")
        self.ship.take_damage(damage)

    def _calm(self):
        """Событие: спокойный полёт, медик лечит экипаж."""
        if self.ship.has_role('Medic'):
            for member in self.ship.crew:
                if member.is_alive():
                    member.heal(self.CALM_HEAL)
            self.log.append("Медик восстановил здоровье членов экипажа.")

    def run(self, turns):
        """Запускает миссию на заданное число ходов.

        На каждом ходу происходит случайное событие, корабль
        пролетает расстояние, равное своей скорости, и тратит
        FUEL_PER_TURN топлива. Все события пишутся в log.

        Args:
            turns (int): Максимальное число ходов.

        Returns:
            bool: True, если цель достигнута; False, если корабль
                вышел из строя или ходы закончились.
        """
        events = [self._asteroid, self._malfunction, self._calm]
        for turn in range(1, turns + 1):
            event = random.choice(events)
            event()
            self.current_distance += self.ship.speed
            self.ship.fuel_level = max(
                0, self.ship.fuel_level - self.FUEL_PER_TURN
            )
            if self.current_distance >= self.target_distance:
                self.log.append(f"Ход {turn}: цель достигнута!")
                return True
            if not self.ship.is_operational():
                self.log.append(
                    f"Миссия '{self.name}' провалена на {turn}-м ходу."
                )
                return False
        self.log.append(
            f"Миссия '{self.name}': ходы закончились, цель не достигнута."
        )
        return False


if __name__ == '__main__':
    random.seed(42)
    ship = SpaceShip("Восток")
    ship.add_crew_member(CrewMember("Юрий", "Pilot"))
    ship.add_crew_member(CrewMember("Анна", "Engineer"))
    ship.add_crew_member(CrewMember("Олег", "Medic"))
    ship.accelerate(20)

    mission = Mission("Марс", ship, target_distance=150)
    success = mission.run(turns=10)

    for entry in mission.log:
        print(entry)
    print("Успех!" if success else "Провал.")
    for member in ship.crew:
        print(member)
