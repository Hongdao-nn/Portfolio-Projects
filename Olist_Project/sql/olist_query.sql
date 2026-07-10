-- GIAI ĐOẠN 1: TẠO CÁC BẢNG ĐỘC LẬP (BẢNG GỐC / DIMENSION TABLES)

CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_unique_id VARCHAR(50),
    customer_zip_code_prefix INT,
    customer_city VARCHAR(100),
    customer_state VARCHAR(10)
);

CREATE TABLE sellers (
    seller_id VARCHAR(50) PRIMARY KEY,
    seller_zip_code_prefix INT,
    seller_city VARCHAR(100),
    seller_state VARCHAR(10)
);

CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_category_name VARCHAR(100),
    product_name_lenght INT,
    product_description_lenght INT,
    product_photos_qty INT,
    product_weight_g INT,
    product_length_cm INT, 
    product_height_cm INT,
    product_width_cm INT
);

CREATE TABLE product_category_name_translation (
    product_category_name VARCHAR(100) PRIMARY KEY,
    product_category_name_english VARCHAR(100)
);

CREATE TABLE geolocation (
    geolocation_zip_code_prefix INT,
    geolocation_lat NUMERIC(18, 15),
    geolocation_lng NUMERIC(18, 15),
    geolocation_city VARCHAR(100),
    geolocation_state VARCHAR(10)
);

-- GIAI ĐOẠN 2: TẠO CÁC BẢNG PHỤ THUỘC (FACT TABLES / RELATIONSHIP TABLES)

