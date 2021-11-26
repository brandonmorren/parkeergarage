SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `nrplaat` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NULL,
  `password` varchar(50) NULL,
  `nummerplaat` varchar(50) NOT NULL,
  `voornaam` varchar(50) NULL,
  `achternaam` varchar(50) NULL,
  `parkingspot` INT NULL,
  `automodel` INT NULL,
  `aankomst` datetime DEFAULT CURRENT_TIMESTAMP,
  `vertrek` datetime DEFAULT CURRENT_TIMESTAMP,
  `tebetalen` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nummerplaat` (`nummerplaat`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;
