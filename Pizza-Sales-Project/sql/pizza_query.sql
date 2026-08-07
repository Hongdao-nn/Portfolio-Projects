-- Tạo bảng Pizza (Sản phẩm)
CREATE TABLE pizzas (
	pizza_name_id VARCHAR(50) PRIMARY KEY,
	pizza_size VARCHAR(10) NOT NULL,
	pizza_category VARCHAR(50) NOT NULL,
	pizza_ingredients TEXT NOT NULL,
	pizza_name VARCHAR(100) NOT NULL,
	unit_price NUMERIC(6, 2) NOT NULL
)

-- Tạo bảng Orders (Đơn hàng)
CREATE TABLE orders (
	order_id INT PRIMARY KEY,
	order_date DATE NOT NULL,
    order_time TIME NOT NULL
)

-- Tạo bảng Orders_Details 
CREATE TABLE orders_details (
	pizza_id INT PRIMARY KEY,
	order_id INT NOT NULL,
    pizza_name_id VARCHAR(50) NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    total_price NUMERIC(6, 2) NOT NULL,

	CONSTRAINT fk_order FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    CONSTRAINT fk_pizza FOREIGN KEY (pizza_name_id) REFERENCES pizzas(pizza_name_id) ON DELETE CASCADE
)
