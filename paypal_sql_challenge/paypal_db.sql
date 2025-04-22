CREATE DATABASE  IF NOT EXISTS `paypal` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `paypal`;
-- MySQL dump 10.13  Distrib 8.0.42, for Linux (x86_64)
--
-- Host: localhost    Database: paypal
-- ------------------------------------------------------
-- Server version	8.0.42

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
-- Table structure for table `merchants`
--

DROP TABLE IF EXISTS `merchants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `merchants` (
  `merchant_id` int NOT NULL,
  `country` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`merchant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `merchants`
--

LOCK TABLES `merchants` WRITE;
/*!40000 ALTER TABLE `merchants` DISABLE KEYS */;
INSERT INTO `merchants` VALUES (101,'germany'),(102,'france'),(103,'italy'),(104,'spain'),(105,'germany');
/*!40000 ALTER TABLE `merchants` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subscriptions`
--

DROP TABLE IF EXISTS `subscriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subscriptions` (
  `subscription_id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `subscription_start_date` date DEFAULT NULL,
  `subscription_end_date` date DEFAULT NULL,
  `subscription_amount` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`subscription_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `subscriptions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subscriptions`
--

LOCK TABLES `subscriptions` WRITE;
/*!40000 ALTER TABLE `subscriptions` DISABLE KEYS */;
INSERT INTO `subscriptions` VALUES (201,1,'2024-01-01','2025-01-01',99.99),(202,2,'2023-01-15','2023-02-15',89.99),(203,3,'2023-02-20','2024-02-20',79.99),(204,4,'2024-03-05','2025-03-05',119.99),(205,5,'2024-03-15','2025-03-15',99.99),(206,6,'2025-04-01','2025-05-01',89.99),(207,7,'2024-04-10','2025-04-10',109.99),(208,8,'2024-04-15','2024-05-15',129.99),(209,9,'2023-04-18','2024-01-01',89.99),(210,10,'2024-02-01','2025-01-01',99.99);
/*!40000 ALTER TABLE `subscriptions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaction_details`
--

DROP TABLE IF EXISTS `transaction_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaction_details` (
  `transaction_id` int NOT NULL,
  `payment_method` enum('credit_card','paypal','bank_transfer') DEFAULT NULL,
  PRIMARY KEY (`transaction_id`),
  CONSTRAINT `transaction_details_ibfk_1` FOREIGN KEY (`transaction_id`) REFERENCES `transactions` (`transaction_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction_details`
--

LOCK TABLES `transaction_details` WRITE;
/*!40000 ALTER TABLE `transaction_details` DISABLE KEYS */;
INSERT INTO `transaction_details` VALUES (1001,'credit_card'),(1002,'paypal'),(1003,'bank_transfer'),(1004,'credit_card'),(1005,'credit_card'),(1006,'paypal'),(1007,'bank_transfer'),(1008,'credit_card'),(1009,'paypal'),(1010,'bank_transfer'),(1011,'credit_card'),(1012,'paypal'),(1013,'credit_card'),(1014,'bank_transfer'),(1015,'credit_card');
/*!40000 ALTER TABLE `transaction_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `transaction_id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `merchant_id` int DEFAULT NULL,
  `transaction_amount` decimal(10,2) DEFAULT NULL,
  `transaction_date` date DEFAULT NULL,
  `transaction_status` enum('success','failed','fraudulent') DEFAULT NULL,
  `payment_method` enum('credit_card','paypal','bank_transfer') DEFAULT NULL,
  PRIMARY KEY (`transaction_id`),
  KEY `user_id` (`user_id`),
  KEY `merchant_id` (`merchant_id`),
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `transactions_ibfk_2` FOREIGN KEY (`merchant_id`) REFERENCES `merchants` (`merchant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES (1001,1,101,120.50,'2024-01-31','success','paypal'),(1002,2,102,250.00,'2024-04-02','failed','credit_card'),(1003,3,103,75.00,'2025-04-03','fraudulent','paypal'),(1004,4,104,95.99,'2024-04-04','success','paypal'),(1005,5,105,135.75,'2025-03-05','success','bank_transfer'),(1006,6,101,45.00,'2024-04-06','failed','paypal'),(1007,7,102,180.00,'2025-01-01','success','credit_card'),(1008,8,103,220.00,'2024-04-08','success','bank_transfer'),(1009,9,104,310.40,'2024-04-09','success','paypal'),(1010,10,105,95.00,'2025-02-12','fraudulent','bank_transfer'),(1011,11,101,205.30,'2024-04-11','success','credit_card'),(1012,12,102,160.50,'2024-04-12','failed','bank_transfer'),(1013,13,103,88.88,'2024-04-13','success','credit_card'),(1014,14,104,105.00,'2024-04-14','success','paypal'),(1015,15,105,210.10,'2024-04-15','success','credit_card');
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL,
  `signup_date` date DEFAULT NULL,
  `country` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'2024-01-01','germany'),(2,'2024-01-15','france'),(3,'2024-02-20','italy'),(4,'2024-03-05','spain'),(5,'2024-03-15','germany'),(6,'2024-04-01','poland'),(7,'2024-04-10','germany'),(8,'2024-04-15','austria'),(9,'2024-04-18','germany'),(10,'2024-04-19','sweden'),(11,'2024-04-20','france'),(12,'2024-04-21','germany'),(13,'2024-01-01','norway'),(14,'2024-04-23','denmark'),(15,'2024-04-24','germany'),(16,'2024-04-25','italy'),(17,'2024-04-26','france'),(18,'2024-04-27','germany'),(19,'2024-04-28','austria'),(20,'2024-04-29','spain');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-22 16:46:54
