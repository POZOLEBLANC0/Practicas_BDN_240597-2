-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: db_test_7b
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tb_logs`
--

DROP TABLE IF EXISTS `tb_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_logs` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `table_name` varchar(80) NOT NULL,
  `table_operation` enum('Create','Read','Update','Delete') DEFAULT NULL,
  `db_user` varchar(80) NOT NULL,
  `operation_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `table_description` text NOT NULL,
  `operation_status` bit(1) DEFAULT b'1',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_logs`
--

LOCK TABLES `tb_logs` WRITE;
/*!40000 ALTER TABLE `tb_logs` DISABLE KEYS */;
INSERT INTO `tb_logs` VALUES (1,'tb_users','Create','root@localhost','2026-09-10 10:22:35','Usuario creado. ID= 3, email=240597@uytxicotepec.edu.mx,nick =POZOLE, creation_date=2026-09-10 10:22:35, status=',_binary ''),(2,'tb_users','Create','root@localhost','2026-09-10 10:24:58','Usuario creado. ID= 4, email=240902@utxicotepec.edu.mx,nick =MaiLov, creation_date=2026-09-10 10:24:58, status=',_binary ''),(3,'tb_users','Create','root@localhost','2026-09-10 10:25:11','Usuario creado. ID= 5, email=240904@utxicotepec.edu.mx,nick =Poncho, creation_date=2026-09-10 10:25:11, status=',_binary ''),(4,'tb_users','Create','root@localhost','2026-09-10 10:25:29','Usuario creado. ID= 6, email=240045@utxicotepec.edu.mx,nick =Carton, creation_date=2026-09-10 10:25:29, status=',_binary ''),(5,'tb_users','Create','marco.ramirez@DESKTOP-1FPT0T3','2026-09-10 10:51:24','Usuario creado. ID= 7, email=marco.ramirez@utxicotepec.edu.mx,nick =MTI-MarcoRH, creation_date=2026-09-10 10:51:24, status=',_binary ''),(6,'tb_users','Create','marco.ramirez@DESKTOP-1FPT0T3','2026-09-10 10:53:48','Usuario creado. ID= 8, email=domingo.mejia@hotmail.com,nick =DomingoFC, creation_date=2026-09-10 10:53:48, status=',_binary ''),(7,'tb_users','Create','marco.ramirez@DESKTOP-1FPT0T3','2026-09-10 10:54:32','Usuario creado. ID= 9, email=carolina55@gmail.com,nick =Super Caro, creation_date=2026-09-10 10:54:32, status=',_binary ''),(8,'tb_users','Update','root@localhost','2026-09-10 11:21:18','Usuario actualizado. ID=3, email anterior: 240597@uytxicotepec.edu.mx -> nuevo: 240597@utxicotepec.edu.mx, nick anterior: POZOLE -> nuevo: POZOLE, status anterior:  -> nuevo: ',_binary ''),(9,'tb_users','Delete','root@localhost','2026-09-10 11:22:30','Usuario eliminado. ID=5, email=240904@utxicotepec.edu.mx, nick=Poncho, creation_date=2026-09-10 10:25:11, status=',_binary ''),(10,'tb_users','Update','marco.ramirez@DESKTOP-1FPT0T3','2026-09-10 11:26:26','Usuario actualizado. ID=9, email anterior: carolina55@gmail.com -> nuevo: carolina55@gmail.com, nick anterior: Super Caro -> nuevo: Carito, status anterior:  -> nuevo: ',_binary ''),(11,'tb_users','Delete','marco.ramirez@DESKTOP-1FPT0T3','2026-09-10 11:28:40','Usuario eliminado. ID=6, email=240045@utxicotepec.edu.mx, nick=Carton, creation_date=2026-09-10 10:25:29, status=',_binary '');
/*!40000 ALTER TABLE `tb_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_users`
--

DROP TABLE IF EXISTS `tb_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_users` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `nick` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `creation_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_update` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `last_login` datetime DEFAULT NULL,
  `status` bit(1) DEFAULT b'1',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `nick` (`nick`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_users`
--

LOCK TABLES `tb_users` WRITE;
/*!40000 ALTER TABLE `tb_users` DISABLE KEYS */;
INSERT INTO `tb_users` VALUES (3,'240597@utxicotepec.edu.mx','POZOLE','99b80047919135e419e068ff7fd150a2','2026-09-10 10:22:35','2026-09-10 11:21:18',NULL,_binary ''),(4,'240902@utxicotepec.edu.mx','MaiLov','81dc9bdb52d04dc20036dbd8313ed055','2026-09-10 10:24:58',NULL,NULL,_binary ''),(7,'marco.ramirez@utxicotepec.edu.mx','MTI-MarcoRH','871534c2971fceb021437786bc940bd2','2026-09-10 10:51:24',NULL,NULL,_binary ''),(8,'domingo.mejia@hotmail.com','DomingoFC','83f4be3a4b45a4d99c8f127e37a80cb0','2026-09-10 10:53:48',NULL,NULL,_binary ''),(9,'carolina55@gmail.com','Carito','01cfcd4f6b8770febfb40cb906715822','2026-09-10 10:54:32','2026-09-10 11:26:26',NULL,_binary '');
/*!40000 ALTER TABLE `tb_users` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_users_after_insert` AFTER INSERT ON `tb_users` FOR EACH ROW BEGIN
              INSERT INTO tb_logs(
                      table_name,
                      table_operation,
                      db_user,
                      table_description,
                      operation_date,
                      operation_status
              )
              values (
                      'tb_users',
                      'Create',
     USER(),
     CONCAT(
     'Usuario creado. ID= ',NEW.ID,
     ', email=', NEW.email,
     ',nick =', NEW.nick,
     ', creation_date=', NEW.creation_date,
     ', status=', NEW.status
     ),
     CURRENT_TIMESTAMP,
     b'1'
     );
     END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_users_after_update` AFTER UPDATE ON `tb_users` FOR EACH ROW BEGIN
    INSERT INTO tb_logs(
        table_name,
        table_operation,
        db_user,
        table_description,
        operation_date,
        operation_status
    )
    VALUES (
        'tb_users',
        'Update',
        USER(),
        CONCAT(
            'Usuario actualizado. ID=', NEW.ID, 
            ', email anterior: ', OLD.email, ' -> nuevo: ', NEW.email,
            ', nick anterior: ', OLD.nick, ' -> nuevo: ', NEW.nick,
            ', status anterior: ', OLD.status, ' -> nuevo: ', NEW.status
        ),
        CURRENT_TIMESTAMP,
        b'1'
    );
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_users_after_delete` AFTER DELETE ON `tb_users` FOR EACH ROW BEGIN
    INSERT INTO tb_logs(
        table_name,
        table_operation,
        db_user,
        table_description,
        operation_date,
        operation_status
    )
    VALUES (
        'tb_users',
        'Delete',
        USER(),
        CONCAT(
            'Usuario eliminado. ID=', OLD.ID,
            ', email=', OLD.email,
            ', nick=', OLD.nick,
            ', creation_date=', OLD.creation_date,
            ', status=', OLD.status
        ),
        CURRENT_TIMESTAMP,
        b'1'
    );
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-10 13:13:20
