from datetime import datetime


class StockMove:

    DIRECTIONS = ("in", "out")

    def __init__(
        self,
        product_id,
        product_name,
        quantity,
        direction,
        reason="",
        created_at=None
    ):
        if direction not in self.DIRECTIONS:
            raise ValueError("Invalid Direction")
        if quantity <= 0:
            raise ValueError("Invalid Quantity")

        self._product_id   = product_id         # read-only
        self._product_name = product_name        # read-only
        self._quantity     = quantity            # read-only
        self._direction    = direction           # read-only
        self._reason       = reason              # read-only
        self._created_at   = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # read-only

    #PROPERTIES — all read-only, a stock move must never be modified
    @property
    def product_id(self):
        return self._product_id

    @property
    def product_name(self):
        return self._product_name

    @property
    def quantity(self):
        return self._quantity

    @property
    def direction(self):
        return self._direction

    @property
    def reason(self):
        return self._reason

    @property
    def created_at(self):
        return self._created_at

    # Serialization for JSON
    def to_dict(self):
        return {
            "product_id":   self._product_id,
            "product_name": self._product_name,
            "quantity":     self._quantity,
            "direction":    self._direction,
            "reason":       self._reason,
            "created_at":   self._created_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            product_id   = data["product_id"],
            product_name = data["product_name"],
            quantity     = data["quantity"],
            direction    = data["direction"],
            reason       = data["reason"],
            created_at   = data["created_at"]
        )


    #Display
    def __str__(self):
        arrow = " IN " if self._direction == "in" else " OUT"
        return (
            f"[{self._created_at[:10]}] {arrow} | "
            f"{self._product_name} | "
            f"Qtt : {self._quantity}"
            + (f" | {self._reason}" if self._reason else "")
        )
