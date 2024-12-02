-- DROP DATABASE IF EXISTS `evalution_system`;

-- CREATE DATABASE `evalution_system`;
-- USE `evalution_system`;

USE `lab2`;
DROP TABLE IF EXISTS `CLASS_STUDENT`;
DROP TABLE IF EXISTS `EVALUTION`; 
-- DROP TABLE IF EXISTS `EMOJI`;
DROP TABLE IF EXISTS `CLASS_INFO`;
DROP TABLE IF EXISTS `USER_STUDENT`;
DROP TABLE IF EXISTS `USER_TEACHER`;
DROP TABLE IF EXISTS `USER_ADMIN`;

-- CREATE TABLE `EMOJI` (
--   `EMOJI_ID` int(11) NOT NULL AUTO_INCREMENT,
--   `EMOJI_NAME` varchar(255) NOT NULL,
--   `EMOJI_CODE` varchar(255) NOT NULL,
--   PRIMARY KEY (`EMOJI_ID`),
--   UNIQUE KEY `EMOJI_CODE_UNIQUE` (`EMOJI_CODE`)
-- ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `USER_STUDENT` (
  `STUDENT_ID` int(11) NOT NULL AUTO_INCREMENT,
  `STUDENT_NAME` varchar(255) NOT NULL,
  `STUDENT_PASSWORD` varchar(255) NOT NULL,
  PRIMARY KEY (`STUDENT_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `USER_TEACHER` (
  `TEACHER_ID` int(11) NOT NULL AUTO_INCREMENT,
  `TEACHER_NAME` varchar(255) NOT NULL,
  `TEACHER_PASSWORD` varchar(255) NOT NULL,
  PRIMARY KEY (`TEACHER_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `USER_ADMIN` (
  `ADMIN_ID` int(11) NOT NULL AUTO_INCREMENT,
  `ADMIN_NAME` varchar(255) NOT NULL,
  `ADMIN_PASSWORD` varchar(255) NOT NULL,
  PRIMARY KEY (`ADMIN_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `CLASS_INFO` (
  `CLASS_ID` int(11) NOT NULL AUTO_INCREMENT,
  `CLASS_NAME` varchar(255) NOT NULL,
  `CLASS_TEACHER_ID` int(11) NOT NULL,
  PRIMARY KEY (`CLASS_ID`),
  FOREIGN KEY (`CLASS_TEACHER_ID`) REFERENCES `USER_TEACHER`(`TEACHER_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `EVALUTION` (
  `EVALUTION_ID` int(11) NOT NULL AUTO_INCREMENT,
  `STUDENT_ID` int(11) NOT NULL,
  `CLASS_ID` int(11) NOT NULL,
  `EMOJI_CODE` varchar(255) NOT NULL,
  `EVALUTION_DATE` datetime NOT NULL,
  PRIMARY KEY (`EVALUTION_ID`),
  FOREIGN KEY (`STUDENT_ID`) REFERENCES `USER_STUDENT`(`STUDENT_ID`),
  FOREIGN KEY (`CLASS_ID`) REFERENCES `CLASS_INFO`(`CLASS_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `CLASS_STUDENT` (
  `CLASS_STUDENT_ID` int(11) NOT NULL AUTO_INCREMENT,
  `CLASS_ID` int(11) NOT NULL,
  `STUDENT_ID` int(11) NOT NULL,
  PRIMARY KEY (`CLASS_STUDENT_ID`),
  FOREIGN KEY (`CLASS_ID`) REFERENCES `CLASS_INFO`(`CLASS_ID`),
  FOREIGN KEY (`STUDENT_ID`) REFERENCES `USER_STUDENT`(`STUDENT_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- INSERT INTO `EMOJI` (`EMOJI_NAME`, `EMOJI_CODE`) VALUES ('grinning face', 'U+1F600');
-- INSERT INTO `EMOJI` (`EMOJI_NAME`, `EMOJI_CODE`) VALUES ('grinning face with big eyes', 'U+1F603');
-- INSERT INTO `EMOJI` (`EMOJI_NAME`, `EMOJI_CODE`) VALUES ('smiling face with heart-eyes', 'U+1F60D');

INSERT INTO `USER_STUDENT` (`STUDENT_NAME`, `STUDENT_PASSWORD`) VALUES ('Leo', '123456');

INSERT INTO `USER_TEACHER` (`TEACHER_NAME`, `TEACHER_PASSWORD`) VALUES ('Sayaka', '123456');

INSERT INTO `CLASS_INFO` (`CLASS_NAME`, `CLASS_TEACHER_ID`) VALUES ('Maj', 1);
INSERT INTO `CLASS_INFO` (`CLASS_NAME`, `CLASS_TEACHER_ID`) VALUES ('Elden Ring', 1);

INSERT INTO `USER_ADMIN` (`ADMIN_NAME`, `ADMIN_PASSWORD`) VALUES ('Admin', '123456');

INSERT INTO `EVALUTION` (`STUDENT_ID`, `CLASS_ID`, `EMOJI_CODE`, `EVALUTION_DATE`) VALUES (1, 1, 'U+1F60D', '2020-01-01 00:00:00');

INSERT INTO `CLASS_STUDENT` (`CLASS_ID`, `STUDENT_ID`) VALUES (1, 1);
INSERT INTO `CLASS_STUDENT` (`CLASS_ID`, `STUDENT_ID`) VALUES (2, 1);
