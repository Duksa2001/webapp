-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 22, 2023 at 10:05 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `quiz_projekat`
--

-- --------------------------------------------------------

--
-- Table structure for table `quiz`
--

CREATE TABLE `quiz` (
  `id` int(11) NOT NULL,
  `ime` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `quiz`
--

INSERT INTO `quiz` (`id`, `ime`) VALUES
(1, 'Geografija'),
(2, 'Gradovi i reke Srbije'),
(3, 'Python');

-- --------------------------------------------------------

--
-- Table structure for table `quiz_question`
--

CREATE TABLE `quiz_question` (
  `id` int(11) NOT NULL,
  `tekst` varchar(1000) NOT NULL,
  `quiz_id` int(11) NOT NULL,
  `broji` int(11) NOT NULL,
  `odg1` text NOT NULL,
  `odg2` text NOT NULL,
  `odg3` text NOT NULL,
  `odg4` text NOT NULL,
  `tacno` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `quiz_question`
--

INSERT INTO `quiz_question` (`id`, `tekst`, `quiz_id`, `broji`, `odg1`, `odg2`, `odg3`, `odg4`, `tacno`) VALUES
(2, 'Bajna Basta je smestena na obalama reke?', 2, 1, 'Dunava', 'Save', 'Drine', 'Juzne Morave', 3),
(4, 'Kroz Kostolac protice koja reka/', 2, 2, 'Sava', 'Mlava', 'Pcinja', 'Drina', 2),
(5, 'Kroz Valjevo protice koja reka?', 2, 3, 'Kolubara', 'Lim', 'Tamis', 'Tisa', 1),
(21, 'Naredba za unos podataka naziva se?', 3, 1, 'print', 'input', 'if', 'for', 2),
(24, 'Koje je najvece jezero u Italiji?', 1, 1, 'Vico', 'Garda', 'Orta', 'Bolsena', 2),
(25, 'Kroz Aleksinac protice koja reka?', 2, 4, 'Velika Morava', 'Sava', 'Juzna Morava', 'Nisava', 3),
(26, 'Koliko ima nacionalih parkova u Srbiji?', 1, 2, '3', '4', '5', '6', 3),
(27, 'U kojoj drzavi se nalazi izvor reke Dunav?', 1, 3, 'Ceska', 'Nemacka', 'Austrija', 'Svajcerska', 2),
(28, 'Sri lanka se nalazi?', 1, 4, 'Pacifiku', 'Atlantik', 'Indijskom okeanu', 'Tihom okeanu', 3),
(29, 'Najveca pustinja na svetu je?', 1, 5, 'Gobi', 'Antarticka pustinja', 'Sahara', 'Arabijska pustinja', 2),
(30, 'Koliko procenata Afrike obuhvata Sahara?', 1, 6, 'Oko 45%', 'Oko 30%', 'Oko 15%', 'Oko 60%', 2),
(35, 'Sta ce ispisati naredba PRINT(12//10)?', 3, 2, '3', '2', '1', '4', 3),
(36, 'Sta ce ispisati naredba PRINT(12%10)?', 3, 3, '1', '2', '3', '4', 2),
(37, 'Operator // nam omogucava ?', 3, 4, 'Ostatak deljenja', 'Celobrojno deljenje', 'Deljenje', 'Nista od navedenog', 2),
(38, 'Sta ce ispisati naredba PRINT(3+12//10)?', 3, 5, '1', '2', '3', '4', 4),
(39, 'Naredba za ispis podataka naziva se?', 3, 6, 'print', 'input', 'if', 'for', 2),
(68, 'Koja od navedenih zemalja ima veci broj stanovnika?', 1, 7, 'Danska', 'Finska', 'Austrija', 'Bugarska', 3);

-- --------------------------------------------------------

--
-- Table structure for table `quiz_user`
--

CREATE TABLE `quiz_user` (
  `user_id` int(11) NOT NULL,
  `quiz_id` int(11) NOT NULL,
  `broj_tacnih_pitanja` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `quiz_user`
--

INSERT INTO `quiz_user` (`user_id`, `quiz_id`, `broj_tacnih_pitanja`) VALUES
(1, 1, 5),
(1, 2, 0),
(1, 3, 3),
(2, 1, 0),
(2, 2, 0),
(2, 3, 0),
(26, 1, 3),
(26, 2, 2),
(26, 3, 0);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `ime` varchar(100) NOT NULL,
  `prezime` varchar(100) NOT NULL,
  `rola` varchar(100) NOT NULL DEFAULT 'user',
  `score` int(100) NOT NULL,
  `lozinka` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `ime`, `prezime`, `rola`, `score`, `lozinka`) VALUES
(1, 'dusan', 'dusan', 'admin', 8, 'pbkdf2:sha256:260000$uEX1r3rop4F96qBq$271d42a15d1167dc3e1983f1431b49c91aac2ee1f19569ac13e89ebde1553710'),
(2, 'milan', 'milan', 'admin', 0, 'pbkdf2:sha256:260000$kaifMIBDVJhOs0TZ$d4c93a3f3c1f48901685377d18434023c9f24c56928a4800379a92a7635d2eb5'),
(26, 'djole', 'djole', 'user', 5, 'pbkdf2:sha256:260000$kWl3fh2MVh4jmYRO$560c6ea34a7ec54b7bb8106e6b45bf0b075190802dfa02c354629b9997071a34');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `quiz`
--
ALTER TABLE `quiz`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `quiz_question`
--
ALTER TABLE `quiz_question`
  ADD PRIMARY KEY (`id`),
  ADD KEY `quiz_id` (`quiz_id`);

--
-- Indexes for table `quiz_user`
--
ALTER TABLE `quiz_user`
  ADD KEY `user_id` (`user_id`),
  ADD KEY `quiz_id` (`quiz_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `quiz`
--
ALTER TABLE `quiz`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `quiz_question`
--
ALTER TABLE `quiz_question`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=87;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `quiz_question`
--
ALTER TABLE `quiz_question`
  ADD CONSTRAINT `quiz_id` FOREIGN KEY (`quiz_id`) REFERENCES `quiz` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `quiz_user`
--
ALTER TABLE `quiz_user`
  ADD CONSTRAINT `quiz_user_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `quiz_user_ibfk_2` FOREIGN KEY (`quiz_id`) REFERENCES `quiz` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
