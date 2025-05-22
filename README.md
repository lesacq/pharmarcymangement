# pharmarcy mangement system


A Python application for managing pharmacy inventory, tracking drug expiration, managing stock, and recording sales.

## Features

- Add, view, and manage medicines in inventory
- Track quantities, expiration dates, and prices
- Process sales and update inventory automatically
- Generate and save sales receipts
- User-friendly GUI built with Tkinter

## Technologies Used

- **Python** for application logic
- **Tkinter** for the graphical user interface
- **MySQL** (via XAMPP) for the database backend

## Setup Instructions

1. **Clone the repository**  

2. **Set up the MySQL database**  
- Use XAMPP or another MySQL server.
- Create a database named `pms`.
- Create the following tables:

```sql
CREATE TABLE inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    quantity INT,
    expiration_date DATE,
    price FLOAT
);

CREATE TABLE sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    medicine_name VARCHAR(255),
    quantity INT,
    total_price FLOAT,
    sale_time DATETIME
);


```



3. Install dependencies
pip install mysql-connector-python

4. Run the application
python [pharmacy.py](http://_vscodecontentref_/0)

![inventory](https://github.com/user-attachments/assets/1566454c-342e-413f-a15c-84a42b7f329b)
![sales](https://github.com/user-attachments/assets/99cc96df-7262-4da2-8752-18a0f963f6f3)
