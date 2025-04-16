CREATE DATABASE ProjectSQL;
Use ProjectSQL;


CREATE TABLE Admin
(
    AdminID int PRIMARY KEY,
    Names varchar(50),
    Email varchar(50) NOT NULL
);


UPDATE Admin
SET AdminID = 1234567890
WHERE AdminID = 0000000000;


UPDATE Admin
SET Email = 'another_example@email.com'
WHERE Email = 'example@email.com';


UPDATE Admin
SET PhoneNumber = 1234567890
WHERE PhoneNumber = 0000000000;


DELETE FROM Admin
WHERE AdminID = 1;


SELECT * FROM Admin;


CREATE TABLE SuperAdmin
(
    AdminID int PRIMARY KEY,
    FOREIGN KEY (AdminID) REFERENCES Admin (AdminID),
);


CREATE TABLE Moderator
(
    AdminID int PRIMARY KEY,
    FOREIGN KEY (AdminID) REFERENCES Admin (AdminID),
);


CREATE TABLE Users
(
    UserID int PRIMARY KEY,
    Names varchar(50),
    Email varchar(50) NOT NULL,
    PhoneNumber int(15) NOT NULL
);


UPDATE Users
SET Email = 'another_example@email.com'
WHERE Email = 'example@email.com';


UPDATE Users
SET PhoneNumber = 1234567890
WHERE PhoneNumber = 0000000000;


UPDATE Users
SET Names = 'Full Name'
WHERE Names = 'First Middle Last';


INSERT INTO Users (UserID, Names, Email, PhoneNumber)
VALUES (1, 'John Doe', 'admin@example.com');


DELETE FROM Users
WHERE UserID=0000000000;


DELETE FROM Users
WHERE Email=example@email.com;


SELECT UserID
FROM Users;


CREATE TABLE Customer
(
    UserID int PRIMARY KEY,
    FOREIGN KEY (UserID) REFERENCES Users (UserID),
    DropoffLocation varchar(225) NOT NULL
);




CREATE TABLE BusinessOwner
(
    UserID int PRIMARY KEY,
    FOREIGN KEY (UserID) REFERENCES Users (UserID),
    PickupLocation varchar(225) NOT NULL,
    AdminID int,
    FOREIGN KEY (AdminID) REFERENCES Admin (AdminID),
    BusinessID int,
    FOREIGN KEY (BusinessID) REFERENCES Business (BusinessID)
);


CREATE TABLE Product
(
    ProductID int PRIMARY KEY,
    Names varchar(50) NOT NULL,
    RegistrationDate int(50) NOT NULL,
    Description varchar(225),
    AdminID int FOREIGN KEY (AdminID) REFERENCES Admin (AdminID),
    UserID int FOREIGN KEY (UserID) REFERENCES Users (UserID)
);


CREATE TABLE Orders
(
    OrderID int PRIMARY KEY,
    OrderDate int(50) NOT NULL,
    OrderTotal int(225) NOT NULL,
    AdminID int,
    FOREIGN KEY (AdminID) REFERENCES Admin (AdminID),
    UserID int,
    FOREIGN KEY (UserID) REFERENCES Users (UserID)
);


INSERT INTO Orders (OrderID, OrderDate, OrderTotal, AdminID, UserID)
VALUES (1, '2025-03-19', 100, 1, 1);


UPDATE Orders
SET OrderTotal = 120
WHERE OrderID = 1;


DELETE FROM Orders
WHERE OrderID = 1;


SELECT * FROM Orders;


CREATE TABLE Sending
(
    OrderID int PRIMARY KEY,
    FOREIGN KEY (OrderID) REFERENCES Orders (OrderID)
);


CREATE TABLE Processing
(
    OrderID int PRIMARY KEY,
    FOREIGN KEY (OrderID) REFERENCES Orders (OrderID)
);


CREATE TABLE Delivered
(
    OrderID int PRIMARY KEY,
    FOREIGN KEY (OrderID) REFERENCES Orders (OrderID)
);


CREATE TABLE OrderItem
(
    OrderID int PRIMARY KEY,
    FOREIGN KEY (OrderID) REFERENCES Orders (OrderID),
    Quantity int NOT NULL
);


CREATE TABLE Delivery
(
    DeliveryID int PRIMARY KEY,
    DestinationAddress varchar NOT NULL,
    EstimatedDeliveryTime varchar NOT NULL,
    DroneID int,
    FOREIGN KEY (DroneID) REFERENCES Drone (DroneID),
    OrderID int,
    FOREIGN KEY (OrderID) REFERENCES Orders (OrderID)
);


CREATE TABLE Pending
(
    DeliveryID int PRIMARY KEY,
    FOREIGN KEY (DeliveryID) REFERENCES Delivery (DeliveryID)
);


CREATE TABLE In_Transit
(
    DeliveryID int PRIMARY KEY,
    FOREIGN KEY (DeliveryID) REFERENCES Delivery (DeliveryID)
);


CREATE TABLE Delivered
(
    DeliveryID int PRIMARY KEY,
    FOREIGN KEY (DeliveryID) REFERENCES Delivery (DeliveryID)
);


CREATE TABLE Warehouse
(
    WarehouseID int PRIMARY KEY,
    Location varchar(225)
);


CREATE TABLE Drone(
    DroneID int PRIMARY KEY,
    Route varchar(225) NOT NULL,
    BatteryLevel int(100) NOT NULL,
    Model varchar(225) NOT NULL,
    ClosestWarehouse varchar(225) NOT NULL,
    WarehouseID int,
    FOREIGN KEY (WarehouseID) REFERENCES Warehouse (WarehouseID)
);


INSERT INTO Drone (DroneID, Route, BatteryLevel, Model, ClosestWarehouse, WarehouseID)
VALUES (1, 'Route A', 1, 'Bigly', 'Warehouse X', 1);


UPDATE Drone
SET BatteryLevel = 90
WHERE DroneID = 1;


DELETE FROM Drone
WHERE DroneID = 1;


SELECT * FROM Drone;


CREATE TABLE Available
(
    DroneID int PRIMARY KEY,
    FOREIGN KEY (DroneID) REFERENCES Drone (DroneID),
);


CREATE TABLE In_Transit
(
    DroneID int PRIMARY KEY,
    FOREIGN KEY (DroneID) REFERENCES Drone (DroneID),
);


CREATE TABLE In_Maintenance
(
    DroneID int PRIMARY KEY,
    FOREIGN KEY (DroneID) REFERENCES Drone (DroneID),
);


CREATE TABLE Manages
(
    AdminID int,
    FOREIGN KEY (AdminID) REFERENCES Admin (AdminID),
    UserID int,
    FOREIGN KEY (UserID) REFERENCES Users (UserID),
    PRIMARY KEY(AdminID, UserID)
);
