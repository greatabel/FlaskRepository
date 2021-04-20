-- MySQL dump 10.13  Distrib 8.0.19, for osx10.14 (x86_64)
--
-- Host: localhost    Database: movie
-- ------------------------------------------------------
-- Server version	8.0.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `movie`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `movie` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `movie`;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `is_super` smallint DEFAULT NULL,
  `role_id` int DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `role_id` (`role_id`),
  KEY `ix_admin_addtime` (`addtime`),
  CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,'Abel','pbkdf2:sha256:150000$xce5c1nM$b08b6d014f9c48ca9b360232d8a3f97ed7b9ea0af8148e255804582d6bea0ff8',0,1,'2021-03-05 19:25:27');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `adminlog`
--

DROP TABLE IF EXISTS `adminlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `adminlog` (
  `id` int NOT NULL AUTO_INCREMENT,
  `admin_id` int DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  KEY `ix_adminlog_addtime` (`addtime`),
  CONSTRAINT `adminlog_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adminlog`
--

LOCK TABLES `adminlog` WRITE;
/*!40000 ALTER TABLE `adminlog` DISABLE KEYS */;
INSERT INTO `adminlog` VALUES (1,1,'127.0.0.1','2021-03-05 19:29:34'),(2,1,'127.0.0.1','2021-03-05 19:30:50'),(3,1,'127.0.0.1','2021-03-05 19:43:01'),(4,1,'127.0.0.1','2021-03-05 19:43:17'),(5,1,'127.0.0.1','2021-03-05 19:46:43'),(6,1,'127.0.0.1','2021-03-07 01:24:54'),(7,1,'127.0.0.1','2021-03-07 05:21:10'),(8,1,'127.0.0.1','2021-03-16 11:19:36'),(9,1,'127.0.0.1','2021-03-16 13:47:26');
/*!40000 ALTER TABLE `adminlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth`
--

DROP TABLE IF EXISTS `auth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `url` (`url`),
  KEY `ix_auth_addtime` (`addtime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth`
--

LOCK TABLES `auth` WRITE;
/*!40000 ALTER TABLE `auth` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `content` text,
  `movie_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  `star` smallint DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `movie_id` (`movie_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_comment_addtime` (`addtime`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`),
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movie`
--

DROP TABLE IF EXISTS `movie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movie` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `info` text,
  `logo` varchar(255) DEFAULT NULL,
  `star` smallint DEFAULT NULL,
  `playnum` bigint DEFAULT NULL,
  `commentnum` bigint DEFAULT NULL,
  `tag_id` int DEFAULT NULL,
  `area` varchar(255) DEFAULT NULL,
  `release_time` date DEFAULT NULL,
  `length` varchar(100) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  UNIQUE KEY `url` (`url`),
  UNIQUE KEY `logo` (`logo`),
  KEY `tag_id` (`tag_id`),
  KEY `ix_movie_addtime` (`addtime`),
  CONSTRAINT `movie_ibfk_1` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movie`
--

LOCK TABLES `movie` WRITE;
/*!40000 ALTER TABLE `movie` DISABLE KEYS */;
INSERT INTO `movie` VALUES (1,'海贼王剧场版10','20210307022959d21cf6fefeba478eab23d66e28da3030.mp4','在一个风和日丽的日子，草帽海贼团正悠闲地在海上航行。突然，天空中出现一个漂浮的小岛，娜美及时通知各位规避即将到来的龙卷风，她的能力引起了小岛上海贼的注意。这个海贼首领非同寻常，他名叫金狮子史基，在大海贼时代到来前曾和哥鲁德?罗杰拼杀争霸。罗杰被俘后，史基也被投入海底监狱，但他却斩断双脚逃亡，并决心向东海展开复仇。史基意欲拉娜美入伙，双方不可避免发生纷争，经过一波三折，娜美最终落入史基手中。为了救出伙伴，并阻止东海毁灭计划，草帽海贼团将和史上最强大的敌人展开对决……本片根据尾田荣一郎同名原著改编，系《海贼王》的第十部剧场版动画，尾田荣一郎亲自担任制作总指挥。','20210307022959ae27bebc659a4fa0b3f15e135916b854.png',4,16,0,1,'日本','2021-03-30','113','2021-03-07 01:52:35'),(2,'人生密密缝','20210307022803d99e7c39ecfe47eab4e06edf843e4e06.mp4','友子（柿园玲佳饰）和母亲过着相依为命的生活，母亲常常徘徊在不同的男人之间，每天都喝到深夜才回来，友子虽然年幼，却早已经习惯了这样的生活。某日，母亲在丢下了生活费后又不知所踪，无奈之下，友子只能找到舅舅政男（桐谷健太饰），暂时住在他的家里。在舅舅家，友子见到了政男的同居“女友”伦子（生田斗真饰），伦子虽然拥有着柔软的胸脯，却是个货真价实的男人。在友子面前，伦子展现出了无限的温柔和体贴，渐渐让友子找回了缺失的母爱，三个人组成了一个奇异却充满了温暖的家庭。可爱乖巧的友子让伦子渐渐产生了想要将她永远留在身边的念头，可就在此时，友子的母亲回来了。','202103070228033500395788114d0283e75ec62053be64.png',4,5,0,2,'日本','2017-12-02','113','2021-03-07 02:28:04'),(3,'八美图','202103070237387118c0a4e49b46fdb8f02462cda4e03c.mp4','圣诞节前夕，一个富裕人家正在忙着筹备圣诞。窗外白雪皑皑，屋里迎来了女儿大学归来。一家人沉浸在圣诞前团聚的气氛。此时，大家以为作为一家之主的父亲还没有睡醒，谁知打开房门一开，他竟死在了睡床上，背后插着一把刀。众人惊慌失措，想报警之时却发现电话线早以被剪断；车已被蓄意破坏，无法开到警局。明显地，凶手就在这8人中间。彼此的猜忌和指控开始了，各人不为人知的秘密一一曝光，伦理道德的颠覆，贪婪自私的本性，令这个圣诞前夕特别混乱。讽刺的是，最后谁是凶手已经不重要了……','202103070237385fd3d4b364b44d63a144396ee7abe1b4.png',3,4,0,2,'美国','2021-03-07','123','2021-03-07 02:37:38'),(4,'必是天堂','20210307031009067601ccd9b443fd87e6c5dffedc01ea.mp4','阔别影坛六年的伊利亚·苏雷曼新片必是天堂将于本月6日开拍，影片将延其以导演本人为主角及故事讲述者的方式，苏雷曼离开自己的祖国巴勒斯坦，去寻找一个无需遭遇日常暴力、路障、身份检查的地方，于是他前往了巴黎、纽约，但他发现这些城市与自己的家乡上演着相似的情节。RectangleProductions公司和MichelMerkt担当制作，LePacte公司已拿下其法国发行权。','2021030703100984af8968f0ca47049e11df464b882efb.png',3,4,0,3,'法国','2021-03-07','97','2021-03-07 03:10:10'),(5,'黑侠','202103161354388c167293f51b47ecb6abd06340fc2a5e.mp4','徐夕（李连杰）本是神秘杀手组织701部队里的一名冷血杀手，因为不想再做杀人工具，他逃离了该组织来到香港化身为一名普通的图书馆理员，因此结识警察石SIR并与之成为好友，不想701部队为追杀黑帮头目突然现身香港，一时石SIR及警方均束手无策，见好友处于危难中，徐夕挺身而出化为黑侠。黑侠让701部队的首脑熊菊（龙刚）大为震怒，遂派徐夕旧情人若兰规劝黑侠归顺，被徐夕断然拒绝，结果令图书馆除Tracy（莫文蔚）之外的诸同事皆丧命。为保护Tracy，徐夕再做黑侠采用强硬态度要带她走，遭不知黑侠就是其意中人徐夕的Tracy的拒绝。后在与熊菊一干人等对抗的过程中，徐夕渐从Tracy身上寻到自己想要的情感。','20210316135438a86184e6f9874cee885ac4bac3ef6b51.png',3,0,0,1,'中国香港','2021-03-16','96','2021-03-16 13:54:38'),(6,'美少女特攻队 Sucker Punch','202103161412452152e7589e65455a8de169da07448719.mp4','金发碧眼的洋娃娃（EmilyBrowning饰）宛如一只时刻会受到惊吓的小鸟，这一天她被送进一家私人会所。该会所由蓝佬（OscarIsaac饰）掌控，他四处网罗妙龄女孩，并让葛斯基夫人（CarlaGugino饰）教授她们舞蹈，旨在取悦那些腰缠万贯的富翁和手眼通天的政要。洋娃娃在此结识了小甜荳（AbbieCornish饰）、火箭女（JenaMalone饰）、布女郎（VanessaHudgens饰）、黑琥珀（JamieChung饰）这4名好友。洋娃娃不愿沦为供人把玩的工具，她与朋友们商量从此逃走。逃亡计划需要4样工具：地图、打火机、刀和钥匙。朋友们负责盗取这些工具，而洋娃娃则用她那迷人且极具魔幻色彩的舞蹈吸引着蓝佬等人的注意力。只是终究也分不清，这是谁人的魔幻世界……','20210316141245282cc7dc36d94f519aa5ef4bd235ae5f.png',3,2,0,5,'美国','2011-10-01','110','2021-03-16 14:12:11'),(7,'印度暴徒','202103161419029fc00e0e2b7b4442b8bc5b7fdf0be93c.mp4','故事的背景是在1795年东印度公司殖民统治印度期间，殖民统治者想要抓住反抗组织”阿扎德“的领袖（阿米特巴·巴强饰演）于是找来了混混弗朗基（阿米尔·汗饰演）充当间谍，但弗朗基在潜伏过程中却有了另外的想法，一段充满了意料之外的动作冒险故事由此展开','202103161419028ad6a6cf8e7049d286c909841cddfe91.png',1,1,0,2,'印度','2018-12-01','164','2021-03-16 14:19:03'),(8,'关云长','20210317103420fb4154edb8ba4132bea44788809ebd77.mp4','东汉末年乱世中，刘备的两位夫人、以及一位未过门的小妾绮兰（孙俪 饰）受困曹营，关云长（甄子丹 饰）为存忠义投降曹操（姜文 饰），但始终不能原谅曹操操控汉室的狼子野心，希望能够重回刘备身边。曹操倾慕关羽之将才以及仁者之心，试图用天下苍生之利益说服后者。适逢袁绍起兵伐曹，关云长于阵斩杀颜良，获封汉寿亭侯，并与张辽（邵兵 饰）结下同袍之谊。曹操将两位刘夫人遣返后，在关云长酒中加入春药，欲使其与绮兰发生不义关系——关云长昔日对同乡绮兰暗怀情意，甚至曾经不惜为她杀死官兵，这段感情终究被叔嫂之礼阻断，清醒过来的关云长携绮兰投奔刘备，沿路冲破重重关卡，留下“过五关斩六将”的千古传奇','20210317103420c5a43383f2814c7e90974c4d391c1d1a.png',2,1,0,2,'中国','2011-10-01','110','2021-03-17 10:34:20'),(9,'生之欲','20210317103514c87a65ad9ff34ca1a7ec7835591ba2a7.mp4','市政府市民科科长渡边勘治（志村乔饰）是名近三十年全勤的模范公务员，然而他和同事们每天忙碌却人浮于事，不知道自己在忙些什么。一帮妇女联合到市政府申请填平社区附近的臭水池，在上面建造个小公园。市民科的接待人员告诉她们要把问题反映到土木课，公园课把她们推到建设科……，申请书转 了一圈后，又被踢回市民科。\r\n　　一个月后，渡边因身体不适，去医院被查出胃癌，时日无多。渡边回到家，感到孤独无助，儿子（金子信雄饰）只想着用老人的退休金及储蓄，到外面另辟小家庭。绝望中的渡边没有去上班，借酒浇愁。之后，请辞的女科员小田（小田切美善饰）给了渡边以启示。','2021031710351492b0fa609e9f447195e3c24f92cc9578.png',5,0,0,6,'日本','1952-10-10','114','2021-03-17 10:35:14');
/*!40000 ALTER TABLE `movie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `moviecol`
--

DROP TABLE IF EXISTS `moviecol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `moviecol` (
  `id` int NOT NULL AUTO_INCREMENT,
  `movie_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `movie_id` (`movie_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_moviecol_addtime` (`addtime`),
  CONSTRAINT `moviecol_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`),
  CONSTRAINT `moviecol_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `moviecol`
--

LOCK TABLES `moviecol` WRITE;
/*!40000 ALTER TABLE `moviecol` DISABLE KEYS */;
INSERT INTO `moviecol` VALUES (1,4,1,'2021-03-07 03:10:47');
/*!40000 ALTER TABLE `moviecol` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oplog`
--

DROP TABLE IF EXISTS `oplog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `oplog` (
  `id` int NOT NULL AUTO_INCREMENT,
  `admin_id` int DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `reason` varchar(600) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  KEY `ix_oplog_addtime` (`addtime`),
  CONSTRAINT `oplog_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oplog`
--

LOCK TABLES `oplog` WRITE;
/*!40000 ALTER TABLE `oplog` DISABLE KEYS */;
INSERT INTO `oplog` VALUES (1,1,'127.0.0.1','添加标签:动画','2021-03-07 01:43:07'),(2,1,'127.0.0.1','添加标签:剧情','2021-03-07 01:49:54'),(3,1,'127.0.0.1','添加电影:《海贼王剧场版10》','2021-03-07 01:52:35'),(4,1,'127.0.0.1','添加电影:《人生密密缝》','2021-03-07 02:28:04'),(5,1,'127.0.0.1','添加标签:喜剧','2021-03-07 02:34:34'),(6,1,'127.0.0.1','添加标签:动作','2021-03-07 02:34:49'),(7,1,'127.0.0.1','添加标签:科幻','2021-03-07 02:34:52'),(8,1,'127.0.0.1','添加标签:爱情','2021-03-07 02:35:21'),(9,1,'127.0.0.1','添加电影:《八美图》','2021-03-07 02:37:38'),(10,1,'127.0.0.1','添加电影:《必是天堂》','2021-03-07 03:10:10'),(11,1,'127.0.0.1','添加电影:《黑侠》','2021-03-16 13:54:38'),(12,1,'127.0.0.1','添加电影:《美少女特攻队 Sucker Punch》','2021-03-16 14:12:11'),(13,1,'127.0.0.1','添加电影:《印度暴徒》','2021-03-16 14:19:03'),(14,1,'127.0.0.1','添加电影:《关云长》','2021-03-17 10:34:21'),(15,1,'127.0.0.1','添加电影:《生之欲》','2021-03-17 10:35:14');
/*!40000 ALTER TABLE `oplog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `preview`
--

DROP TABLE IF EXISTS `preview`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `preview` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `logo` varchar(255) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  UNIQUE KEY `logo` (`logo`),
  KEY `ix_preview_addtime` (`addtime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `preview`
--

LOCK TABLES `preview` WRITE;
/*!40000 ALTER TABLE `preview` DISABLE KEYS */;
/*!40000 ALTER TABLE `preview` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `auths` varchar(600) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_role_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'超级管理员','','2021-03-05 19:25:27');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tag`
--

DROP TABLE IF EXISTS `tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tag` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_tag_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tag`
--

LOCK TABLES `tag` WRITE;
/*!40000 ALTER TABLE `tag` DISABLE KEYS */;
INSERT INTO `tag` VALUES (1,'动画','2021-03-07 01:43:07'),(2,'剧情','2021-03-07 01:49:54'),(3,'喜剧','2021-03-07 02:34:34'),(4,'动作','2021-03-07 02:34:49'),(5,'科幻','2021-03-07 02:34:52'),(6,'爱情','2021-03-07 02:35:21');
/*!40000 ALTER TABLE `tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(11) DEFAULT NULL,
  `info` text,
  `face` varchar(255) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  `uuid` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `face` (`face`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_user_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'test','pbkdf2:sha256:150000$i80ncZh5$c81812f68c606b2d9a51d837d622e91facaa59e934ba5cb6515b831bca19b050','test@126.com','13971041228','','2021030701301475e2a8628d36442da244b01cf71352e6.jpeg','2021-03-05 21:40:09','2ee7a4bcf9fc43e49e36a3c8a51c1e73');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userlog`
--

DROP TABLE IF EXISTS `userlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userlog` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_userlog_addtime` (`addtime`),
  CONSTRAINT `userlog_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userlog`
--

LOCK TABLES `userlog` WRITE;
/*!40000 ALTER TABLE `userlog` DISABLE KEYS */;
INSERT INTO `userlog` VALUES (1,1,'127.0.0.1','2021-03-05 21:40:17'),(2,1,'127.0.0.1','2021-03-07 03:01:21'),(3,1,'127.0.0.1','2021-03-07 05:21:21'),(4,1,'127.0.0.1','2021-03-16 00:51:58'),(5,1,'127.0.0.1','2021-03-16 13:46:54');
/*!40000 ALTER TABLE `userlog` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-03-17 11:07:14
