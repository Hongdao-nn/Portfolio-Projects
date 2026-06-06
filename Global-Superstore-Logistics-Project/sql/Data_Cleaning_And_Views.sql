-- Overview the dataset
SELECT COUNT (*) as Number_of_row FROM dbo.sales_orders;
SELECT TOP 10 * FROM dbo.sales_orders;

-- Check for NULLs in critical columns
SELECT 
	COUNT (CASE WHEN Customer_ID IS NULL THEN 1 END) AS null_customer_ID,
	COUNT (CASE WHEN Customer_Name IS NULL THEN 1 END) AS null_customer_name,
	COUNT (CASE WHEN Order_ID IS NULL THEN 1 END) AS null_order_ID,
	COUNT (CASE WHEN Order_Date IS NULL THEN 1 END) AS null_order_date,
	COUNT (CASE WHEN Ship_Date IS NULL THEN 1 END) AS null_ship_date,
	COUNT (CASE WHEN Profit IS NULL THEN 1 END) AS null_profit,
	COUNT (CASE WHEN Quantity IS NULL THEN 1 END) AS null_quantity,
	COUNT (CASE WHEN Sales IS NULL THEN 1 END) AS null_sales,
	COUNT (CASE WHEN Shipping_Cost IS NULL THEN 1 END) AS null_shipping_cost,
	COUNT (CASE WHEN Order_Priority IS NULL THEN 1 END) AS null_priority,
    COUNT (CASE WHEN Ship_Mode IS NULL THEN 1 END) AS null_ship_mode,
    COUNT (CASE WHEN Discount IS NULL THEN 1 END) AS null_discount,
    COUNT (CASE WHEN Sub_Category IS NULL THEN 1 END) AS null_sub_category,
    COUNT (CASE WHEN Segment IS NULL THEN 1 END) AS null_segment
FROM dbo.sales_orders;

-- Check the date range and geographic scope of the dataset.
SELECT 
	-- Check the time range
	MIN (Order_Date) AS earliest_order,MAX(Order_Date) AS latest_order,
	MIN (Ship_Date) AS earliest_shipping,MAX(Ship_Date) AS latest_shipping,
	-- Check geographic scope and segment
	COUNT (DISTINCT Country) AS total_countries,
	COUNT (DISTINCT Market) AS total_markets,
	COUNT (DISTINCT Category) AS total_categories
FROM dbo.sales_orders;
GO

-- Create a view that keeps only valid transactions
CREATE VIEW clean_sales AS
SELECT 
    -- Group 1: Identifiers & Customer Details
    Customer_ID,
    Customer_Name,
    Segment,             
    Order_ID,
	-- Group 2: Dates
    Order_Date,
    Ship_Date,
	-- Group 3: Logistics & Operations
    Order_Priority,      
    Ship_Mode,
	-- Group 4: Geography & Product Hierarchy
    Country,
    Market,
    Category,
    Sub_Category,        
    -- Group 5: Financial Metrics
    Sales,
    Quantity,            
    Discount,            
    Profit,
    Shipping_Cost
FROM dbo.sales_orders
WHERE 
    -- Ensure the shipping date is on or after the order date.
    Ship_Date >= Order_Date
    -- Eliminate critical data error instances.
    AND Quantity > 0
	AND Sales > 0
    AND Discount >= 0 AND Discount <= 1;
GO

-- Create view to observe the supply chain and logistics
CREATE VIEW logistics_performance AS
SELECT 
    Order_ID,
    Customer_ID,
    Customer_Name,
    Segment,
    Order_Date,
    Ship_Date,
    Order_Priority,
    Ship_Mode,
    Country,
    Market,
    Category,
    Sub_Category,
    Sales,
    Quantity,
    Shipping_Cost,

    -- 1. Calculate the actual number of shipping days
    DATEDIFF (day, Order_Date, Ship_Date) AS Shipping_Lag,
    -- 2. Establish a hypothetical Service Level Agreement (SLA) for each type of transportation.
    -- Same Day: 0 day, First Class: 2 days, Second Class: 4 days, Standard: 6 days
    CASE
        WHEN Ship_Mode = 'Same Day' THEN 0
        WHEN Ship_Mode = 'First Class' THEN 2
        WHEN Ship_Mode = 'Second Class' THEN 2
        ELSE 6
    END AS SLA_Target_Days
FROM clean_sales;
GO 