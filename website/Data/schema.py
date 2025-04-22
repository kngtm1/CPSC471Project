### Run this file to create the database

import sqlite3

# Use raw string to avoid issues with backslashes
connect = sqlite3.connect("website\Data\StoreDB.db")

# Admin Table
connect.execute("""
    CREATE TABLE Admin (
        AdminID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT,
        Email TEXT NOT NULL, 
        Password TEXT
    );
""")

# SuperAdmin Table
connect.execute("""
    CREATE TABLE SuperAdmin (
        AdminID INTEGER PRIMARY KEY AUTOINCREMENT,
        FOREIGN KEY (AdminID) REFERENCES Admin(AdminID)
    );
""")

# Moderator Table
connect.execute("""
    CREATE TABLE Moderator (
        AdminID INTEGER PRIMARY KEY AUTOINCREMENT,
        FOREIGN KEY (AdminID) REFERENCES Admin(AdminID)
    );
""")

# Users Table
connect.execute("""
    CREATE TABLE Users (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT,
        Email TEXT NOT NULL,
        PhoneNumber INTEGER NOT NULL,
        Password TEXT NOT NULL
    );
""")

# Customer Table
connect.execute("""
    CREATE TABLE Customer (
        UserID INTEGER PRIMARY KEY,
        DropoffLocation TEXT NOT NULL,
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    );
""")

# Business Table
connect.execute("""
    CREATE TABLE Business (
        BusinessID INTEGER PRIMARY KEY AUTOINCREMENT,
        BusinessName TEXT NOT NULL,
        Description TEXT,
        Category TEXT
    );
""")

# BusinessOwner Table
connect.execute("""
    CREATE TABLE BusinessOwner (
        UserID INTEGER PRIMARY KEY,
        PickupLocation TEXT NOT NULL,
        AdminID INTEGER,
        BusinessID INTEGER,
        FOREIGN KEY (UserID) REFERENCES Users(UserID),
        FOREIGN KEY (AdminID) REFERENCES Admin(AdminID),
        FOREIGN KEY (BusinessID) REFERENCES Business(BusinessID)
    );
""")

# Product Table
connect.execute("""
    CREATE TABLE Product (
        BusinessID INTEGER,
        ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Category TEXT NOT NULL,
        Description TEXT NOT NULL,
        Price INTEGER NOT NULL, 
        Stock INTEGER NOT NULL,
        FOREIGN KEY (BusinessID) REFERENCES Business(BusinessID)

    );
""")

# Orders Table
connect.execute("""
    CREATE TABLE Orders (
        OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
        OrderDate TEXT NOT NULL,
        OrderTotal INTEGER NOT NULL,
        AdminID INTEGER,
        UserID INTEGER,
        Status TEXT,
        FOREIGN KEY (AdminID) REFERENCES Admin(AdminID),
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    );
""")

# OrderItem Table
connect.execute("""
    CREATE TABLE OrderItem (
        OrderID INTEGER,
    ProductID INTEGER,
    Quantity INTEGER NOT NULL,
    PRIMARY KEY (OrderID, ProductID),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
    );
""")

# Warehouse Table
connect.execute("""
    CREATE TABLE Warehouse (
        WarehouseID INTEGER PRIMARY KEY AUTOINCREMENT,
        Location TEXT
    );
""")

# Drone Table
connect.execute("""
    CREATE TABLE Drone (
        DroneID INTEGER PRIMARY KEY AUTOINCREMENT,
        Route TEXT NOT NULL,
        BatteryLevel INTEGER NOT NULL,
        Model TEXT NOT NULL,
        ClosestWarehouse TEXT NOT NULL,
        WarehouseID INTEGER,
        Status TEXT,
        FOREIGN KEY (WarehouseID) REFERENCES Warehouse(WarehouseID)
    );
""")

# Delivery Table
connect.execute("""
    CREATE TABLE Delivery (
        DeliveryID INTEGER PRIMARY KEY AUTOINCREMENT,
        DestinationAddress TEXT NOT NULL,
        EstimatedDeliveryTime TEXT NOT NULL,
        DroneID INTEGER,
        OrderID INTEGER,
        Status TEXT,
        FOREIGN KEY (DroneID) REFERENCES Drone(DroneID),
        FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
    );
""")

# Manages Table
connect.execute("""
    CREATE TABLE Manages (
        AdminID INTEGER,
        UserID INTEGER,
        PRIMARY KEY (AdminID, UserID),
        FOREIGN KEY (AdminID) REFERENCES Admin(AdminID),
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    );
""")

connect.commit()
connect.close()
