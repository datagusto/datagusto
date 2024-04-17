# ************************************************************
# Sequel Ace SQL dump
# Version 20062
#
# https://sequel-ace.com/
# https://github.com/Sequel-Ace/Sequel-Ace
#
# Host: localhost (MySQL 5.7.44)
# Database: dbtest
# Generation Time: 2024-04-10 09:49:17 +0000
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
	(4,'James Madison','James Madison Jr',4,'Port Conway','Virginia',57),
	(5,'James Monroe','',5,'Monroe Hall','Virginia',58),
	(7,'John Quincy Adams','',6,'Braintree','Massachusetts',57),
	(6,'Andrew Jackson','',7,'Waxhaws Region','South/North Carolina',61),
	(9,'Martin Van Buren','',8,'Kinderhook','New York',54),
	(8,'William Henry Harrison','',9,'Charles City County','Virginia',68),
	(11,'John Tyler','John Tyler Jr',10,'Charles City County','Virginia',51),
	(13,'James K. Polk','James Knox Polk',11,'Pineville','North Carolina',49),
	(10,'Zachary Taylor','',12,'Barboursville','Virginia',64),
	(14,'Millard Fillmore','',13,'Moravia','New York',50),
	(15,'Franklin Pierce','',14,'Hillsborough','New Hampshire',48),
	(12,'James Buchanan','James Buchanan Jr',15,'Cove Gap','Pennsylvania',65),
	(17,'Abraham Lincoln','',16,'Hardin County','Kentucky',52),
	(16,'Andrew Johnson','',17,'Raleigh','North Carolina',56),
	(18,'Ulysses S. Grant','Hiram Ulysses Grant',18,'Point Pleasant','Ohio',46),
	(19,'Rutherford B. Hayes','Rutherford Birchard Hayes',19,'Delaware','Ohio',54),
	(21,'James A. Garfield','James Abram Garfield',20,'Moreland Hills','Ohio',49),
	(20,'Chester A. Arthur','Chester Alan Arthur',21,'Fairfield','Vermont',51),
	(23,'Grover Cleveland','Stephen Grover Cleveland',22,'Caldwell','New Jersey',47),
	(22,'Benjamin Harrison','',23,'North Bend','Ohio',55),
	(23,'Grover Cleveland','Stephen Grover Cleveland',24,'Caldwell','New Jersey',55),
	(24,'William McKinley','William McKinley Jr',25,'Niles','Ohio',54),
	(27,'Theodore Roosevelt','Theodore Roosevelt Jr',26,'New York City','New York',42),
	(26,'William Howard Taft','',27,'Cincinnati','Ohio',51),
	(25,'Woodrow Wilson','Thomas Woodrow Wilson',28,'Staunton','Virginia',56),
	(28,'Warren G. Harding','Warren Gamaliel Harding',29,'Blooming Grove','Ohio',55),
	(29,'Calvin Coolidge','John Calvin Coolidge Jr',30,'Plymouth','Vermont',51),
	(30,'Herbert Hoover','Herbert Clark Hoover',31,'West Branch','Iowa',54),
	(31,'Franklin D. Roosevelt','Franklin Delano Roosevelt',32,'Hyde Park','New York',51),
	(32,'Harry S. Truman','',33,'Lamar','Missouri',60),
	(33,'Dwight D. Eisenhower','David Dwight Eisenhower',34,'Denison','Texas',62),
	(38,'John F. Kennedy','John Fitzgerald Kennedy',35,'Brookline','Massachusetts',43),
	(34,'Lyndon B. Johnson','Lyndon Baines Johnson',36,'Stonewall','Texas',55),
	(36,'Richard M. Nixon','Richard Milhous Nixon',37,'Yorba Linda','California',56),
	(37,'Gerald R. Ford','Leslie Lynch King Jr',38,'Omaha','Nebraska',61),
	(40,'Jimmy Carter','James Earl Carter Jr',39,'Plains','Georgia',52),
	(35,'Ronald Reagan','Ronald Wilson Reagan',40,'Tampico','Illinois',69),
	(39,'George H. W. Bush','George Herbert Walker Bush',41,'Milton','Massachusetts',64),
	(42,'Bill Clinton','William Jefferson Blythe III',42,'Hope','Arkansas',46),
	(41,'George W. Bush','George Walker Bush',43,'New Haven','Connecticut',54),
	(43,'Barack Obama','Barack Hussein Obama II',44,'Honolulu','Hawaii',47),
	(1,'George Washington','',1,'Pope&#39;s Creek','Virginia',57),
	(2,'John Adams','John Adams Jr',2,'Braintree','Massachusetts',61),
	(3,'Thomas Jefferson','',3,'Goochland County','Virginia',57),
	(4,'James Madison','James Madison Jr',4,'Port Conway','Virginia',57),
	(5,'James Monroe','',5,'Monroe Hall','Virginia',58),
	(7,'John Quincy Adams','',6,'Braintree','Massachusetts',57),
	(6,'Andrew Jackson','',7,'Waxhaws Region','South/North Carolina',61),
	(9,'Martin Van Buren','',8,'Kinderhook','New York',54),
	(8,'William Henry Harrison','',9,'Charles City County','Virginia',68),
	(11,'John Tyler','John Tyler Jr',10,'Charles City County','Virginia',51),
	(13,'James K. Polk','James Knox Polk',11,'Pineville','North Carolina',49),
	(10,'Zachary Taylor','',12,'Barboursville','Virginia',64),
	(14,'Millard Fillmore','',13,'Moravia','New York',50),
	(15,'Franklin Pierce','',14,'Hillsborough','New Hampshire',48),
	(12,'James Buchanan','James Buchanan Jr',15,'Cove Gap','Pennsylvania',65),
	(17,'Abraham Lincoln','',16,'Hardin County','Kentucky',52),
	(16,'Andrew Johnson','',17,'Raleigh','North Carolina',56),
	(18,'Ulysses S. Grant','Hiram Ulysses Grant',18,'Point Pleasant','Ohio',46),
	(19,'Rutherford B. Hayes','Rutherford Birchard Hayes',19,'Delaware','Ohio',54),
	(21,'James A. Garfield','James Abram Garfield',20,'Moreland Hills','Ohio',49),
	(20,'Chester A. Arthur','Chester Alan Arthur',21,'Fairfield','Vermont',51),
	(23,'Grover Cleveland','Stephen Grover Cleveland',22,'Caldwell','New Jersey',47),
	(22,'Benjamin Harrison','',23,'North Bend','Ohio',55),
	(23,'Grover Cleveland','Stephen Grover Cleveland',24,'Caldwell','New Jersey',55),
	(24,'William McKinley','William McKinley Jr',25,'Niles','Ohio',54),
	(27,'Theodore Roosevelt','Theodore Roosevelt Jr',26,'New York City','New York',42),
	(26,'William Howard Taft','',27,'Cincinnati','Ohio',51),
	(25,'Woodrow Wilson','Thomas Woodrow Wilson',28,'Staunton','Virginia',56),
	(28,'Warren G. Harding','Warren Gamaliel Harding',29,'Blooming Grove','Ohio',55),
	(29,'Calvin Coolidge','John Calvin Coolidge Jr',30,'Plymouth','Vermont',51),
	(30,'Herbert Hoover','Herbert Clark Hoover',31,'West Branch','Iowa',54),
	(31,'Franklin D. Roosevelt','Franklin Delano Roosevelt',32,'Hyde Park','New York',51),
	(32,'Harry S. Truman','',33,'Lamar','Missouri',60),
	(33,'Dwight D. Eisenhower','David Dwight Eisenhower',34,'Denison','Texas',62),
	(38,'John F. Kennedy','John Fitzgerald Kennedy',35,'Brookline','Massachusetts',43),
	(34,'Lyndon B. Johnson','Lyndon Baines Johnson',36,'Stonewall','Texas',55),
	(36,'Richard M. Nixon','Richard Milhous Nixon',37,'Yorba Linda','California',56),
	(37,'Gerald R. Ford','Leslie Lynch King Jr',38,'Omaha','Nebraska',61),
	(40,'Jimmy Carter','James Earl Carter Jr',39,'Plains','Georgia',52),
	(35,'Ronald Reagan','Ronald Wilson Reagan',40,'Tampico','Illinois',69),
	(39,'George H. W. Bush','George Herbert Walker Bush',41,'Milton','Massachusetts',64),
	(42,'Bill Clinton','William Jefferson Blythe III',42,'Hope','Arkansas',46),
	(41,'George W. Bush','George Walker Bush',43,'New Haven','Connecticut',54),
	(43,'Barack Obama','Barack Hussein Obama II',44,'Honolulu','Hawaii',47);

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
	(2,'John Adams; October 30 1735 – July 4 1826; (aged 90);','Massachusetts','March 4 1797; –; March 4 1801;','Federalist','3; (1796)','1st; Vice President of the United States'),
	(3,'Thomas Jefferson; April 13 1743 – July 4 1826; (aged 83);','Virginia','March 4 1801; –; March 4 1809','Democratic-; Republican','4; (1800)','2nd; Vice President of the United States'),
	(3,'Thomas Jefferson; April 13 1743 – July 4 1826; (aged 83);','Virginia','March 4 1801; –; March 4 1809','Democratic-; Republican','5; (1804)','2nd; Vice President of the United States'),
	(4,'James Madison; March 16 1751 – June 28 1836; (aged 85);','Virginia','March 4 1809; –; March 4 1817','Democratic-; Republican','6; (1808)','5th; United States Secretary of State; (1801–1809)'),
	(4,'James Madison; March 16 1751 – June 28 1836; (aged 85);','Virginia','March 4 1809; –; March 4 1817','Democratic-; Republican','7; (1812)','5th; United States Secretary of State; (1801–1809)'),
	(5,'James Monroe; April 28 1758 – July 4 1831; (aged 73);','Virginia','March 4 1817; –; March 4 1825','Democratic-; Republican','8; (1816)','7th; United States Secretary of State; (1811–1817)'),
	(5,'James Monroe; April 28 1758 – July 4 1831; (aged 73);','Virginia','March 4 1817; –; March 4 1825','Democratic-; Republican','9; (1820)','7th; United States Secretary of State; (1811–1817)'),
	(6,'John Quincy Adams; July 11 1767 – February 23 1848; (aged 80);','Massachusetts','March 4 1825; –; March 4 1829;','Democratic-; Republican','10; (1824)','8th; United States Secretary of State; (1817–1825)'),
	(7,'Andrew Jackson; March 15 1767 – June 8 1845; (aged 78);','Tennessee','March 4 1829; –; March 4 1837','Democratic','11; (1828)','U.S. Senator from Tennessee; (1823–1825)'),
	(7,'Andrew Jackson; March 15 1767 – June 8 1845; (aged 78);','Tennessee','March 4 1829; –; March 4 1837','Democratic','12; (1832)','U.S. Senator from Tennessee; (1823–1825)'),
	(8,'Martin Van Buren; December 5 1782 – July 24 1862; (aged 79);','New York','March 4 1837; –; March 4 1841;','Democratic','13; (1836)','8th; Vice President of the United States'),
	(9,'William Henry Harrison; February 9 1773 – April 4 1841; (aged 68);','Ohio','March 4 1841; –; April 4 1841;','Whig','14; (1840)','United States Minister to Colombia; (1828–1829)'),
	(10,'John Tyler; March 29 1790 – January 18 1862; (aged 71);','Virginia','April 4 1841; –; March 4 1845','Whig; April 4 1841 – September 13 1841','14; (1840)','10th; Vice President of the United States;'),
	(10,'John Tyler; March 29 1790 – January 18 1862; (aged 71);','Virginia','April 4 1841; –; March 4 1845','Independent; September 13 1841 – March 4 1845;','14; (1840)','10th; Vice President of the United States;'),
	(11,'James K. Polk; November 2 1795 – June 15 1849; (aged 53);','Tennessee','March 4 1845; –; March 4 1849','Democratic','15; (1844)','9th; Governor of Tennessee; (1839–1841)'),
	(12,'Zachary Taylor; November 24 1784 – July 9 1850; (aged 65);','Louisiana','March 4 1849; –; July 9 1850;','Whig','16; (1848)','Major General of the 1st Infantry Regiment; United States Army; (1846–1849)'),
	(13,'Millard Fillmore; January 7 1800 – March 8 1874; (aged 74);','New York','July 9 1850; –; March 4 1853;','Whig','16; (1848)','12th; Vice President of the United States'),
	(14,'Franklin Pierce; November 23 1804 – October 8 1869; (aged 64);','New Hampshire','March 4 1853; –; March 4 1857','Democratic','17; (1852)','Brigadier General of the 9th Infantry; United States Army; (1847–1848)'),
	(15,'James Buchanan; April 23 1791 – June 1 1868; (aged 77);','Pennsylvania','March 4 1857; –; March 4 1861','Democratic','18; (1856)','United States Minister to the; Court of St James&#39;s; (1853–1856)'),
	(16,'Abraham Lincoln; February 12 1809 – April 15 1865; (aged 56);','Illinois','March 4 1861; –; April 15 1865;','Republican','19; (1860)','U.S. Representative for Illinois&#39; 7th; (1847–1849)'),
	(16,'Abraham Lincoln; February 12 1809 – April 15 1865; (aged 56);','Illinois','March 4 1861; –; April 15 1865;','Republican; National Union;','20; (1864)','U.S. Representative for Illinois&#39; 7th; (1847–1849)'),
	(17,'Andrew Johnson; December 29 1808 – July 31 1875; (aged 66);','Tennessee','April 15 1865; –; March 4 1869','Democratic; National Union; Not Affiliated;','20; (1864)','16th; Vice President of the United States'),
	(18,'Ulysses S. Grant; April 27 1822 – July 23 1885; (aged 63);','Ohio','March 4 1869; –; March 4 1877','Republican','21; (1868)','Commanding General of the U.S. Army; (1864–1869)'),
	(18,'Ulysses S. Grant; April 27 1822 – July 23 1885; (aged 63);','Ohio','March 4 1869; –; March 4 1877','Republican','22; (1872)','Commanding General of the U.S. Army; (1864–1869)'),
	(19,'Rutherford B. Hayes; October 4 1822 – January 17 1893; (aged 70);','Ohio','March 4 1877; –; March 4 1881','Republican','23; (1876)','32nd; Governor of Ohio; (1868–1872 1876–1877)'),
	(20,'James A. Garfield; November 19 1831 – September 19 1881; (aged 49);','Ohio','March 4 1881; –; September 19 1881;','Republican','24; (1880)','U.S. Representative for Ohio&#39;s 19th; (1863–1881)'),
	(21,'Chester A. Arthur; October 5 1829 – November 18 1886; (aged 57);','New York','September 19 1881; –; March 4 1885','Republican','24; (1880)','20th; Vice President of the United States'),
	(22,'Grover Cleveland; March 18 1837 – June 24 1908; (aged 71);','New York','March 4 1885; –; March 4 1889;','Democratic','25; (1884)','28th; Governor of New York; (1883–1885)'),
	(23,'Benjamin Harrison; August 20 1833 – March 13 1901; (aged 67);','Indiana','March 4 1889; –; March 4 1893;','Republican','26; (1888)','U.S. Senator from Indiana; (1881–1887)'),
	(24,'Grover Cleveland; March 18 1837 – June 24 1908; (aged 71);','New York','March 4 1893; –; March 4 1897','Democratic','27; (1892)','22nd; President of the United States; (1885–1889)'),
	(25,'William McKinley; January 29 1843 – September 14 1901; (aged 58);','Ohio','March 4 1897; –; September 14 1901;','Republican','28; (1896)','39th; Governor of Ohio; (1892–1896)'),
	(25,'William McKinley; January 29 1843 – September 14 1901; (aged 58);','Ohio','March 4 1897; –; September 14 1901;','Republican','29; (1900)','39th; Governor of Ohio; (1892–1896)'),
	(26,'Theodore Roosevelt; October 27 1858 – January 6 1919; (aged 60);','New York','September 14 1901; –; March 4 1909;','Republican','29; (1900)','25th; Vice President of the United States'),
	(26,'Theodore Roosevelt; October 27 1858 – January 6 1919; (aged 60);','New York','September 14 1901; –; March 4 1909;','Republican','30; (1904)','25th; Vice President of the United States'),
	(27,'William Howard Taft; September 15 1857 – March 8 1930; (aged 72);','Ohio','March 4 1909; –; March 4 1913;','Republican','31; (1908)','42nd; United States Secretary of War; (1904–1908)'),
	(28,'Woodrow Wilson; December 28 1856 – February 3 1924; (aged 67);','New Jersey','March 4 1913; –; March 4 1921','Democratic','32; (1912)','34th; Governor of New Jersey; (1911–1913)'),
	(28,'Woodrow Wilson; December 28 1856 – February 3 1924; (aged 67);','New Jersey','March 4 1913; –; March 4 1921','Democratic','33; (1916)','34th; Governor of New Jersey; (1911–1913)'),
	(29,'Warren G. Harding; November 2 1865 – August 2 1923; (aged 57);','Ohio','March 4 1921; –; August 2 1923;','Republican','34; (1920)','U.S. Senator from Ohio; (1915–1921)'),
	(30,'Calvin Coolidge; July 4 1872 – January 5 1933; (aged 60);','Massachusetts','August 2 1923; –; March 4 1929','Republican','34; (1920)','29th; Vice President of the United States'),
	(30,'Calvin Coolidge; July 4 1872 – January 5 1933; (aged 60);','Massachusetts','August 2 1923; –; March 4 1929','Republican','35; (1924)','29th; Vice President of the United States'),
	(31,'Herbert Hoover; August 10 1874 – October 20 1964; (aged 90);','Iowa','March 4 1929; –; March 4 1933;','Republican','36; (1928)','3rd; United States Secretary of Commerce; (1921–1928)'),
	(32,'Franklin D. Roosevelt; January 30 1882 – April 12 1945; (aged 63);','New York','March 4 1933; –; April 12 1945;','Democratic','37; (1932);','44th; Governor of New York; (1929–1932)'),
	(32,'Franklin D. Roosevelt; January 30 1882 – April 12 1945; (aged 63);','New York','March 4 1933; –; April 12 1945;','Democratic','38; (1936)','44th; Governor of New York; (1929–1932)'),
	(32,'Franklin D. Roosevelt; January 30 1882 – April 12 1945; (aged 63);','New York','March 4 1933; –; April 12 1945;','Democratic','39; (1940)','44th; Governor of New York; (1929–1932)'),
	(32,'Franklin D. Roosevelt; January 30 1882 – April 12 1945; (aged 63);','New York','March 4 1933; –; April 12 1945;','Democratic','40; (1944)','44th; Governor of New York; (1929–1932)'),
	(33,'Harry S. Truman; May 8 1884 – December 26 1972; (aged 88);','Missouri','April 12 1945; –; January 20 1953','Democratic','40; (1944)','34th; Vice President of the United States'),
	(33,'Harry S. Truman; May 8 1884 – December 26 1972; (aged 88);','Missouri','April 12 1945; –; January 20 1953','Democratic','41; (1948)','34th; Vice President of the United States'),
	(34,'Dwight D. Eisenhower; October 14 1890 – March 28 1969; (aged 78);','Kansas','January 20 1953; –; January 20 1961;','Republican','42; (1952)','Supreme Allied Commander Europe; (1949–1952)'),
	(34,'Dwight D. Eisenhower; October 14 1890 – March 28 1969; (aged 78);','Kansas','January 20 1953; –; January 20 1961;','Republican','43; (1956)','Supreme Allied Commander Europe; (1949–1952)'),
	(35,'John F. Kennedy; May 29 1917 – November 22 1963; (aged 46);','Massachusetts','January 20 1961; –; November 22 1963;','Democratic','44; (1960)','U.S. Senator from Massachusetts; (1953–1960)'),
	(36,'Lyndon B. Johnson; August 27 1908 – January 22 1973; (aged 64);','Texas','November 22 1963; –; January 20 1969','Democratic','44; (1960)','37th; Vice President of the United States'),
	(36,'Lyndon B. Johnson; August 27 1908 – January 22 1973; (aged 64);','Texas','November 22 1963; –; January 20 1969','Democratic','45; (1964)','37th; Vice President of the United States'),
	(37,'Richard Nixon; January 9 1913 – April 22 1994; (aged 81);','California','January 20 1969; –; August 9 1974;','Republican','46; (1968)','36th; Vice President of the United States; (1953–1961)'),
	(37,'Richard Nixon; January 9 1913 – April 22 1994; (aged 81);','California','January 20 1969; –; August 9 1974;','Republican','47; (1972)','36th; Vice President of the United States; (1953–1961)'),
	(38,'Gerald Ford; July 14 1913 – December 26 2006; (aged 93);','Michigan','August 9 1974; –; January 20 1977;','Republican','47; (1972)','40th; Vice President of the United States'),
	(39,'Jimmy Carter; Born: October 1 1924 (age 91);','Georgia','January 20 1977; –; January 20 1981;','Democratic','48; (1976)','76th; Governor of Georgia; (1971–1975)'),
	(40,'Ronald Reagan; February 6 1911 – June 5 2004; (aged 93);','California','January 20 1981; –; January 20 1989','Republican','49; (1980)','33rd; Governor of California; (1967–1975)'),
	(40,'Ronald Reagan; February 6 1911 – June 5 2004; (aged 93);','California','January 20 1981; –; January 20 1989','Republican','50; (1984)','33rd; Governor of California; (1967–1975)'),
	(41,'George H. W. Bush; Born: June 12 1924 (age 91);','Texas','January 20 1989; –; January 20 1993;','Republican','51; (1988)','43rd; Vice President of the United States'),
	(42,'Bill Clinton; Born: August 19 1946 (age 69);','Arkansas','January 20 1993; –; January 20 2001','Democratic','52; (1992)','40th &amp; 42nd; Governor of Arkansas; (1979–1981 1983–1992)'),
	(42,'Bill Clinton; Born: August 19 1946 (age 69);','Arkansas','January 20 1993; –; January 20 2001','Democratic','53; (1996)','40th &amp; 42nd; Governor of Arkansas; (1979–1981 1983–1992)'),
	(43,'George W. Bush; Born: July 6 1946 (age 69);','Texas','January 20 2001; –; January 20 2009','Republican','54; (2000)','46th; Governor of Texas; (1995–2000)'),
	(43,'George W. Bush; Born: July 6 1946 (age 69);','Texas','January 20 2001; –; January 20 2009','Republican','55; (2004)','46th; Governor of Texas; (1995–2000)'),
	(44,'Barack Obama; Born: August 4 1961 (age 54);','Illinois','January 20 2009; –; Incumbent','Democratic','56; (2008)','U.S. Senator from Illinois; (2005–2008)'),
	(44,'Barack Obama; Born: August 4 1961 (age 54);','Illinois','January 20 2009; –; Incumbent','Democratic','57; (2012)','U.S. Senator from Illinois; (2005–2008)'),
	(1,'George Washington; February 22 1732 – December 14 1799; (aged 67);','Virginia','April 30 1789; –; March 4 1797','Non-partisan;','1; (1789)','Commander-in-Chief; of the; Continental Army; (1775–1783)'),
	(1,'George Washington; February 22 1732 – December 14 1799; (aged 67);','Virginia','April 30 1789; –; March 4 1797','Non-partisan;','2; (1792)','Commander-in-Chief; of the; Continental Army; (1775–1783)'),
	(2,'John Adams; October 30 1735 – July 4 1826; (aged 90);','Massachusetts','March 4 1797; –; March 4 1801;','Federalist','3; (1796)','1st; Vice President of the United States'),
	(3,'Thomas Jefferson; April 13 1743 – July 4 1826; (aged 83);','Virginia','March 4 1801; –; March 4 1809','Democratic-; Republican','4; (1800)','2nd; Vice President of the United States'),
	(3,'Thomas Jefferson; April 13 1743 – July 4 1826; (aged 83);','Virginia','March 4 1801; –; March 4 1809','Democratic-; Republican','5; (1804)','2nd; Vice President of the United States'),
	(4,'James Madison; March 16 1751 – June 28 1836; (aged 85);','Virginia','March 4 1809; –; March 4 1817','Democratic-; Republican','6; (1808)','5th; United States Secretary of State; (1801–1809)'),
	(4,'James Madison; March 16 1751 – June 28 1836; (aged 85);','Virginia','March 4 1809; –; March 4 1817','Democratic-; Republican','7; (1812)','5th; United States Secretary of State; (1801–1809)'),
	(5,'James Monroe; April 28 1758 – July 4 1831; (aged 73);','Virginia','March 4 1817; –; March 4 1825','Democratic-; Republican','8; (1816)','7th; United States Secretary of State; (1811–1817)'),
	(5,'James Monroe; April 28 1758 – July 4 1831; (aged 73);','Virginia','March 4 1817; –; March 4 1825','Democratic-; Republican','9; (1820)','7th; United States Secretary of State; (1811–1817)'),
	(6,'John Quincy Adams; July 11 1767 – February 23 1848; (aged 80);','Massachusetts','March 4 1825; –; March 4 1829;','Democratic-; Republican','10; (1824)','8th; United States Secretary of State; (1817–1825)'),
	(7,'Andrew Jackson; March 15 1767 – June 8 1845; (aged 78);','Tennessee','March 4 1829; –; March 4 1837','Democratic','11; (1828)','U.S. Senator from Tennessee; (1823–1825)'),
	(7,'Andrew Jackson; March 15 1767 – June 8 1845; (aged 78);','Tennessee','March 4 1829; –; March 4 1837','Democratic','12; (1832)','U.S. Senator from Tennessee; (1823–1825)'),
	(8,'Martin Van Buren; December 5 1782 – July 24 1862; (aged 79);','New York','March 4 1837; –; March 4 1841;','Democratic','13; (1836)','8th; Vice President of the United States'),
	(9,'William Henry Harrison; February 9 1773 – April 4 1841; (aged 68);','Ohio','March 4 1841; –; April 4 1841;','Whig','14; (1840)','United States Minister to Colombia; (1828–1829)'),
	(10,'John Tyler; March 29 1790 – January 18 1862; (aged 71);','Virginia','April 4 1841; –; March 4 1845','Whig; April 4 1841 – September 13 1841','14; (1840)','10th; Vice President of the United States;'),
	(10,'John Tyler; March 29 1790 – January 18 1862; (aged 71);','Virginia','April 4 1841; –; March 4 1845','Independent; September 13 1841 – March 4 1845;','14; (1840)','10th; Vice President of the United States;'),
	(11,'James K. Polk; November 2 1795 – June 15 1849; (aged 53);','Tennessee','March 4 1845; –; March 4 1849','Democratic','15; (1844)','9th; Governor of Tennessee; (1839–1841)'),
	(12,'Zachary Taylor; November 24 1784 – July 9 1850; (aged 65);','Louisiana','March 4 1849; –; July 9 1850;','Whig','16; (1848)','Major General of the 1st Infantry Regiment; United States Army; (1846–1849)'),
	(13,'Millard Fillmore; January 7 1800 – March 8 1874; (aged 74);','New York','July 9 1850; –; March 4 1853;','Whig','16; (1848)','12th; Vice President of the United States'),
	(14,'Franklin Pierce; November 23 1804 – October 8 1869; (aged 64);','New Hampshire','March 4 1853; –; March 4 1857','Democratic','17; (1852)','Brigadier General of the 9th Infantry; United States Army; (1847–1848)'),
	(15,'James Buchanan; April 23 1791 – June 1 1868; (aged 77);','Pennsylvania','March 4 1857; –; March 4 1861','Democratic','18; (1856)','United States Minister to the; Court of St James&#39;s; (1853–1856)'),
	(16,'Abraham Lincoln; February 12 1809 – April 15 1865; (aged 56);','Illinois','March 4 1861; –; April 15 1865;','Republican','19; (1860)','U.S. Representative for Illinois&#39; 7th; (1847–1849)'),
	(16,'Abraham Lincoln; February 12 1809 – April 15 1865; (aged 56);','Illinois','March 4 1861; –; April 15 1865;','Republican; National Union;','20; (1864)','U.S. Representative for Illinois&#39; 7th; (1847–1849)'),
	(17,'Andrew Johnson; December 29 1808 – July 31 1875; (aged 66);','Tennessee','April 15 1865; –; March 4 1869','Democratic; National Union; Not Affiliated;','20; (1864)','16th; Vice President of the United States'),
	(18,'Ulysses S. Grant; April 27 1822 – July 23 1885; (aged 63);','Ohio','March 4 1869; –; March 4 1877','Republican','21; (1868)','Commanding General of the U.S. Army; (1864–1869)'),
	(18,'Ulysses S. Grant; April 27 1822 – July 23 1885; (aged 63);','Ohio','March 4 1869; –; March 4 1877','Republican','22; (1872)','Commanding General of the U.S. Army; (1864–1869)'),
	(19,'Rutherford B. Hayes; October 4 1822 – January 17 1893; (aged 70);','Ohio','March 4 1877; –; March 4 1881','Republican','23; (1876)','32nd; Governor of Ohio; (1868–1872 1876–1877)'),
	(20,'James A. Garfield; November 19 1831 – September 19 1881; (aged 49);','Ohio','March 4 1881; –; September 19 1881;','Republican','24; (1880)','U.S. Representative for Ohio&#39;s 19th; (1863–1881)'),
	(21,'Chester A. Arthur; October 5 1829 – November 18 1886; (aged 57);','New York','September 19 1881; –; March 4 1885','Republican','24; (1880)','20th; Vice President of the United States'),
	(22,'Grover Cleveland; March 18 1837 – June 24 1908; (aged 71);','New York','March 4 1885; –; March 4 1889;','Democratic','25; (1884)','28th; Governor of New York; (1883–1885)'),
	(23,'Benjamin Harrison; August 20 1833 – March 13 1901; (aged 67);','Indiana','March 4 1889; –; March 4 1893;','Republican','26; (1888)','U.S. Senator from Indiana; (1881–1887)'),
	(24,'Grover Cleveland; March 18 1837 – June 24 1908; (aged 71);','New York','March 4 1893; –; March 4 1897','Democratic','27; (1892)','22nd; President of the United States; (1885–1889)'),
	(25,'William McKinley; January 29 1843 – September 14 1901; (aged 58);','Ohio','March 4 1897; –; September 14 1901;','Republican','28; (1896)','39th; Governor of Ohio; (1892–1896)'),
	(25,'William McKinley; January 29 1843 – September 14 1901; (aged 58);','Ohio','March 4 1897; –; September 14 1901;','Republican','29; (1900)','39th; Governor of Ohio; (1892–1896)'),
	(26,'Theodore Roosevelt; October 27 1858 – January 6 1919; (aged 60);','New York','September 14 1901; –; March 4 1909;','Republican','29; (1900)','25th; Vice President of the United States'),
	(26,'Theodore Roosevelt; October 27 1858 – January 6 1919; (aged 60);','New York','September 14 1901; –; March 4 1909;','Republican','30; (1904)','25th; Vice President of the United States'),
	(27,'William Howard Taft; September 15 1857 – March 8 1930; (aged 72);','Ohio','March 4 1909; –; March 4 1913;','Republican','31; (1908)','42nd; United States Secretary of War; (1904–1908)'),
	(28,'Woodrow Wilson; December 28 1856 – February 3 1924; (aged 67);','New Jersey','March 4 1913; –; March 4 1921','Democratic','32; (1912)','34th; Governor of New Jersey; (1911–1913)'),
	(28,'Woodrow Wilson; December 28 1856 – February 3 1924; (aged 67);','New Jersey','March 4 1913; –; March 4 1921','Democratic','33; (1916)','34th; Governor of New Jersey; (1911–1913)'),
	(29,'Warren G. Harding; November 2 1865 – August 2 1923; (aged 57);','Ohio','March 4 1921; –; August 2 1923;','Republican','34; (1920)','U.S. Senator from Ohio; (1915–1921)'),
	(30,'Calvin Coolidge; July 4 1872 – January 5 1933; (aged 60);','Massachusetts','August 2 1923; –; March 4 1929','Republican','34; (1920)','29th; Vice President of the United States'),
	(30,'Calvin Coolidge; July 4 1872 – January 5 1933; (aged 60);','Massachusetts','August 2 1923; –; March 4 1929','Republican','35; (1924)','29th; Vice President of the United States'),
	(31,'Herbert Hoover; August 10 1874 – October 20 1964; (aged 90);','Iowa','March 4 1929; –; March 4 1933;','Republican','36; (1928)','3rd; United States Secretary of Commerce; (1921–1928)'),
	(32,'Franklin D. Roosevelt; January 30 1882 – April 12 1945; (aged 63);','New York','March 4 1933; –; April 12 1945;','Democratic','37; (1932);','44th; Governor of New York; (1929–1932)'),
	(32,'Franklin D. Roosevelt; January 30 1882 – April 12 1945; (aged 63);','New York','March 4 1933; –; April 12 1945;','Democratic','38; (1936)','44th; Governor of New York; (1929–1932)'),
	(32,'Franklin D. Roosevelt; January 30 1882 – April 12 1945; (aged 63);','New York','March 4 1933; –; April 12 1945;','Democratic','39; (1940)','44th; Governor of New York; (1929–1932)'),
	(32,'Franklin D. Roosevelt; January 30 1882 – April 12 1945; (aged 63);','New York','March 4 1933; –; April 12 1945;','Democratic','40; (1944)','44th; Governor of New York; (1929–1932)'),
	(33,'Harry S. Truman; May 8 1884 – December 26 1972; (aged 88);','Missouri','April 12 1945; –; January 20 1953','Democratic','40; (1944)','34th; Vice President of the United States'),
	(33,'Harry S. Truman; May 8 1884 – December 26 1972; (aged 88);','Missouri','April 12 1945; –; January 20 1953','Democratic','41; (1948)','34th; Vice President of the United States'),
	(34,'Dwight D. Eisenhower; October 14 1890 – March 28 1969; (aged 78);','Kansas','January 20 1953; –; January 20 1961;','Republican','42; (1952)','Supreme Allied Commander Europe; (1949–1952)'),
	(34,'Dwight D. Eisenhower; October 14 1890 – March 28 1969; (aged 78);','Kansas','January 20 1953; –; January 20 1961;','Republican','43; (1956)','Supreme Allied Commander Europe; (1949–1952)'),
	(35,'John F. Kennedy; May 29 1917 – November 22 1963; (aged 46);','Massachusetts','January 20 1961; –; November 22 1963;','Democratic','44; (1960)','U.S. Senator from Massachusetts; (1953–1960)'),
	(36,'Lyndon B. Johnson; August 27 1908 – January 22 1973; (aged 64);','Texas','November 22 1963; –; January 20 1969','Democratic','44; (1960)','37th; Vice President of the United States'),
	(36,'Lyndon B. Johnson; August 27 1908 – January 22 1973; (aged 64);','Texas','November 22 1963; –; January 20 1969','Democratic','45; (1964)','37th; Vice President of the United States'),
	(37,'Richard Nixon; January 9 1913 – April 22 1994; (aged 81);','California','January 20 1969; –; August 9 1974;','Republican','46; (1968)','36th; Vice President of the United States; (1953–1961)'),
	(37,'Richard Nixon; January 9 1913 – April 22 1994; (aged 81);','California','January 20 1969; –; August 9 1974;','Republican','47; (1972)','36th; Vice President of the United States; (1953–1961)'),
	(38,'Gerald Ford; July 14 1913 – December 26 2006; (aged 93);','Michigan','August 9 1974; –; January 20 1977;','Republican','47; (1972)','40th; Vice President of the United States'),
	(39,'Jimmy Carter; Born: October 1 1924 (age 91);','Georgia','January 20 1977; –; January 20 1981;','Democratic','48; (1976)','76th; Governor of Georgia; (1971–1975)'),
	(40,'Ronald Reagan; February 6 1911 – June 5 2004; (aged 93);','California','January 20 1981; –; January 20 1989','Republican','49; (1980)','33rd; Governor of California; (1967–1975)'),
	(40,'Ronald Reagan; February 6 1911 – June 5 2004; (aged 93);','California','January 20 1981; –; January 20 1989','Republican','50; (1984)','33rd; Governor of California; (1967–1975)'),
	(41,'George H. W. Bush; Born: June 12 1924 (age 91);','Texas','January 20 1989; –; January 20 1993;','Republican','51; (1988)','43rd; Vice President of the United States'),
	(42,'Bill Clinton; Born: August 19 1946 (age 69);','Arkansas','January 20 1993; –; January 20 2001','Democratic','52; (1992)','40th &amp; 42nd; Governor of Arkansas; (1979–1981 1983–1992)'),
	(42,'Bill Clinton; Born: August 19 1946 (age 69);','Arkansas','January 20 1993; –; January 20 2001','Democratic','53; (1996)','40th &amp; 42nd; Governor of Arkansas; (1979–1981 1983–1992)'),
	(43,'George W. Bush; Born: July 6 1946 (age 69);','Texas','January 20 2001; –; January 20 2009','Republican','54; (2000)','46th; Governor of Texas; (1995–2000)'),
	(43,'George W. Bush; Born: July 6 1946 (age 69);','Texas','January 20 2001; –; January 20 2009','Republican','55; (2004)','46th; Governor of Texas; (1995–2000)'),
	(44,'Barack Obama; Born: August 4 1961 (age 54);','Illinois','January 20 2009; –; Incumbent','Democratic','56; (2008)','U.S. Senator from Illinois; (2005–2008)'),
	(44,'Barack Obama; Born: August 4 1961 (age 54);','Illinois','January 20 2009; –; Incumbent','Democratic','57; (2012)','U.S. Senator from Illinois; (2005–2008)');

/*!40000 ALTER TABLE `president_vote` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
