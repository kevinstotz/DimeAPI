CREATE DATABASE  IF NOT EXISTS `DimeAPI` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `DimeAPI`;
-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: localhost    Database: DimeAPI-dev
-- ------------------------------------------------------
-- Server version	5.7.20-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `DimeAPI_currency`
--

DROP TABLE IF EXISTS `DimeAPI_currency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DimeAPI_currency` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `symbol` varchar(10) NOT NULL,
  `coinName` varchar(30) NOT NULL,
  `fullName` varchar(100) NOT NULL,
  `totalCoinSupply` double NOT NULL,
  `icon` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `DimeAPI_currencyhistory`
--

DROP TABLE IF EXISTS `DimeAPI_currencyhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DimeAPI_currencyhistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `price` double NOT NULL,
  `marketCap` double NOT NULL,
  `totalCoinSupply` double NOT NULL,
  `currency_id` int(11) NOT NULL,
  `timestamp` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `DimeAPI_currencyhist_currency_id_3447e405_fk_DimeAPI_c` (`currency_id`),
  CONSTRAINT `DimeAPI_currencyhist_currency_id_3447e405_fk_DimeAPI_c` FOREIGN KEY (`currency_id`) REFERENCES `DimeAPI_currency` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `DimeAPI_currencyxchangemap`
--

DROP TABLE IF EXISTS `DimeAPI_currencyxchangemap`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DimeAPI_currencyxchangemap` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `currency_id` int(11) NOT NULL,
  `currencyXChange_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `DimeAPI_currencyxcha_currency_id_d15fd797_fk_DimeAPI_c` (`currency_id`),
  KEY `DimeAPI_currencyxcha_currencyXChange_id_8fd4a5fc_fk_DimeAPI_x` (`currencyXChange_id`),
  CONSTRAINT `DimeAPI_currencyxcha_currencyXChange_id_8fd4a5fc_fk_DimeAPI_x` FOREIGN KEY (`currencyXChange_id`) REFERENCES `DimeAPI_xchangecurrency` (`id`),
  CONSTRAINT `DimeAPI_currencyxcha_currency_id_d15fd797_fk_DimeAPI_c` FOREIGN KEY (`currency_id`) REFERENCES `DimeAPI_currency` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `DimeAPI_customuser`
--

DROP TABLE IF EXISTS `DimeAPI_customuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DimeAPI_customuser` (
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `inserted` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_logged_in` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `status_id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`),
  KEY `DimeAPI_customuser_status_id_bec05ab7_fk_DimeAPI_userstatus_id` (`status_id`),
  CONSTRAINT `DimeAPI_customuser_status_id_bec05ab7_fk_DimeAPI_userstatus_id` FOREIGN KEY (`status_id`) REFERENCES `DimeAPI_userstatus` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `DimeAPI_customuser_groups`
--

DROP TABLE IF EXISTS `DimeAPI_customuser_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DimeAPI_customuser_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `customuser_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `DimeAPI_customuser_groups_customuser_id_group_id_a58a4e2a_uniq` (`customuser_id`,`group_id`),
  KEY `DimeAPI_customuser_groups_group_id_23754c7d_fk_auth_group_id` (`group_id`),
  CONSTRAINT `DimeAPI_customuser_g_customuser_id_4381ae82_fk_DimeAPI_c` FOREIGN KEY (`customuser_id`) REFERENCES `DimeAPI_customuser` (`id`),
  CONSTRAINT `DimeAPI_customuser_groups_group_id_23754c7d_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `DimeAPI_customuser_user_permissions`
--

DROP TABLE IF EXISTS `DimeAPI_customuser_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DimeAPI_customuser_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `customuser_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `DimeAPI_customuser_user__customuser_id_permission_ea55845e_uniq` (`customuser_id`,`permission_id`),
  KEY `DimeAPI_customuser_u_permission_id_69cd9d67_fk_auth_perm` (`permission_id`),
  CONSTRAINT `DimeAPI_customuser_u_customuser_id_cb7bde05_fk_DimeAPI_c` FOREIGN KEY (`customuser_id`) REFERENCES `DimeAPI_customuser` (`id`),
  CONSTRAINT `DimeAPI_customuser_u_permission_id_69cd9d67_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `DimeAPI_DimeMutualFund`
