/*
Navicat MySQL Data Transfer

Source Server         : toshare
Source Server Version : 50556
Source Host           : 192.168.151.213:3306
Source Database       : kday_qfq

Target Server Type    : MYSQL
Target Server Version : 50556
File Encoding         : 65001

Date: 2018-12-07 21:59:53
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for stock_basic
-- ----------------------------
DROP TABLE IF EXISTS `stock_basic`;
CREATE TABLE `stock_basic` (
  `ts_code` char(9) NOT NULL,
  `symbol` char(6) DEFAULT NULL,
  `name` char(12) DEFAULT NULL,
  `area` char(20) DEFAULT NULL,
  `industry` char(50) DEFAULT NULL,
  `fullname` varchar(200) DEFAULT NULL,
  `enname` varchar(100) DEFAULT NULL,
  `market` char(50) DEFAULT NULL,
  `exchange` char(20) DEFAULT NULL,
  `curr_type` char(10) DEFAULT NULL,
  `list_status` char(10) DEFAULT NULL,
  `list_date` datetime DEFAULT NULL,
  `delist_date` datetime DEFAULT NULL,
  `is_hs` char(2) DEFAULT NULL,
  PRIMARY KEY (`ts_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
