CREATE TABLE Caregivers (
    Username varchar(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
);

CREATE TABLE Vaccines (
    Name varchar(255),
    Doses int,
    PRIMARY KEY (Name)
);
CREATE TABLE Patients (
	Username varchar(225),
	Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
);