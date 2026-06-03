from Classes.stock_move import StockMove

class Product:

    def __init__(
        self,
        product_id,
        name,
        price,
        quantity,
        minimum_stock=5,
        category="General",
        active=True
    ):
        if not isinstance(product_id, (int, str)) or not str(product_id).strip():
            raise ValueError("Invalid product_id")
        if not name or not name.strip():
            raise ValueError("Product name cannot be empty")
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        if minimum_stock < 0:
            raise ValueError("Min. stock cannot be negative")

        self._product_id    = product_id        # read-only via property
        self._name          = name.strip()       # setter with validation
        self._price         = price              # setter with validation
        self._quantity      = quantity           # read-only, modified only via add/remove_stock
        self._minimum_stock = minimum_stock      # setter with validation
        self.category       = category           # no property needed
        self.active         = active             # no property needed

    #PROPERTIES
    @property
    def product_id(self):
        return self._product_id
    # no setter — product_id is read-only

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not value.strip():
            raise ValueError("Product name cannot be empty")
        self._name = value.strip()

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value

    @property
    def quantity(self):
        return self._quantity
    # no setter — quantity must be modified only via add_stock / remove_stock

    @property
    def minimum_stock(self):
        return self._minimum_stock

    @minimum_stock.setter
    def minimum_stock(self, value):
        if value < 0:
            raise ValueError("Min. stock cannot be negative")
        self._minimum_stock = value

	#stock management
    def add_stock(self, amount, reason=""):
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Quantity to add cannot be negative")
        self._quantity += amount
        return StockMove(self._product_id, self._name, amount, "in", reason)

    def remove_stock(self, amount, reason=""):
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Quantity to remove cannot be negative")
        if amount > self._quantity:
            raise ValueError(
                f"Not enough quantity available in stock : {self._quantity} , "
                f"{amount} waited"
            )
        self._quantity -= amount
        return StockMove(self._product_id, self._name, amount, "out", reason)

    def is_low_stock(self):
        return self._quantity <= self._minimum_stock

	#Archive
    def archive(self):
        self.active = False

    def unarchive(self):
        self.active = True

    #Serialization for JSON - not used anymore
    '''
    def to_dict(self):
        return {
            "product_id":    self._product_id,
            "name":          self._name,
            "price":         self._price,
            "quantity":      self._quantity,
            "minimum_stock": self._minimum_stock,
            "category":      self.category,
            "active":        self.active
        }

    @classmethod
    def from_dict(cls, data):
        try:
            return cls(
                product_id    = data["product_id"],
                name          = data["name"],
                price         = data["price"],
                quantity      = data["quantity"],
                minimum_stock = data.get("minimum_stock", 10),
                category      = data.get("category", "General"),
                active        = data.get("active", True)
            )
        except KeyError as e:
            raise KeyError(f"missing mandatory field : {e}")
    '''

    #Display
    def __str__(self):
        status = "" if self.active else " [ARCHIVED]"
        low    = " low stock" if self.is_low_stock() else ""
        return (
            f"[{self._product_id}] {self._name}{status} | "
            f"Category : {self.category} | "
            f"Price : {self._price:.2f}€ | "
            f"Stock : {self._quantity}{low}"
        )

    def __repr__(self):
        return (
            f"Product(id={self._product_id!r}, name={self._name!r}, "
            f"price={self._price}, quantity={self._quantity}, active={self.active})"
        )