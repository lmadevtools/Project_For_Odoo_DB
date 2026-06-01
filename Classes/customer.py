from Utils.validator import is_valid_email


class Customer:

    def __init__(
        self,
        customer_id,
        name,
        email,
        phone="",
        active=True
    ):
        if not customer_id or not str(customer_id).strip():
            raise ValueError("Invalid ID")
        if not name or not name.strip():
            raise ValueError("Client name cannot be empty")
        if not is_valid_email(email):
            raise ValueError(f"Invalid mail: {email!r}")

        self._customer_id = customer_id        # read-only via property
        self._name        = name.strip()        # setter with validation
        self._email       = email.strip().lower()  # setter with validation
        self._phone       = phone.strip()       # setter with strip
        self.active       = active              # no property needed

    #PROPERTIES
    @property
    def customer_id(self):
        return self._customer_id
    # no setter — customer_id is read-only

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not value.strip():
            raise ValueError("Client name cannot be empty")
        self._name = value.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not is_valid_email(value):
            raise ValueError(f"Invalid mail: {value!r}")
        self._email = value.strip().lower()

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        self._phone = value.strip() if value else ""

	#Archive
    def archive(self):
        self.active = False

    def unarchive(self):
        self.active = True

    #serialization for JSON
    def to_dict(self):
        return {
            "customer_id": self._customer_id,
            "name":        self._name,
            "email":       self._email,
            "phone":       self._phone,
            "active":      self.active
        }

    @classmethod
    def from_dict(cls, data):
        try:
            return cls(
                customer_id = data["customer_id"],
                name        = data["name"],
                email       = data["email"],
                phone       = data.get("phone", ""),
                active      = data.get("active", True),
            )
        except KeyError as e:
            raise KeyError(f"missing mandatory information : {e}")

    #Display
    def __str__(self):
        status = "" if self.active else " [ARCHIVED]"
        return (
            f"[{self._customer_id}] {self._name}{status} | "
            f"{self._email}"
            + (f" | {self._phone}" if self._phone else "")
        )

    def __repr__(self):
        return (
            f"Customer(id={self._customer_id!r}, name={self._name!r}, "
            f"email={self._email!r}, active={self.active})"
        )
