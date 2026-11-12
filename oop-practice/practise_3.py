"""Практика 3: модель онлайн-магазина.

Модуль реализует товары, корзину, заказы и покупателей.
Товар резервируется на складе при добавлении в корзину
и возвращается на склад при удалении из неё.
"""


class Product:
    """Товар в каталоге магазина.

    Attributes:
        name (str): Название товара.
        price (float): Цена за единицу в рублях.
        stock (int): Количество единиц на складе.
        category (str): Категория товара.
    """

    def __init__(self, name, price, stock, category):
        """Создаёт товар.

        Args:
            name (str): Название товара.
            price (float): Цена за единицу в рублях.
            stock (int): Начальный остаток на складе.
            category (str): Категория товара.
        """
        self.name = name
        self.price = price
        self.stock = stock
        self.category = category

    def get_info(self):
        """Возвращает описание товара.

        Returns:
            str: Название, цена, остаток и категория.
        """
        return (
            f"Product: {self.name}, Price: {self.price}, "
            f"Stock: {self.stock}, Category: {self.category}"
        )


class ShoppingCart:
    """Корзина покупателя.

    При добавлении товар резервируется: его остаток на складе
    уменьшается. При удалении или уменьшении количества
    товар возвращается на склад.

    Attributes:
        items (list[tuple[Product, int]]): Позиции корзины
            в виде пар (товар, количество).
    """

    def __init__(self):
        """Создаёт пустую корзину."""
        self.items = []

    def add_product(self, product, quantity):
        """Добавляет товар в корзину и резервирует его на складе.

        Если товар уже есть в корзине, его количество
        увеличивается, а новая позиция не создаётся.

        Args:
            product (Product): Добавляемый товар.
            quantity (int): Количество единиц, больше нуля.

        Raises:
            ValueError: Если количество не больше нуля
                или на складе недостаточно товара.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        if quantity > product.stock:
            raise ValueError("Not enough stock available.")
        for i, (p, q) in enumerate(self.items):
            if p == product:
                self.items[i] = (p, q + quantity)
                product.stock -= quantity
                return
        self.items.append((product, quantity))
        product.stock -= quantity

    def remove_product(self, product):
        """Удаляет товар из корзины и возвращает его на склад.

        Args:
            product (Product): Удаляемый товар.

        Raises:
            ValueError: Если товара нет в корзине.
        """
        for i, (p, quantity) in enumerate(self.items):
            if p == product:
                self.items.pop(i)
                product.stock += quantity
                return
        raise ValueError("Product not found in cart.")

    def update_quantity(self, product, new_quantity):
        """Изменяет количество товара в корзине.

        Разница между старым и новым количеством
        возвращается на склад или резервируется.

        Args:
            product (Product): Товар в корзине.
            new_quantity (int): Новое количество, больше нуля.

        Raises:
            ValueError: Если товара нет в корзине, количество
                не больше нуля или на складе недостаточно товара.
        """
        for i, (p, quantity) in enumerate(self.items):
            if p == product:
                if new_quantity <= 0:
                    raise ValueError("Quantity must be greater than zero.")
                if new_quantity <= product.stock + quantity:
                    product.stock += quantity - new_quantity
                    self.items[i] = (product, new_quantity)
                    return
                else:
                    raise ValueError("Not enough stock available.")
        raise ValueError("Product not found in cart.")

    def calculate_total(self):
        """Считает стоимость корзины без скидок и налогов.

        Returns:
            float: Сумма «цена × количество» по всем позициям.
        """
        total = 0
        for product, quantity in self.items:
            total += product.price * quantity
        return total


class Order:
    """Заказ, оформленный из корзины.

    Заказ сохраняет копию позиций корзины, поэтому
    последующая очистка корзины на него не влияет.
    Итог считается так: сначала применяется скидка,
    затем начисляется налог.

    Attributes:
        TAX_RATE (float): Ставка налога, 13%.
        discount (float): Скидка в долях, от 0 до 1.
        items (list[tuple[Product, int]]): Позиции заказа.
    """

    TAX_RATE = 0.13

    def __init__(self, cart, discount=0):
        """Создаёт заказ из корзины.

        Args:
            cart (ShoppingCart): Корзина с товарами.
            discount (float): Скидка в долях: 0.1 означает 10%.

        Raises:
            ValueError: Если скидка вне диапазона от 0 до 1
                или корзина пуста.
        """
        if discount < 0 or discount > 1:
            raise ValueError("Discount must be between 0 and 1.")
        if not cart.items:
            raise ValueError("Cannot create an order with an empty cart.")
        self.discount = discount
        self.items = list(cart.items)

    def calculate_final_total(self):
        """Считает итоговую стоимость заказа.

        Формула: сумма * (1 - discount) * (1 + TAX_RATE).

        Returns:
            float: Итог, округлённый до копеек.
        """
        total = 0
        for product, quantity in self.items:
            total += product.price * quantity
        return round(total * (1 - self.discount) * (1 + self.TAX_RATE), 2)


class Customer:
    """Покупатель магазина.

    Attributes:
        name (str): Имя покупателя.
        order_history (list[Order]): Оформленные заказы.
    """

    def __init__(self, name, order_history=None):
        """Создаёт покупателя.

        Args:
            name (str): Имя покупателя.
            order_history (list[Order] | None): Существующая
                история заказов. По умолчанию пустая.
        """
        self.name = name
        self.order_history = order_history or []

    def place_order(self, cart, discount=0):
        """Оформляет заказ из корзины и сохраняет его в историю.

        После оформления корзина очищается.

        Args:
            cart (ShoppingCart): Корзина с товарами.
            discount (float): Скидка в долях, от 0 до 1.

        Returns:
            Order: Оформленный заказ.

        Raises:
            ValueError: Если корзина пуста или скидка некорректна.
        """
        order = Order(cart, discount)
        cart.items.clear()
        self.order_history.append(order)
        return order


if __name__ == '__main__':
    milk = Product("Молоко", 100, 10, "Еда")
    cart = ShoppingCart()
    cart.add_product(milk, 4)
    cart.add_product(milk, 6)

    customer = Customer("Аня")
    order = customer.place_order(cart, discount=0.1)

    print("Итог заказа:", order.calculate_final_total())
    print("Остаток на складе:", milk.stock)
    print(milk.get_info())

    try:
        customer.place_order(cart)
    except ValueError as error:
        print("Ошибка:", error)