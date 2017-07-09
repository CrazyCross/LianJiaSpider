
DROP TABLE IF EXISTS `tb_renthouse`;
CREATE TABLE `tb_renthouse` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name`  varchar(1000) not NULL,
  `price`  varchar(10) DEFAULT NULL,
  `address` varchar(1000) DEFAULT NULL,
  `houseType` varchar(1000) DEFAULT NULL,
  `time` varchar(1000) DEFAULT NULL,
  `meters` varchar(10) DEFAULT NULL,
  `region` varchar(1000) DEFAULT NULL,
  `towards` varchar(1000) DEFAULT NULL,
  `url` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`,`name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;



