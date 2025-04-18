import sqlite3

# Connect to the existing database
connect = sqlite3.connect("website/Data/StoreDB.db")
cursor = connect.cursor()

# Insert Admins
cursor.execute("INSERT OR IGNORE INTO Admin (AdminID, Name, Email) VALUES (1, 'Alice Admin', 'alice@admin.com')")
cursor.execute("INSERT OR IGNORE INTO Admin (AdminID, Name, Email) VALUES (2, 'Bob Boss', 'bob@admin.com')")

# Insert SuperAdmin and Moderator
cursor.execute("INSERT OR IGNORE INTO SuperAdmin (AdminID) VALUES (1)")
cursor.execute("INSERT OR IGNORE INTO Moderator (AdminID) VALUES (2)")

# Insert Users
cursor.execute("INSERT OR IGNORE INTO Users (UserID, Name, Email, PhoneNumber, Password) VALUES (1, 'Charlie Customer', 'c@example.com', 1234567890, 'c')")
cursor.execute("INSERT OR IGNORE INTO Users (UserID, Name, Email, PhoneNumber, Password) VALUES (2, 'Brenda Business', 'b@shop.com', 9876543210, 'b')")


# Insert Customer and BusinessOwner
cursor.execute("INSERT OR IGNORE INTO Customer (UserID, DropoffLocation) VALUES (1, '123 Maple Street')")
cursor.execute("INSERT OR IGNORE INTO Business (BusinessID, BusinessName, Description, Category) VALUES (1, 'Brenda Tech Shop', 'Local Goods', 'Stuff')")
cursor.execute("INSERT OR IGNORE INTO BusinessOwner (UserID, PickupLocation, AdminID, BusinessID) VALUES (2, '456 Elm Avenue', 2, 1)")


# Insert Product
cursor.execute("INSERT OR IGNORE INTO Product (BusinessID, Name, Category, Description, Price, Stock) VALUES (1, 'Eco-Friendly Water Bottle', 'Home & Kitchen', 'Reusable 750ml bottle made of stainless steel.', 1999, 150);")
cursor.execute("INSERT OR IGNORE INTO Product (BusinessID, Name, Category, Description, Price, Stock) VALUES (1, 'Wireless Earbuds', 'Electronics', 'Bluetooth 5.0 earbuds with noise cancellation.', 5999, 75)")
cursor.execute("INSERT OR IGNORE INTO Product (BusinessID, Name, Category, Description, Price, Stock) VALUES (2, 'Business 2 Smart LED Light Bulb', 'Home & Lighting', 'Color-changing bulb with remote app control.', 1449, 200)")


# Insert Order
cursor.execute("INSERT OR IGNORE INTO Orders (OrderID, OrderDate, OrderTotal, AdminID, UserID, Status) VALUES (1, '2025-04-16', 39, 2, 1, 'Processing')")

# Insert OrderItem
cursor.execute("INSERT OR IGNORE INTO OrderItem (OrderID, Quantity) VALUES (1, 2)")

# Insert Warehouse
cursor.execute("INSERT OR IGNORE INTO Warehouse (WarehouseID, Location) VALUES (1, 'Central Depot')")

# Insert Drone
cursor.execute("INSERT OR IGNORE INTO Drone (DroneID, Route, BatteryLevel, Model, ClosestWarehouse, WarehouseID, Status) VALUES (1, 'Route A', 80, 'FalconX', 'Central Depot', 1, 'Available')")

# Insert Delivery
cursor.execute("INSERT OR IGNORE INTO Delivery (DeliveryID, DestinationAddress, EstimatedDeliveryTime, DroneID, OrderID, Status) VALUES (1, '123 Maple Street', '2025-04-17 15:00', 1, 1, 'In_Transit')")

# Insert Manages
cursor.execute("INSERT OR IGNORE INTO Manages (AdminID, UserID) VALUES (2, 2)")

# Commit and close
connect.commit()
connect.close()