--

DROP TABLE IF EXISTS `DimeAPI_DimeMutualFund`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DimeAPI_DimeMutualFund` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rebalanceDate` date NOT NULL,
  `rank` int(11) NOT NULL,
  `level` double NOT NULL,
  `rebalancePrice` double NOT NULL,
  `marketCap` bigint(20) NOT NULL,
  `percentOfDime` double NOT NULL,
  `amount` double NOT NULL,
  `rebalanceValue` double NOT NULL,
  `endPrice` double NOT NULL,
  `endValue` double NOT NULL,
  `currency_id` int(11) NOT NULL,
  `period_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `DimeAPI_DimeMutualFund_currency_id_af15b874_fk_DimeAPI_currency_id` (`currency_id`),
  KEY `DimeAPI_DimeMutualFund_period_id_86d63b33_fk_DimeAPI_period_id` (`period_id`),
  CONSTRAINT `DimeAPI_DimeMutualFund_currency_id_af15b874_fk_DimeAPI_currency_id` FOREIGN KEY (`currency_id`) REFERENCES `DimeAPI_currency` (`id`),
  CONSTRAINT `DimeAPI_DimeMutualFund_period_id_86d63b33_fk_DimeAPI_period_id` FOREIGN KEY (`period_id`) REFERENCES `DimeAPI_period` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `DimeAPI_emailaddress`
--

DROP TABLE IF EXISTS `DimeAPI_emailaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DimeAPI_emailaddress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `inserted` datetime(6) NOT NULL,
  `status_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `DimeAPI_emailaddress_status_id_eff8cc3b_fk_DimeAPI_e` (`status_id`),
  KEY `DimeAPI_emailaddress_user_id_6e22e2cc_fk_DimeAPI_customuser_id` (`user_id`),
  CONSTRAINT `DimeAPI_emailaddress_status_id_eff8cc3b_fk_DimeAPI_e` FOREIGN KEY (`status_id`) REFERENCES `DimeAPI_emailaddressstatus` (`id`),
  CONSTRAINT `DimeAPI_emailaddress_user_id_6e22e2cc_fk_DimeAPI_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `DimeAPI_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `DimeAPI_emailaddressstatus`
--

DROP TABLE IF EXISTS `DimeAPI_emailaddressstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DimeAPI_emailaddressstatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `DimeAPI_emailtemplate`
--

DROP TABLE IF EXISTS `DimeAPI_emailtemplate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DimeAPI_emailtemplate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subject` varchar(60) NOT NULL,
  `fromAddress` varchar(50) NOT NULL,
  `htmlFilename` varchar(100) DEFAULT NULL,
  `textFilename` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `DimeAPI_name`
--

DROP TABLE IF EXISTS `DimeAPI_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DimeAPI_name` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `inserted` datetime(6) NOT NULL,
  `type_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `DimeAPI_name_type_id_3bfc10fd_fk_DimeAPI_nametype_id` (`type_id`),
  KEY `DimeAPI_name_user_id_c9bd10f0_fk_DimeAPI_customuser_id` (`user_id`),
  CONSTRAINT `DimeAPI_name_type_id_3bfc10fd_fk_DimeAPI_nametype_id` FOREIGN KEY (`type_id`) REFERENCES `DimeAPI_nametype` (`id`),
  CONSTRAINT `DimeAPI_name_user_id_c9bd10f0_fk_DimeAPI_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `DimeAPI_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `DimeAPI_nametype`
--

DROP TABLE IF EXISTS `DimeAPI_nametype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DimeAPI_nametype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `DimeAPI_network`
--

