CREATE TABLE `department` (
  department_id int NOT NULL PRIMARY KEY ,
  department_name varchar(45) NOT NULL
);

CREATE TABLE `student` (
  `student_number` char(8) NOT NULL PRIMARY KEY ,
  `surname` varchar(100) NOT NULL,
  `other_names` varchar(100) NOT NULL,
  `date_of_birth` date NOT NULL
);

CREATE TABLE `subject` (
  `subject_id` int NOT NULL PRIMARY KEY,
  `name` varchar(45) NOT NULL,
  `department_id` int NOT NULL,
    FOREIGN KEY (department_id)
        REFERENCES department(department_id)
);

CREATE TABLE `staff` (
  `staff_code` char(3) NOT NULL PRIMARY KEY ,
  `surname` varchar(100) NOT NULL,
  `other_names` varchar(100) NOT NULL,
  `department_id` int NOT NULL,
  FOREIGN KEY (department_id)
      REFERENCES department (department_id)
);

CREATE TABLE `course` (
  `course_id` int NOT NULL PRIMARY KEY ,
  `year` year NOT NULL,
  `subject_id` int NOT NULL,
    FOREIGN KEY (subject_id)
        REFERENCES subject (subject_id)
);

CREATE TABLE `enrolment` (
  `student_number` char(8),
  `class_id` int NOT NULL,
    PRIMARY KEY (student_number, class_id),
    FOREIGN KEY (student_number)
        REFERENCES student(student_number),
    FOREIGN KEY (class_id)
        REFERENCES class(class_id)
);

CREATE TABLE `class` (
  `class_id` int NOT NULL PRIMARY KEY ,
  `block` char(1) NOT NULL,
  `course_id` int NOT NULL,
    FOREIGN KEY (course_id)
        REFERENCES course (course_id)
);

CREATE TABLE `staff_login` (
  `staff_code` char(3) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`staff_code`),
  CONSTRAINT `staff_login_fk1` FOREIGN KEY (`staff_code`) REFERENCES `staff` (`staff_code`)
);

CREATE TABLE `student_login` (
  `student_number` char(8) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`student_number`),
  CONSTRAINT `student_login_fk1` FOREIGN KEY (`student_number`) REFERENCES `student` (`student_number`)
);

CREATE TABLE `teaching` (
  `staff_code` char(3) NOT NULL,
  `class_id` int NOT NULL,
  PRIMARY KEY (`staff_code`,`class_id`),
  CONSTRAINT `teaching_fk1` FOREIGN KEY (`staff_code`) REFERENCES `staff` (`staff_code`),
  CONSTRAINT `teaching_fk2` FOREIGN KEY (`class_id`) REFERENCES `class` (`class_id`)
);

CREATE TABLE `assessment` (
  assessment_id int NOT NULL,
  subject_id int NOT NULL,
  total_marks int NOT NULL DEFAULT '100',
  grading TEXT CHECK( grading IN ('ABC','DMP') )   NOT NULL DEFAULT 'ABC',
  title varchar(45) NOT NULL DEFAULT 'assessment',
  PRIMARY KEY (`assessment_id`),
  CONSTRAINT `assessment_fk1` FOREIGN KEY (`subject_id`) REFERENCES `subject` (`subject_id`)
);

CREATE TABLE `assessment_set` (
  `assessment_id` int NOT NULL,
  `class_id` int NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`assessment_id`,`class_id`),
  CONSTRAINT `assessment_set_fk1` FOREIGN KEY (`assessment_id`) REFERENCES `assessment` (`assessment_id`),
  CONSTRAINT `assessment_set_fk2` FOREIGN KEY (`class_id`) REFERENCES `class` (`class_id`)
);

CREATE TABLE `assessment_results` (
  `assessment_id` int NOT NULL,
  `student_number` char(8) NOT NULL,
  `marks` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`assessment_id`,`student_number`),
  CONSTRAINT `assessment_results_fk1` FOREIGN KEY (`assessment_id`) REFERENCES `assessment` (`assessment_id`),
  CONSTRAINT `assessment_results_fk2` FOREIGN KEY (`student_number`) REFERENCES `student` (`student_number`)
);
