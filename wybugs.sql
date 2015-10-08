/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50625
 Source Host           : localhost
 Source Database       : scrapy

 Target Server Type    : MySQL
 Target Server Version : 50625
 File Encoding         : utf-8

 Date: 10/08/2015 16:00:57 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `wybugs`
-- ----------------------------
DROP TABLE IF EXISTS `wybugs`;
CREATE TABLE `wybugs` (
  `id` int(8) unsigned NOT NULL AUTO_INCREMENT,
  `fbid` varchar(20),
  `title` varchar(255) NOT NULL,
  `corp` varchar(100) NOT NULL,
  `author` varchar(100) NOT NULL,
  `type` varchar(255),
  `submit_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `confirm_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `open_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `status` varchar(60) NOT NULL,
  `user_level` char(2) NOT NULL,
  `result_level` char(2),
  `user_rank` smallint(2),
  `result_rank` smallint(2),
  `corp_reply` text,
  `attention_num` smallint(4) DEFAULT NULL,
  `collection_num` smallint(4) DEFAULT NULL,
  `reply_num` smallint(4) DEFAULT NULL,
  `is_lightning` tinyint(1) DEFAULT '0',
  `dollar_num` smallint(1) DEFAULT '0',
  `description` text,
  `detail` text,
  `poc` text,
  `patch` text,
  `crawl_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `fbid` (`fbid`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=130 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