DROP TABLE IF EXISTS `DimeAPI_network`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DimeAPI_network` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `number` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `url` varchar(100) NOT NULL,
  `queryUrl` varchar(100) NOT NULL,
  `api` varchar(42) NOT NULL,
  `genesis` int(11) NOT NULL,
  `lastBlockChecked` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `DimeAPI_newsletter`
--

DROP TABLE IF EXISTS `DimeAPI_newsletter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DimeAPI_newsletter` (
  `email` varchar(254) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `DimeAPI_notification`
--

DROP TABLE IF EXISTS `DimeAPI_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DimeAPI_notification` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fromUser` int(11) NOT NULL,
  `toUser` int(11) NOT NULL,
  `message` int(11) NOT NULL,
  `status_id` int(11) NOT NULL,
  `type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `DimeAPI_notification_status_id_394f58bd_fk_DimeAPI_n` (`status_id`),
  KEY `DimeAPI_notification_type_id_151be984_fk_DimeAPI_n` (`type_id`),
  CONSTRAINT `DimeAPI_notification_status_id_394f58bd_fk_DimeAPI_n` FOREIGN KEY (`status_id`) REFERENCES `DimeAPI_notificationstatus` (`id`),
  CONSTRAINT `DimeAPI_notification_type_id_151be984_fk_DimeAPI_n` FOREIGN KEY (`type_id`) REFERENCES `DimeAPI_notificationtype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `DimeAPI_notificationstatus`
--

DROP TABLE IF EXISTS `DimeAPI_notificationstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DimeAPI_notificationstatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `DimeAPI_notificationtype`
--

DROP TABLE IF EXISTS `DimeAPI_notificationtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DimeAPI_notificationtype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `DimeAPI_password`
--

DROP TABLE IF EXISTS `DimeAPI_password`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DimeAPI_password` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `DimeAPI_passwordreset`
--

DROP TABLE IF EXISTS `DimeAPI_passwordreset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DimeAPI_passwordreset` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `authorizationCode` varchar(20) NOT NULL,
  `clicked` datetime(6) NOT NULL,
  `inserted` datetime(6) NOT NULL,
  `status_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `DimeAPI_passwordrese_status_id_83e9d432_fk_DimeAPI_p` (`status_id`),
  KEY `DimeAPI_passwordreset_user_id_b2f1a479_fk_DimeAPI_customuser_id` (`user_id`),
  CONSTRAINT `DimeAPI_passwordrese_status_id_83e9d432_fk_DimeAPI_p` FOREIGN KEY (`status_id`) REFERENCES `DimeAPI_passwordresetstatus` (`id`),
  CONSTRAINT `DimeAPI_passwordreset_user_id_b2f1a479_fk_DimeAPI_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `DimeAPI_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `DimeAPI_passwordresetstatus`
--

DROP TABLE IF EXISTS `DimeAPI_passwordresetstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DimeAPI_passwordresetstatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `DimeAPI_period`
--

DROP TABLE IF EXISTS `DimeAPI_period`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DimeAPI_period` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `endDay` int(11) NOT NULL,
  `endMonth` int(11) NOT NULL,
  `endQarter` int(11) NOT NULL,
  `endYear` int(11) NOT NULL,
  `startDay` int(11) NOT NULL,
  `startMonth` int(11) NOT NULL,
  `startQarter` int(11) NOT NULL,
  `startYear` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `DimeAPI_register`
--

DROP TABLE IF EXISTS `DimeAPI_register`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DimeAPI_register` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `firstName` varchar(50) NOT NULL,
  `lastName` varchar(50) NOT NULL,
  `ipAddress` char(39) DEFAULT NULL,
  `deviceInfo_id` int(11) NOT NULL,
  `authorizationCode` varchar(20) NOT NULL,
  `status_id` int(11) NOT NULL,
  `password` varchar(20) NOT NULL,
  `inserted` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `DimeAPI_register_status_id_57c31ff2_fk_DimeAPI_registerstatus_id` (`status_id`),
  KEY `DimeAPI_register_userAgent_id_831a7a38` (`deviceInfo_id`),
  CONSTRAINT `DimeAPI_register_deviceInfo_id_90b34f41_fk_DimeAPI_useragent_id` FOREIGN KEY (`deviceInfo_id`) REFERENCES `DimeAPI_useragent` (`id`),
  CONSTRAINT `DimeAPI_register_status_id_57c31ff2_fk_DimeAPI_registerstatus_id` FOREIGN KEY (`status_id`) REFERENCES `DimeAPI_registerstatus` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `DimeAPI_registerstatus`
--

DROP TABLE IF EXISTS `DimeAPI_registerstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DimeAPI_registerstatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `DimeAPI_useragent`
--

