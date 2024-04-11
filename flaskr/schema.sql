DROP TABLE IF EXISTS subject;
DROP TABLE IF EXISTS teacher;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS course_subject;
DROP TABLE IF EXISTS batch;
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS attendance_student;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  role TEXT NOT NULL
);

CREATE TABLE course(
    id integer primary key AUTOINCREMENT,
    course_name text not null
);
CREATE TABLE teacher(
    id integer primary key AUTOINCREMENT,
    first_name text not null,
    last_name text not null,
    email text not null,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
);
CREATE TABLE subject(
    id integer primary key AUTOINCREMENT,
    subject_name text not null,
    subject_code text not null,
    teacher_id INTEGER NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES teacher (id)

);
CREATE TABLE course_subject(
    id integer primary key AUTOINCREMENT,
    course_id INTEGER not null,
    subject_id INTEGER NOT NULL,
    FOREIGN KEY (course_id) REFERENCES course (id),
    FOREIGN KEY (subject_id) REFERENCES subject (id)
);
CREATE TABLE batch(
    id integer primary key AUTOINCREMENT,
    batch_year text not null,
    batch_intake text NOT NULL,
    batch_name text NOT NULL
);

CREATE TABLE student(
    id integer primary key AUTOINCREMENT,
    first_name text not null,
    last_name text not null,
    email text NOT NULL,
    image text NOT NULL,
    batch_id INTEGER not null,
    course_id INTEGER NOT NULL,
    FOREIGN KEY (course_id) REFERENCES course (id),
    FOREIGN KEY (batch_id) REFERENCES batch (id)
);

CREATE TABLE attendance(
    id integer primary key AUTOINCREMENT,
    batch_id INTEGER not null,
    course_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    attendance_date text NOT NULL,
    user_id INTEGER NOT NULL,
    type text NOT NULL,
    FOREIGN KEY (batch_id) REFERENCES batch (id),
    FOREIGN KEY (course_id) REFERENCES course (id),
    FOREIGN KEY (subject_id) REFERENCES subject (id)
);
CREATE TABLE attendance_student(
    id integer primary key AUTOINCREMENT,
    attendance_id INTEGER not null,
    student_id INTEGER NOT NULL,
    status INTEGER NOT NULL,
    FOREIGN KEY (attendance_id) REFERENCES attendance (id),
    FOREIGN KEY (student_id) REFERENCES student (id)
);
INSERT INTO course (course_name) VALUES
('Computer and Information Sciences'),
('AWS Cloud Architect'),
('Program and Project Management');
INSERT INTO batch (batch_year, batch_intake, batch_name) VALUES
('2024', 'fall', 'Batch A'),
('2024', 'spring', 'Batch B');

INSERT INTO user (username,role, password)
VALUES 
    ('admin@yopmail.com','admin', 'scrypt:32768:8:1$psZiWG3OIZxrS1jC$c1a335941efd2187bbef3a98894d7abf6e740d0d33a078a9b9e6b38d6ce1c41a5f17f7017733ad7532778c2d510985949d052a4e7b8117b627fc0f805781ac17'),
    ('emily.johnson@yopmail.com','teacher', 'scrypt:32768:8:1$psZiWG3OIZxrS1jC$c1a335941efd2187bbef3a98894d7abf6e740d0d33a078a9b9e6b38d6ce1c41a5f17f7017733ad7532778c2d510985949d052a4e7b8117b627fc0f805781ac17'),
    ('michael.thompson@yopmail.com','teacher', 'scrypt:32768:8:1$psZiWG3OIZxrS1jC$c1a335941efd2187bbef3a98894d7abf6e740d0d33a078a9b9e6b38d6ce1c41a5f17f7017733ad7532778c2d510985949d052a4e7b8117b627fc0f805781ac17'),
    ('sarah.davis@yopmail.com','teacher', 'scrypt:32768:8:1$psZiWG3OIZxrS1jC$c1a335941efd2187bbef3a98894d7abf6e740d0d33a078a9b9e6b38d6ce1c41a5f17f7017733ad7532778c2d510985949d052a4e7b8117b627fc0f805781ac17'),
    ('john.rodriguez@yopmail.com','teacher', 'scrypt:32768:8:1$psZiWG3OIZxrS1jC$c1a335941efd2187bbef3a98894d7abf6e740d0d33a078a9b9e6b38d6ce1c41a5f17f7017733ad7532778c2d510985949d052a4e7b8117b627fc0f805781ac17');

Insert into teacher(first_name,last_name,email,user_id) values 
('Emily', 'Johnson', 'emily.johnson@yopmail.com',2),
    ('Michael', 'Thompson', 'michael.thompson@yopmail.com',3),
    ('Sarah', 'Davis', 'sarah.davis@yopmail.com',4),
    ('John', 'Rodriguez', 'john.rodriguez@yopmail.com',5);

INSERT INTO subject (subject_name, subject_code, teacher_id) VALUES
    ('Mathematics', 'MATH101', 1),
    ('Physics', 'PHYS102', 2),
    ('Biology', 'BIOL103', 3),
    ('History', 'HIST104', 4);
INSERT INTO course_subject (course_id, subject_id) VALUES
(1,1),
(1,2),
(1,3),
(2,4),
(2,1),
(2,2),
(2,3),
(2,4),
(3,1),
(3,2),
(3,3),
(3,4);
INSERT INTO student (first_name, last_name, email,batch_id,course_id,image) VALUES
    ('John', 'Doe', 'john.doe@yopmail.com',1,1,'/img/profile/defaults.jpg'),
    ('Jane', 'Smith', 'jane.smith@yopmail.com',1,1,'/img/profile/defaults.jpg'),
    ('Michael', 'Johnson', 'michael.johnson@yopmail.com',1,1,'/static/img/profile/defaults.jpg'),
    ('Emily', 'Brown', 'emily.brown@yopmail.com',1,1,'/img/profile/defaults.jpg'),
    ('David', 'Williams', 'david.williams@yopmail.com',1,1,'/img/profile/defaults.jpg'),
    ('Sarah', 'Jones', 'sarah.jones@yopmail.com',1,1,'/img/profile/defaults.jpg'),
    ('Daniel', 'Garcia', 'daniel.garcia@yopmail.com',1,1,'/img/profile/defaults.jpg'),
    ('Jennifer', 'Martinez', 'jennifer.martinez@yopmail.com',1,1,'/img/profile/defaults.jpg'),
    ('James', 'Hernandez', 'james.hernandez@yopmail.com',1,1,'/img/profile/defaults.jpg'),
    ('Jessica', 'Lopez', 'jessica.lopez@yopmail.com',1,1,'/img/profile/defaults.jpg');