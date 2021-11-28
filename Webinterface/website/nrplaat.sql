SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `nrplaat` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NULL,
  `voornaam` varchar(50) NULL,
  `achternaam` varchar(50) NULL,
  `straat_huisnummer` varchar(100) NULL,
  `gemeente_postcode` varchar(100) NULL,
  `bank` varchar(50) NULL,
  `nummerplaat` varchar(50) NOT NULL,
  `parkingspot` INT NULL,
  `aankomst` datetime DEFAULT CURRENT_TIMESTAMP,
  `vertrek` datetime NULL,
  `tebetalen` FLOAT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nummerplaat` (`nummerplaat`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;


CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NULL UNIQUE,
  `password` varchar(255) NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);


CREATE TABLE IF NOT EXISTS `parkingspot` (
  `parkingspot` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(50) NULL,
  `aankomst` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`parkingspot`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;


INSERT INTO `parkingspot`(`parkingspot`, `status`, `aankomst`) 
VALUES 
(1,'beschikbaar',CURRENT_TIMESTAMP),
(2,'beschikbaar',CURRENT_TIMESTAMP),
(3,'beschikbaar',CURRENT_TIMESTAMP),
(4,'beschikbaar',CURRENT_TIMESTAMP);