DROP TABLE IF EXISTS `DimeAPI_useragent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DimeAPI_useragent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userAgent` varchar(255) DEFAULT NULL,
  `os` varchar(20) DEFAULT NULL,
  `browser` varchar(20) DEFAULT NULL,
  `device` varchar(20) DEFAULT NULL,
  `os_version` varchar(30) DEFAULT NULL,
  `browser_version` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `DimeAPI_userstatus`
--

DROP TABLE IF EXISTS `DimeAPI_userstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DimeAPI_userstatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(42) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `DimeAPI_xchange`
--

DROP TABLE IF EXISTS `DimeAPI_xchange`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DimeAPI_xchange` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `url` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `DimeAPI_xchangecurrency`
--

DROP TABLE IF EXISTS `DimeAPI_xchangecurrency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DimeAPI_xchangecurrency` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `currency` int(11) NOT NULL,
  `currencyXChange_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `DimeAPI_xchangecurre_currencyXChange_id_59ba4e10_fk_DimeAPI_x` (`currencyXChange_id`),
  CONSTRAINT `DimeAPI_xchangecurre_currencyXChange_id_59ba4e10_fk_DimeAPI_x` FOREIGN KEY (`currencyXChange_id`) REFERENCES `DimeAPI_xchange` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_DimeAPI_customuser_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_DimeAPI_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `DimeAPI_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `oauth2_provider_accesstoken`
--

DROP TABLE IF EXISTS `oauth2_provider_accesstoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oauth2_provider_accesstoken` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `token` varchar(255) NOT NULL,
  `expires` datetime(6) NOT NULL,
  `scope` longtext NOT NULL,
  `application_id` bigint(20) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `oauth2_provider_accesstoken_token_8af090f8_uniq` (`token`),
  KEY `oauth2_provider_acce_user_id_6e4c9a65_fk_DimeAPI_c` (`user_id`),
  KEY `oauth2_provider_accesstoken_application_id_b22886e1_fk` (`application_id`),
  CONSTRAINT `oauth2_provider_acce_user_id_6e4c9a65_fk_DimeAPI_c` FOREIGN KEY (`user_id`) REFERENCES `DimeAPI_customuser` (`id`),
  CONSTRAINT `oauth2_provider_accesstoken_application_id_b22886e1_fk` FOREIGN KEY (`application_id`) REFERENCES `oauth2_provider_application` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `oauth2_provider_application`
--

DROP TABLE IF EXISTS `oauth2_provider_application`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oauth2_provider_application` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `client_id` varchar(100) NOT NULL,
  `redirect_uris` longtext NOT NULL,
  `client_type` varchar(32) NOT NULL,
  `authorization_grant_type` varchar(32) NOT NULL,
  `client_secret` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `skip_authorization` tinyint(1) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `client_id` (`client_id`),
  KEY `oauth2_provider_application_client_secret_53133678` (`client_secret`),
  KEY `oauth2_provider_appl_user_id_79829054_fk_DimeAPI_c` (`user_id`),
  CONSTRAINT `oauth2_provider_appl_user_id_79829054_fk_DimeAPI_c` FOREIGN KEY (`user_id`) REFERENCES `DimeAPI_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `oauth2_provider_grant`
--

