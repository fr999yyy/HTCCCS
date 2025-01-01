CREATE DATABASE htcccs;
USE htcccs;
DROP DATABASE htcccs;

CREATE TABLE Students (
    stdID INT PRIMARY KEY,
    stdName VARCHAR(10) NOT NULL,
    team INT NOT NULL,
    satb ENUM('S', 'A', 'T', 'B') NOT NULL,
    JorH ENUM('J', 'H') NOT NULL,
    stdTag VARCHAR(15)
);

CREATE TABLE Volunteers (
    volunteerID INT AUTO_INCREMENT PRIMARY KEY,
    campName VARCHAR(15),
    profilePic VARCHAR(255) -- Path to the profile picture
);

CREATE TABLE Sections (
    sectionID INT AUTO_INCREMENT PRIMARY KEY,
	sectionTime VARCHAR(30)
);

CREATE TABLE Courses (
    courseID INT AUTO_INCREMENT PRIMARY KEY,
    courseName VARCHAR(50) NOT NULL,
    courseInfo VARCHAR(255),
    stdLimit INT,
    courseType VARCHAR(1) NOT NULL,
    sectionId INT NOT NULL,
    FOREIGN KEY (sectionID) REFERENCES Sections(sectionID)
);

CREATE TABLE CourseVolunteers (
    courseID INT NOT NULL,
    volunteerID INT NOT NULL,
    PRIMARY KEY (courseID, volunteerID),
    FOREIGN KEY (courseID) REFERENCES Courses(courseID) ON DELETE CASCADE,
    FOREIGN KEY (volunteerID) REFERENCES Volunteers(volunteerID) ON DELETE CASCADE
);

CREATE TABLE Forms (
    formID INT AUTO_INCREMENT PRIMARY KEY,
    formType ENUM('J1', 'H1', 'J2', 'H2') NOT NULL,
    userType ENUM('J', 'H') NOT NULL,
    sectionID INT NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sectionID) REFERENCES Sections(sectionID)
);

CREATE TABLE Selections (
    selectionID INT AUTO_INCREMENT PRIMARY KEY,
    stdID INT NOT NULL,
    courseID INT NOT NULL,
    priorityOrder INT NOT NULL,
    formID INT NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
    FOREIGN KEY (FormID) REFERENCES Forms(FormID)
);

CREATE TABLE AdminSettings (
    settingName VARCHAR(50) PRIMARY KEY,
    configure VARCHAR(50)
);

SELECT -- 連結courses & volunteers
    Courses.courseID, 
    Courses.courseName, 
    Courses.courseInfo,
    Courses.sectionNumber, 
    Volunteers.campName, 
	Volunteers.profilePic
FROM 
    Courses
INNER JOIN 
    Volunteers 
ON 
    Courses.volunteerID = Voulunteers.volunteerID;


SELECT -- 選課結果 tbd 
    S.sectionNumber, 
    S.priorityOrder, 
    C.courseName, 
    V.campName, 
    V.profilePic 
FROM 
    Selections S
JOIN 
    Courses C ON S.courseID = C.courseID
JOIN 
    Volunteers V ON C.voulunteerID = V.voulunteerID
WHERE 
    S.UserID = 1
ORDER BY 
    S.sectionNumber, S.priorityOrder;

