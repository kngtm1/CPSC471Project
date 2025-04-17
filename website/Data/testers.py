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
cursor.execute("INSERT OR IGNORE INTO Users (UserID, Name, Email, PhoneNumber) VALUES (1, 'Charlie Customer', 'charlie@example.com', 1234567890)")
cursor.execute("INSERT OR IGNORE INTO Users (UserID, Name, Email, PhoneNumber) VALUES (2, 'Brenda Business', 'brenda@shop.com', 9876543210)")

# Insert Customer and BusinessOwner
cursor.execute("INSERT OR IGNORE INTO Customer (UserID, DropoffLocation) VALUES (1, '123 Maple Street')")
cursor.execute("INSERT OR IGNORE INTO Business (BusinessID, BusinessName, Description, Category) VALUES (1, 'Brenda Boutique', 'Fashionable local shop', 'Clothing')")
cursor.execute("INSERT OR IGNORE INTO BusinessOwner (UserID, PickupLocation, AdminID, BusinessID) VALUES (2, '456 Elm Avenue', 2, 1)")

# Insert Product
cursor.execute("INSERT OR IGNORE INTO Product (ProductID, Names, RegistrationDate, Description, AdminID, UserID, Price) VALUES (1, 'Stylish Shirt', '2025-04-16', 'A trendy cotton shirt', 2, 2, 80)")

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
