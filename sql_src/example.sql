use lab2;
drop table if exists borrow_list;
drop table if exists reserve_list;
drop table if exists punish_list;
drop table if exists dis_head;
drop table if exists elder_list;
drop table if exists disciple_list;
drop table if exists book_list;

DROP PROCEDURE IF EXISTS ExpelDisciple;
DROP procedure IF exists ReserveBook;
DROP TRIGGER IF EXISTS insert_dis_head;
DROP FUNCTION IF EXISTS CountActiveDisciples;

CREATE TABLE `disciple_list` (
  `disciple_id` int  NOT NULL AUTO_INCREMENT,
  `disciple_name` varchar(45) DEFAULT NULL,
  `disciple_age` int DEFAULT NULL,
  `disciple_level` int DEFAULT NULL,
  `disciple_faction` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`disciple_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '弟子列表,记录弟子的id,名称,修为,派系';

CREATE TABLE `dis_head` (
  `disid` int NOT NULL AUTO_INCREMENT,
  `head_id` varchar(255) DEFAULT '../static/head/1.png',
  PRIMARY KEY (`disid`),
  KEY `head_id_idx` (`head_id`),
  CONSTRAINT `disid` FOREIGN KEY (`disid`) REFERENCES `disciple_list` (`disciple_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '弟子-头像';

CREATE TABLE `book_list` (
  `book_id` int NOT NULL AUTO_INCREMENT,
  `book_name` varchar(45) DEFAULT NULL,
  `book_type` varchar(45) DEFAULT NULL,
  `book_level` int DEFAULT 0,
  `book_status` int DEFAULT 0,
  PRIMARY KEY (`book_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '秘籍列表,包含id,名称,等级,类别,状态';

CREATE TABLE `elder_list` (
  `elder_id` int NOT NULL,
  `elder_name` varchar(45) NOT NULL,
  `elder_age` int DEFAULT NULL,
  `elder_faction` varchar(45) DEFAULT NULL,
  `elder_level` int DEFAULT NULL,
  PRIMARY KEY (`elder_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '长老列表,包含id,名称,年龄,修为,派系';

CREATE TABLE `borrow_list` (
  `borrow_list_dis_id` int NOT NULL,
  `borrow_list_book_id` int NOT NULL,
  `borrow_list_elder_id` int NOT NULL,
  `borrow_list_start_date` DATETIME NOT NULL,
  `borrow_list_end_date` date DEFAULT NULL,
  PRIMARY KEY (
    `borrow_list_dis_id`,
    `borrow_list_book_id`,
    `borrow_list_elder_id`,
    `borrow_list_start_date`
  ),
  KEY `book_id_idx` (`borrow_list_book_id`),
  KEY `elder_id_idx` (`borrow_list_elder_id`),
  CONSTRAINT `book_id` FOREIGN KEY (`borrow_list_book_id`) REFERENCES `book_list` (`book_id`),
  CONSTRAINT `dis_id` FOREIGN KEY (`borrow_list_dis_id`) REFERENCES `disciple_list` (`disciple_id`),
  CONSTRAINT `elder_id` FOREIGN KEY (`borrow_list_elder_id`) REFERENCES `elder_list` (`elder_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '借阅列表,包含弟子id,书籍id,经手长老id,初始借阅时间,归还时间（可以为空,空则表示未归还）';

CREATE TABLE `reserve_list` (
  `reserve_list_dis_id` int NOT NULL,
  `reserve_list_book_id` int NOT NULL,
  `reserve_list_date` DATETIME NOT NULL,
  `reserve_list_res_date` date DEFAULT NULL,
  PRIMARY KEY (
    `reserve_list_dis_id`,
    `reserve_list_book_id`,
    `reserve_list_date`
  ),
  KEY `book_idx` (`reserve_list_book_id`),
  CONSTRAINT `book` FOREIGN KEY (`reserve_list_book_id`) REFERENCES `book_list` (`book_id`),
  CONSTRAINT `dis` FOREIGN KEY (`reserve_list_dis_id`) REFERENCES `disciple_list` (`disciple_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '预约表,包含弟子id,书籍id,预约日期,预计借书日期';

CREATE TABLE `punish_list` (
  `punish_list_dis_id` int NOT NULL,
  `punish_list_elder_id` int NOT NULL,
  `punish_list_startdate` DATETIME NOT NULL,
  `punish_list_enddate` date DEFAULT NULL,
  PRIMARY KEY (
    `punish_list_dis_id`,
    `punish_list_elder_id`,
    `punish_list_startdate`
  ),
  KEY `elder_idx` (`punish_list_elder_id`),
  KEY `elder_p_idx` (`punish_list_elder_id`),
  CONSTRAINT `dis_p` FOREIGN KEY (`punish_list_dis_id`) REFERENCES `disciple_list` (`disciple_id`),
  CONSTRAINT `elder_p` FOREIGN KEY (`punish_list_elder_id`) REFERENCES `elder_list` (`elder_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '惩戒记录,包含弟子id,长老id,惩戒起止日';

INSERT INTO `disciple_list` (`disciple_id`, `disciple_name`, `disciple_age`, `disciple_level`, `disciple_faction`) VALUES 
  (1, '反骨仔',20,80,'移除'),
  (2, '小舞', 19, 78, '魂'),
  (3, '戴沐白', 21, 50, '魂'),
  (4, '朱竹清', 20, 68, '魂'),
  (5, '马红俊', 20, 68, '魂'),
  (6, '奥斯卡', 20, 78, '魂'),
  (7, '宁荣荣', 20, 68, '魂'),
  (8, '唐三', 20, 89, '魂');

INSERT INTO `book_list` (`book_id`, `book_name`, `book_type`, `book_level`, `book_status`) VALUES 
  (1, '焚决', '功法', 0, 0),
  (2, '弄焰决', '功法', 20, 0),
  (3, '大天造化掌', '斗技', 90, 0),
  (4, '青天化龙决', '斗技', 80, 0),
  (5, '八极崩', '斗技', 15, 0),
  (6, '异火亘古尺', '斗技', 100, 0),
  (7, '狮虎碎金吟', '斗技', 20, 0),
  (8, '龙腾九霄', '斗技', 85, 0),
(9, '凤舞九天', '功法', 90, 0),
(10, '天地无极掌', '斗技', 70, 0),
(11, '九阳真经', '功法', 95, 0),
(12, '九阴真经', '功法', 95, 0),
(13, '破虚手', '斗技', 80, 0),
(14, '无影脚', '斗技', 75, 0),
(15, '太极拳', '功法', 65, 0),
(16, '六脉神剑', '斗技', 100, 0),
(17, '神照功', '功法', 85, 0),
(18, '神行百变', '斗技', 70, 0),
(19, '天魔解体', '斗技', 90, 0),
(20, '乾坤大挪移', '功法', 100, 0),
(21, '神魔大侠', '斗技', 80, 0),
(22, '天地人魔', '功法', 75, 0),
(23, '独孤九剑', '斗技', 95, 0),
(24, '神雕侠侣', '功法', 70, 0),
(25, '天龙八部', '斗技', 85, 0),
(26, '笑傲江湖', '功法', 80, 0),
(27, '神雕大侠', '斗技', 75, 0),
(28, '倚天屠龙记', '功法', 90, 0),
(29, '神魔乐章', '斗技', 70, 0),
(30, '天地无极', '功法', 85, 0),
(31, '神魔天尊', '斗技', 80, 0),
(32, '神魔九变', '功法', 75, 0),
(33, '神魔无敌', '斗技', 90, 0),
(34, '神魔之心', '功法', 70, 0),
(35, '神魔之力', '斗技', 85, 0),
(36, '神魔之怒', '功法', 80, 0),
(37, '神魔之翼', '斗技', 75, 0),
(38, '神魔之眼', '功法', 90, 0),
(39, '神魔之手', '斗技', 70, 0),
(40, '神魔之足', '功法', 85, 0),
(41, '神魔之魂', '斗技', 80, 0),
(42, '神魔之体', '功法', 75, 0),
(43, '神魔之血', '斗技', 90, 0),
(44, '神魔之舞', '功法', 70, 0),
(45, '神魔之歌', '斗技', 85, 0),
(46, '神魔之泪', '功法', 80, 0),
(47, '神魔之笑', '斗技', 75, 0),
(48, '神魔之吻', '功法', 90, 0),
(49, '神魔之愿', '斗技', 70, 0),
(50, '神魔之誓', '功法', 85, 0),
(51, '神魔之刃', '斗技', 80, 0),
(52, '神魔之盾', '功法', 75, 0),
(53, '神魔之箭', '斗技', 90, 0),
(54, '神魔之弓', '功法', 70, 0),
(55, '神魔之剑', '斗技', 85, 0),
(56, '神魔之枪', '功法', 80, 0),
(57, '神魔之斧', '斗技', 75, 0),
(58, '神魔之锤', '功法', 90, 0),
(59, '神魔之矛', '斗技', 70, 0),
(60, '神魔之棍', '功法', 85, 0),
(61, '神魔之鞭', '斗技', 80, 0),
(62, '神魔之链', '功法', 75, 0),
(63, '神魔之星', '斗技', 90, 0),
(64, '神魔之月', '功法', 70, 0),
(65, '神魔之日', '斗技', 85, 0),
(66, '神魔之海', '功法', 80, 0),
(67, '神魔之山', '斗技', 75, 0),
(68, '神魔之河', '功法', 90, 0),
(69, '神魔之风', '斗技', 70, 0),
(70, '神魔之火', '功法', 85, 0),
(71, '神魔之水', '斗技', 80, 0),
(72, '神魔之土', '功法', 75, 0),
(73, '神魔之雷', '斗技', 90, 0),
(74, '神魔之雨', '功法', 70, 0),
(75, '神魔之雪', '斗技', 85, 0),
(76, '神魔之霜', '功法', 80, 0),
(77, '神魔之云', '斗技', 75, 0),
(78, '神魔之雾', '功法', 90, 0),
(79, '神魔之露', '斗技', 70, 0),
(80, '神魔之霹雳', '功法', 85, 0),
(81, '神魔之冰', '斗技', 80, 0),
(82, '神魔之烟', '功法', 75, 0),
(83, '神魔之炎', '斗技', 90, 0),
(84, '神魔之光', '功法', 70, 0),
(85, '神魔之暗', '斗技', 85, 0),
(86, '神魔之影', '功法', 80, 0),
(87, '神魔之音', '斗技', 75, 0),
(88, '神魔之静', '功法', 90, 0),
(89, '神魔之动', '斗技', 70, 0),
(90, '神魔之生', '功法', 85, 0),
(91, '神魔之死', '斗技', 80, 0),
(92, '神魔之始', '功法', 75, 0),
(93, '神魔之终', '斗技', 90, 0),
(94, '神魔之空', '功法', 70, 0),
(95, '神魔之实', '斗技', 85, 0),
(96, '神魔之旧', '功法', 80, 0),
(97, '神魔之新', '斗技', 75, 0),
(98, '神魔之快', '功法', 90, 0),
(99, '神魔之慢', '斗技', 70, 0),
(100, '神魔之永', '功法', 85, 0);

INSERT INTO `elder_list` (`elder_id`, `elder_name`, `elder_age`, `elder_faction`, `elder_level`) VALUES 
  (1, '大型反骨仔',99,'移除',999),
  (2, '小舞老师', 59, '魂', 99),
  (3, '戴老头', 61, '魂', 101),
  (4, '朱老头', 60, '魂', 99),
  (5, '马老头', 60, '魂', 99),
  (6, '奥斯卡老师', 60, '魂', 99),
  (7, '宁老头', 60, '魂', 99),
  (8, '唐老头', 60, '魂', 100),
  (9, '药尘',100,'斗',99);

INSERT INTO `borrow_list` (`borrow_list_dis_id`, `borrow_list_book_id`, `borrow_list_elder_id`, `borrow_list_start_date`, `borrow_list_end_date`) VALUES 
  (1, 15, 1, '2020-10-01 00:00:01', NULL),
  (2, 16, 2, '2020-10-01 00:00:01', NULL),
  (3, 17, 3, '2020-10-01 00:00:01', NULL),
  (4, 18, 4, '2020-10-01 00:00:01', NULL),
  (5, 19, 5, '2020-10-01 00:00:01', NULL),
  (6, 20, 6, '2020-10-01 00:00:01', NULL),
  (7, 21, 7, '2020-10-01 00:00:01', NULL);
  

INSERT INTO `reserve_list` (`reserve_list_dis_id`, `reserve_list_book_id`, `reserve_list_date`, `reserve_list_res_date`) VALUES 
  (1, 8, '2020-10-01 00:00:01', '2024-10-15'),
  (2, 9, '2020-10-01 00:00:01', '2024-10-15'),
  (3, 10, '2020-10-01 00:00:01', '2024-10-15'),
  (4, 11, '2020-10-01 00:00:01', '2024-10-15'),
  (5, 12, '2020-10-01 00:00:01', '2024-10-15'),
  (6, 13, '2020-10-01 00:00:01', '2024-10-15'),
  (7, 14, '2020-10-01 00:00:01', '2024-10-15');

INSERT INTO `punish_list` (`punish_list_dis_id`, `punish_list_elder_id`, `punish_list_startdate`, `punish_list_enddate`) VALUES 
  (1, 1, '2020-10-01 00:00:01', '2021-10-15'),
  (2, 2, '2020-10-01 00:00:01', '2021-10-15'),
  (3, 3, '2020-10-01 00:00:01', '2021-10-15'),
  (4, 4, '2020-10-01 00:00:01', '2021-10-15'),
  (5, 5, '2020-10-01 00:00:01', '2021-10-15'),
  (6, 6, '2020-10-01 00:00:01', '2024-10-15'),
  (7, 7, '2020-10-01 00:00:01', '2024-10-15');

INSERT INTO `dis_head` (`disid`, `head_id`) VALUES 
  (1, '../static/head/1.png'),
  (2, '../static/head/2.png'),
  (3, '../static/head/1.png'),
  (4, '../static/head/1.png'),
  (5, '../static/head/1.png'),
  (6, '../static/head/1.png'),
  (7, '../static/head/1.png'),
  (8, '../static/head/1.png');
-- SELECT * FROM reserve_list ;
-- DELETE FROM reserve_list WHERE reserve_list_dis_id = 1 AND reserve_list_book_id = 8;
-- SELECT * FROM reserve_list;

DELIMITER //
CREATE PROCEDURE `ExpelDisciple`(IN dis_id INT)
BEGIN
    UPDATE `disciple_list` SET `disciple_faction` = '移除' WHERE `disciple_id` = dis_id;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER insert_dis_head
AFTER INSERT ON disciple_list
FOR EACH ROW
BEGIN
   INSERT INTO dis_head(disid, head_id) VALUES (NEW.disciple_id, '../static/head/1.png');
END;//
DELIMITER ;

DELIMITER //
CREATE FUNCTION `CountActiveDisciples`()
RETURNS INT
DETERMINISTIC READS SQL DATA
BEGIN
   DECLARE disciple_count INT;
   SELECT COUNT(*) INTO disciple_count FROM `disciple_list` WHERE `disciple_faction` <> '移除';
   RETURN disciple_count;
END;//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE `ReserveBook`(IN book_id INT, IN user_id INT, IN reserve_date DATETIME, IN res_date DATE)
BEGIN
    START TRANSACTION;
    INSERT INTO `reserve_list`(`reserve_list_dis_id`, `reserve_list_book_id`, `reserve_list_date`, `reserve_list_res_date`) VALUES (book_id, user_id);
    UPDATE `book_list` SET `book_status` = 1 WHERE `book_id` = book_id;
    COMMIT;
END //
DELIMITER ;