DROP TABLE IF EXISTS `oauth2_provider_grant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oauth2_provider_grant` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `code` varchar(255) NOT NULL,
  `expires` datetime(6) NOT NULL,
  `redirect_uri` varchar(255) NOT NULL,
  `scope` longtext NOT NULL,
  `application_id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `oauth2_provider_grant_code_49ab4ddf_uniq` (`code`),
  KEY `oauth2_provider_grant_application_id_81923564_fk` (`application_id`),
  KEY `oauth2_provider_grant_user_id_e8f62af8_fk_DimeAPI_customuser_id` (`user_id`),
  CONSTRAINT `oauth2_provider_grant_application_id_81923564_fk` FOREIGN KEY (`application_id`) REFERENCES `oauth2_provider_application` (`id`),
  CONSTRAINT `oauth2_provider_grant_user_id_e8f62af8_fk_DimeAPI_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `DimeAPI_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `oauth2_provider_refreshtoken`
--

DROP TABLE IF EXISTS `oauth2_provider_refreshtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oauth2_provider_refreshtoken` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `token` varchar(255) NOT NULL,
  `access_token_id` bigint(20) NOT NULL,
  `application_id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `access_token_id` (`access_token_id`),
  UNIQUE KEY `oauth2_provider_refreshtoken_token_d090daa4_uniq` (`token`),
  KEY `oauth2_provider_refreshtoken_application_id_2d1c311b_fk` (`application_id`),
  KEY `oauth2_provider_refr_user_id_da837fce_fk_DimeAPI_c` (`user_id`),
  CONSTRAINT `oauth2_provider_refr_user_id_da837fce_fk_DimeAPI_c` FOREIGN KEY (`user_id`) REFERENCES `DimeAPI_customuser` (`id`),
  CONSTRAINT `oauth2_provider_refreshtoken_access_token_id_775e84e8_fk` FOREIGN KEY (`access_token_id`) REFERENCES `oauth2_provider_accesstoken` (`id`),
  CONSTRAINT `oauth2_provider_refreshtoken_application_id_2d1c311b_fk` FOREIGN KEY (`application_id`) REFERENCES `oauth2_provider_application` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `otp_static_staticdevice`
--

DROP TABLE IF EXISTS `otp_static_staticdevice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `otp_static_staticdevice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `confirmed` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `otp_static_staticdev_user_id_7f9cff2b_fk_DimeAPI_c` (`user_id`),
  CONSTRAINT `otp_static_staticdev_user_id_7f9cff2b_fk_DimeAPI_c` FOREIGN KEY (`user_id`) REFERENCES `DimeAPI_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `otp_static_statictoken`
--

DROP TABLE IF EXISTS `otp_static_statictoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `otp_static_statictoken` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` varchar(16) NOT NULL,
  `device_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `otp_static_statictok_device_id_74b7c7d1_fk_otp_stati` (`device_id`),
  KEY `otp_static_statictoken_token_d0a51866` (`token`),
  CONSTRAINT `otp_static_statictok_device_id_74b7c7d1_fk_otp_stati` FOREIGN KEY (`device_id`) REFERENCES `otp_static_staticdevice` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `otp_totp_totpdevice`
--

DROP TABLE IF EXISTS `otp_totp_totpdevice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `otp_totp_totpdevice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `confirmed` tinyint(1) NOT NULL,
  `key` varchar(80) NOT NULL,
  `step` smallint(5) unsigned NOT NULL,
  `t0` bigint(20) NOT NULL,
  `digits` smallint(5) unsigned NOT NULL,
  `tolerance` smallint(5) unsigned NOT NULL,
  `drift` smallint(6) NOT NULL,
  `last_t` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `otp_totp_totpdevice_user_id_0fb18292_fk_DimeAPI_customuser_id` (`user_id`),
  CONSTRAINT `otp_totp_totpdevice_user_id_0fb18292_fk_DimeAPI_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `DimeAPI_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `two_factor_phonedevice`
--

DROP TABLE IF EXISTS `two_factor_phonedevice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `two_factor_phonedevice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `confirmed` tinyint(1) NOT NULL,
  `number` varchar(128) NOT NULL,
  `key` varchar(40) NOT NULL,
  `method` varchar(4) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `two_factor_phonedevice_user_id_54718003_fk_DimeAPI_customuser_id` (`user_id`),
  CONSTRAINT `two_factor_phonedevice_user_id_54718003_fk_DimeAPI_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `DimeAPI_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-02-11  8:54:08
