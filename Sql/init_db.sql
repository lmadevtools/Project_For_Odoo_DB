--PRODUCTS
CREATE TABLE IF NOT EXISTS products(
    product_id              VARCHAR(10)         PRIMARY KEY,
    product_name            VARCHAR(100)        NOT NULL,
    price                   DECIMAL(10,2)       NOT NULL 
                                                CONSTRAINT products_min_price CHECK (price >= 0),
    quantity                INT                 NOT NULL 
                                                CONSTRAINT products_min_quantity CHECK (quantity >= 0),
    minimum_stock           INT                 DEFAULT 5 
                                                CONSTRAINT products_min_stock CHECK (minimum_stock >= 0),
    category                VARCHAR(50)         DEFAULT 'General',
    active                  BOOLEAN             DEFAULT TRUE
);

--CUSTOMERS
CREATE TABLE IF NOT EXISTS customers(
    customer_id             VARCHAR(10)         PRIMARY KEY,
    customer_name            VARCHAR(100)        NOT NULL,
    email                   VARCHAR(150)        NOT NULL UNIQUE,
    phone                   VARCHAR(20)         DEFAULT '',
    active                  BOOLEAN             NOT NULL DEFAULT TRUE
);

--ORDERS
CREATE TABLE IF NOT EXISTS orders(
    order_id                VARCHAR(20)         PRIMARY KEY,
    customer_id             VARCHAR(10)         NOT NULL, 
                                                CONSTRAINT orders_fk_customer  
                                                FOREIGN KEY(customer_id)
                                                REFERENCES customers(customer_id),
    customer_name           VARCHAR(100)        NOT NULL,
    order_status            VARCHAR(20)         NOT NULL DEFAULT 'draft' 
                                                CONSTRAINT orders_status_range CHECK (order_status IN ('draft','confirmed','done','cancelled')),
    created_at              TIMESTAMP           NOT NULL DEFAULT NOW(),
    total                   DECIMAL(10,2)       NOT NULL DEFAULT 0
);

--ORDERLINES
CREATE TABLE IF NOT EXISTS order_lines(
    id                      SERIAL              PRIMARY KEY,
    order_id                VARCHAR(20)         NOT NULL, 
                                                CONSTRAINT order_lines_fk_order  
                                                FOREIGN KEY(order_id)
                                                REFERENCES orders(order_id),
    product_id              VARCHAR(10)         NOT NULL, 
                                                CONSTRAINT order_lines_fk_product  
                                                FOREIGN KEY(product_id)
                                                REFERENCES products(product_id),
    product_name            VARCHAR(100)        NOT NULL,
    quantity                INT                 NOT NULL 
                                                CONSTRAINT orders_lines_min_quantity CHECK (quantity > 0),
    unit_price              DECIMAL(10,2)       NOT NULL 
                                                CONSTRAINT orders_lines_min_unit_price CHECK (unit_price >= 0),
    subtotal                DECIMAL(10,2)       NOT NULL
);

--STOCK_MOVES
CREATE TABLE IF NOT EXISTS stock_moves(
    id                      SERIAL              PRIMARY KEY,  
    product_id              VARCHAR(10)         NOT NULL, 
                                                CONSTRAINT stock_moves_fk_product  
                                                FOREIGN KEY(product_id)
                                                REFERENCES products(product_id),
    product_name            VARCHAR(100)        NOT NULL,
    quantity                INT                 NOT NULL 
                                                CONSTRAINT stock_moves_min_quantity CHECK(quantity > 0),
    direction               VARCHAR(3)          NOT NULL 
                                                CONSTRAINT stock_moves_direction_range CHECK (direction IN('in','out')),
    reason                  VARCHAR(255)        DEFAULT '',
    created_at              TIMESTAMP           NOT NULL DEFAULT NOW()
);
