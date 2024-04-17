# ************************************************************
# Sequel Ace SQL dump
# Version 20062
#
# https://sequel-ace.com/
# https://github.com/Sequel-Ace/Sequel-Ace
#
# Host: localhost (MySQL 5.7.44)
# Database: db
# Generation Time: 2024-04-10 09:49:05 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
SET NAMES utf8mb4;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE='NO_AUTO_VALUE_ON_ZERO', SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table president
# ------------------------------------------------------------

DROP TABLE IF EXISTS `president`;

CREATE TABLE `president` (
  `OB` int(11) DEFAULT NULL,
  `Name` varchar(50) DEFAULT NULL,
  `BirthName` varchar(50) DEFAULT NULL COMMENT 'full name of the president',
  `OP` int(11) DEFAULT NULL,
  `Birthplace` varchar(50) DEFAULT NULL,
  `StateOfBirth` varchar(50) DEFAULT NULL,
  `AP` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `president` WRITE;
/*!40000 ALTER TABLE `president` DISABLE KEYS */;

INSERT INTO `president` (`OB`, `Name`, `BirthName`, `OP`, `Birthplace`, `StateOfBirth`, `AP`)
VALUES
	(1,'George Washington','',1,'Pope&#39;s Creek','Virginia',57),
	(2,'John Adams','John Adams Jr',2,'Braintree','Massachusetts',61),
	(3,'Thomas Jefferson','',3,'Goochland County','Virginia',57),
	(4,'James Madison','James Madison Jr',4,'Port Conway','Virginia',57);

/*!40000 ALTER TABLE `president` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table president_vote
# ------------------------------------------------------------

DROP TABLE IF EXISTS `president_vote`;

CREATE TABLE `president_vote` (
  `No` int(11) DEFAULT NULL,
  `President` varchar(128) DEFAULT NULL,
  `State` varchar(50) DEFAULT NULL,
  `TermOfOffice` varchar(50) DEFAULT NULL,
  `Party` varchar(50) DEFAULT NULL,
  `Term` varchar(50) DEFAULT NULL,
  `PreviousOffice` varchar(128) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `president_vote` WRITE;
/*!40000 ALTER TABLE `president_vote` DISABLE KEYS */;

INSERT INTO `president_vote` (`No`, `President`, `State`, `TermOfOffice`, `Party`, `Term`, `PreviousOffice`)
VALUES
	(1,'George Washington; February 22 1732 – December 14 1799; (aged 67);','Virginia','April 30 1789; –; March 4 1797','Non-partisan;','1; (1789)','Commander-in-Chief; of the; Continental Army; (1775–1783)'),
	(1,'George Washington; February 22 1732 – December 14 1799; (aged 67);','Virginia','April 30 1789; –; March 4 1797','Non-partisan;','2; (1792)','Commander-in-Chief; of the; Continental Army; (1775–1783)'),
	(2,'John Adams; October 30 1735 – July 4 1826; (aged 90);','Massachusetts','March 4 1797; –; March 4 1801;','Federalist','3; (1796)','1st; Vice President of the United States');

/*!40000 ALTER TABLE `president_vote` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