CREATE TABLE orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    order_status VARCHAR(50),
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP,
    CONSTRAINT fk_orders_customers FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_payments (
    order_id VARCHAR(50),
    payment_sequential INT,
    payment_type VARCHAR(50),
    payment_installments INT,
    payment_value NUMERIC(10, 2),   
    CONSTRAINT fk_payments_orders FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE reviews (
    review_id VARCHAR(50),
    order_id VARCHAR(50),
    review_score INT,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP,
    CONSTRAINT fk_reviews_orders FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE order_items (
    order_id VARCHAR(50),
    order_item_id INT, 
    product_id VARCHAR(50),
    seller_id VARCHAR(50),
    shipping_limit_date TIMESTAMP,
    price NUMERIC(10, 2),
    freight_value NUMERIC(10, 2),
    PRIMARY KEY (order_id, order_item_id),
    CONSTRAINT fk_items_orders FOREIGN KEY (order_id) REFERENCES orders(order_id),
    CONSTRAINT fk_items_products FOREIGN KEY (product_id) REFERENCES products(product_id),
    CONSTRAINT fk_items_sellers FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
);

-- GIAI ĐOẠN 3: BÀI TOÁN KINH DOANh
-- Bài toán 1: Xu hướng doanh thu theo tháng và tính lũy kế

WITH order_revenue_aggregated AS (
	SELECT 
		order_id, 
		SUM(payment_value) AS total_order_payment 
	FROM order_payments
	GROUP BY order_id
),
monthly_revenue AS (
    SELECT 
        DATE_TRUNC('month', o.order_purchase_timestamp) AS month,
        SUM(r.total_order_payment) AS total_revenue
    FROM orders o
    JOIN order_revenue_aggregated r ON o.order_id = r.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY DATE_TRUNC('month', o.order_purchase_timestamp)
)
SELECT 
    month,
    total_revenue,
    SUM(total_revenue) OVER (ORDER BY month) AS cumulative_revenue
FROM monthly_revenue
ORDER BY month;

-- Bài toán 2: Phân khúc khách hàng

WITH customer_order_payments AS (
    SELECT 
        order_id,
        SUM(payment_value) AS total_order_amount
    FROM order_payments
    GROUP BY order_id
),
customer_rfm_raw AS (
    SELECT 
        c.customer_unique_id,
        -- Recency: Lấy ngày gần đây nhất trong DB trừ đi ngày mua hàng cuối cùng của khách
        (SELECT MAX(order_purchase_timestamp) FROM orders) - MAX(o.order_purchase_timestamp) AS recency_interval,
        -- Frequency: Đếm số đơn hàng độc lập mà khách đã mua và được giao thành công
        COUNT(DISTINCT o.order_id) AS frequency,
        -- Monetary: Tổng số tiền khách đã chi trả cho các đơn hàng thành công
        SUM(p.total_order_amount) AS monetary
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN customer_order_payments p ON o.order_id = p.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
)
SELECT 
    customer_unique_id,
    EXTRACT(DAY FROM recency_interval) AS recency_days, -- Chuyển kiểu Interval thành số ngày integer
    frequency,
    monetary
FROM customer_rfm_raw
ORDER BY frequency DESC, monetary DESC;

-- Bài toán 3: Phân tích giao hàng trễ và ảnh hưởng đến điểm đánh giá

WITH delivery_performance AS (
	SELECT 
        o.order_id,
        o.order_delivered_customer_date,
        o.order_estimated_delivery_date,
		CASE 
            WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 'Late'
            ELSE 'On Time'
        END AS delivery_status,
		CASE 
            WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date 
            THEN EXTRACT(DAY FROM (o.order_delivered_customer_date - o.order_estimated_delivery_date))
            ELSE 0
        END AS days_late,
		r.review_score
    FROM orders o
    JOIN reviews r ON o.order_id = r.order_id
    WHERE o.order_status = 'delivered' 
      AND o.order_delivered_customer_date IS NOT NULL
)
SELECT 
    delivery_status,
    COUNT(order_id) AS total_orders,
    ROUND(AVG(review_score), 2) AS avg_review_score,
    ROUND(AVG(days_late), 1) AS avg_days_late
FROM delivery_performance
GROUP BY delivery_status;

-- Bài toán 4: Phân tích danh mục sản phẩm

WITH product_revenue AS (
    SELECT 
        oi.product_id,
        COUNT(oi.order_id) AS total_units_sold,
        SUM(oi.price) AS total_revenue
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.order_status = 'delivered' 
    GROUP BY oi.product_id
),
category_summary AS (
    SELECT 
        COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS category_name,
        SUM(pr.total_units_sold) AS units_sold,
        SUM(pr.total_revenue) AS revenue,
        ROUND(AVG(r.review_score), 2) AS avg_review_score
    FROM products p
    JOIN product_revenue pr ON p.product_id = pr.product_id
    LEFT JOIN product_category_name_translation t ON p.product_category_name = t.product_category_name
    LEFT JOIN order_items oi ON p.product_id = oi.product_id
    LEFT JOIN reviews r ON oi.order_id = r.order_id
    GROUP BY COALESCE(t.product_category_name_english, p.product_category_name, 'unknown')
)
SELECT 
    category_name,
    units_sold,
    ROUND(revenue, 2) AS total_revenue,
    avg_review_score
FROM category_summary
ORDER BY total_revenue DESC
LIMIT 10;

-- Bài toán 5: Tỷ lệ giữ chân khách hàng

WITH customer_first_purchase AS (
    SELECT 
        c.customer_unique_id,
        DATE_TRUNC('month', MIN(o.order_purchase_timestamp)) AS cohort_month
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
),
order_months AS (
    SELECT DISTINCT
        c.customer_unique_id,
        DATE_TRUNC('month', o.order_purchase_timestamp) AS order_month
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.order_status = 'delivered'
),
cohort_sizes AS (
    SELECT 
        cohort_month,
        COUNT(DISTINCT customer_unique_id) AS total_customers
    FROM customer_first_purchase
    GROUP BY cohort_month
),
retention_table AS (
    SELECT 
        f.cohort_month,
        m.order_month,
        (EXTRACT(YEAR FROM m.order_month) - EXTRACT(YEAR FROM f.cohort_month)) * 12 +
        (EXTRACT(MONTH FROM m.order_month) - EXTRACT(MONTH FROM f.cohort_month)) AS month_index,
        COUNT(DISTINCT m.customer_unique_id) AS retained_customers
    FROM order_months m
    JOIN customer_first_purchase f ON m.customer_unique_id = f.customer_unique_id
    GROUP BY f.cohort_month, m.order_month
)
SELECT 
    r.cohort_month,
    s.total_customers AS cohort_size,
    r.month_index,
    r.retained_customers,
    ROUND((r.retained_customers::NUMERIC / s.total_customers) * 100, 2) AS retention_rate
FROM retention_table r
JOIN cohort_sizes s ON r.cohort_month = s.cohort_month
WHERE r.month_index >= 0 
ORDER BY r.cohort_month, r.month_index;