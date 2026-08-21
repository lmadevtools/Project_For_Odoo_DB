from Utils.validator import is_valid_email

def validate_customer_id(customer_id):
    if not customer_id or not str(customer_id).strip():
        raise ValueError("Invalid ID")
    return customer_id


def validate_name(name):
    if not name or not name.strip():
        raise ValueError("Client name cannot be empty")
    return name.strip()


def validate_email(email):
    if not is_valid_email(email):
        raise ValueError(f"Invalid mail: {email!r}")
    return email.strip().lower()


def normalize_phone(phone):
    return phone.strip() if phone else ""


def create_customer(
    customer_id,
    name,
    email,
    phone="",
    active=True
):
    return {
        "customer_id": validate_customer_id(customer_id),
        "name": validate_name(name),
        "email": validate_email(email),
        "phone": normalize_phone(phone),
        "active": active,
    }


def archive_customer(customer):
    return {
        **customer,
        "active": False,
    }

def archive_customer_by_id(customers, customer_id):
    return [
        archive_customer(customer)
        if customer["customer_id"] == customer_id
        else customer
        for customer in customers
    ]


def unarchive_customer(customer):
    return {
        **customer,
        "active": True,
    }


def is_active(customer):
    return customer["active"]


def get_customer_email(customer):
    return customer["email"]


def get_active_customers(customers):
    return filter(is_active, customers)


def get_active_customer_emails(customers):
    return map(
        get_customer_email,
        get_active_customers(customers)
    )


def format_customer(customer):
    status = "" if customer["active"] else " [ARCHIVED]"

    phone = (
        f" | {customer['phone']}"
        if customer["phone"]
        else ""
    )

    return (
        f"[{customer['customer_id']}] "
        f"{customer['name']}{status} | "
        f"{customer['email']}"
        f"{phone}"
    )


def calculate_active_customer_count(customers):
    return sum(
        1
        for customer in customers
        if is_active(customer)
    )




