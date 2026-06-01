from datetime import datetime
from Classes.product import Product


class OrderLine:
    #an order line (1 product + quantity + price)

    def __init__(self, product: Product, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be a positive number")   #manage empty or negative qtt error

        self.product        = product
        self.quantity       = quantity
        self.unit_price     = product.price   #price fixed at the order time

    @property
    def subtotal(self):
        return round(self.unit_price * self.quantity, 2)

    #serialization for JSON
    def to_dict(self):
        return {
            "product_id": self.product.product_id,
            "product_name": self.product.name,  
            "quantity":   self.quantity,
            "unit_price": self.unit_price,
            "subtotal":   self.subtotal
        }

    def __str__(self):
        return (
            f"  {self.product.name} x{self.quantity} "
            f"@ {self.unit_price:.2f}€ = {self.subtotal:.2f}€"
        )


# ======================================================================

class Order:
    VALID_STATUS = ("draft", "confirmed", "done", "cancelled")   #limit status of an order to those choice

    def __init__(
        self,
        order_id,
        customer,
        lines=None,
        status="draft",
        created_at=None
    ):
        if not order_id or not str(order_id).strip():
            raise ValueError("Invalid order_id")                 #error : invalid ID
        if status not in self.VALID_STATUS:
            raise ValueError(f"Invalid Status : {status!r}")     #error invalid status

        self.order_id   = order_id
        self.customer   = customer
        self.lines      = lines if lines is not None else []
        self.status     = status
        self.created_at = created_at or datetime.now().isoformat()

    #Add a new line or udpate quantity in the order
    def add_line(self, product: Product, quantity: int):
        if self.status != "draft":
            raise RuntimeError("Cannot update an order if not in draft status")  #error if not in draft status
        if not product.active:
            raise ValueError(f"product '{product.name}' is archived")    #error if product not active

        for line in self.lines:
            if line.product.product_id == product.product_id:
                line.quantity += quantity
                return

        self.lines.append(OrderLine(product, quantity))


    #remove a line in the order
    def remove_line(self, product_id):
        if self.status != "draft":
            raise RuntimeError("Cannot update an order if not in draft status") #error if not in draft status
        before = len(self.lines)
        self.lines = [l for l in self.lines if l.product.product_id != product_id]
        if len(self.lines) == before:
            raise ValueError(f"No line for the product : {product_id!r}")

    #Confirm order and update stock
    def confirm(self):
        if self.status != "draft":
            raise RuntimeError(f"Cannot confirm a order in status '{self.status}'")  #error if not in draft
        if not self.lines:
            raise RuntimeError("Cannot confirm an empty order ")  #error no line in the order

        for line in self.lines:
            line.product.remove_stock(line.quantity)   # lève ValueError if not enough stock

        self.status = "confirmed"

	#order done
    def mark_done(self):
        if self.status != "confirmed":
            raise RuntimeError(f"Order must be 'confirmed' before 'done' (current status : '{self.status}')")
        self.status = "done"

    #cancel order and put back in stock
    def cancel(self):
        if self.status in ("done", "cancelled"):
            raise RuntimeError(f"Cannot cancel an order in this status : '{self.status}'")
        if self.status == "confirmed":
            for line in self.lines:
                line.product.add_stock(line.quantity)
        self.status = "cancelled"

    #round the total.
    @property
    def total(self):
        return round(sum(l.subtotal for l in self.lines), 2)

    #Serialization for JSON
    def to_dict(self):
        return {
            "order_id":   self.order_id,
            "customer_id": self.customer.customer_id,
            "customer_name": self.customer.name,  # dénormalization
            "status":     self.status,
            "created_at": self.created_at,
            "lines":      [l.to_dict() for l in self.lines],
            "total":      self.total
        }

    #Display
    def __str__(self):
        header = (
            f"Order {self.order_id} | Client : {self.customer.name} | "
            f"Status : {self.status.upper()} | created : {self.created_at[:10]}"
        )
        lines = "\n".join(str(l) for l in self.lines) if self.lines else "  (no row)"
        return f"{header}\n{lines}\n  TOTAL : {self.total:.2f}€"

    def __repr__(self):
        return (
            f"Order(id={self.order_id!r}, customer={self.customer.name!r}, "
            f"status={self.status!r}, lines={len(self.lines)}, total={self.total})"
        )
