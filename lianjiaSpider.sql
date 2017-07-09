DROP TABLE IF EXISTS `tb_ershouhouse_new`;
CREATE TABLE `tb_ershouhouse_new` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `district`  varchar(1000) DEFAULT NULL,
  `name`  varchar(1000) DEFAULT NULL,
  `totalPrice` varchar(1000) DEFAULT NULL,
  `perPrice` varchar(1000) DEFAULT NULL,
  `communityName` varchar(1000) DEFAULT NULL,
  `houseType` varchar(1000) DEFAULT NULL,
  `area` varchar(1000) DEFAULT NULL,
  `houseTowards` varchar(1000) DEFAULT NULL,
  `houseDec` varchar(1000) DEFAULT NULL,
  `hasElevator` varchar(1000) DEFAULT NULL,
  `positionInfo` varchar(1000) DEFAULT NULL,
  `followNum` varchar(1000) DEFAULT NULL,
  `viewTime` varchar(1000) DEFAULT NULL,
  `publishTime` varchar(1000) DEFAULT NULL,
  `url` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;
