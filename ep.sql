-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jun 18, 2022 at 05:27 PM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 7.4.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ep`
--

-- --------------------------------------------------------

--
-- Table structure for table `cards`
--

CREATE TABLE `cards` (
  `id` int(1) NOT NULL,
  `user_id` int(11) NOT NULL,
  `merch_id` int(11) NOT NULL,
  `card_id` varchar(50) DEFAULT NULL,
  `Holder` varchar(100) NOT NULL,
  `Status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `collect`
--

CREATE TABLE `collect` (
  `id` int(11) NOT NULL,
  `merch_id` int(11) NOT NULL,
  `paylink_id` int(11) DEFAULT NULL,
  `invoice_id` int(11) DEFAULT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Gateway` varchar(100) NOT NULL,
  `tx_id` varchar(100) NOT NULL,
  `tx_ref` varchar(100) DEFAULT NULL,
  `Data` text NOT NULL,
  `Amount` float NOT NULL,
  `Fees` float NOT NULL,
  `Currency` varchar(25) NOT NULL,
  `Comment` text NOT NULL,
  `Initiated` timestamp NOT NULL DEFAULT current_timestamp(),
  `Confirmed` timestamp NULL DEFAULT NULL,
  `Attached` text NOT NULL,
  `for_ex` int(11) DEFAULT NULL,
  `Status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `exchange`
--

CREATE TABLE `exchange` (
  `id` int(11) NOT NULL,
  `collect_id` int(11) NOT NULL,
  `Amount` float NOT NULL,
  `_from` varchar(25) NOT NULL,
  `_to` varchar(25) NOT NULL,
  `Comments` text NOT NULL,
  `Status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `merchant`
--

CREATE TABLE `merchant` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `Kind` varchar(50) NOT NULL,
  `Name` text NOT NULL,
  `Location` text NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Logo` text DEFAULT NULL,
  `Pub_Key` text DEFAULT NULL,
  `Sec_Key` text DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT current_timestamp(),
  `Comment` text NOT NULL,
  `Status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `mgurush`
--

CREATE TABLE `mgurush` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `merch_id` int(11) DEFAULT NULL,
  `Kind` varchar(25) NOT NULL,
  `tx_ref` varchar(25) NOT NULL,
  `Recieved` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `Amount` int(11) NOT NULL,
  `Phone` varchar(25) NOT NULL,
  `Comments` text NOT NULL,
  `Status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `paylink`
--

CREATE TABLE `paylink` (
  `id` int(11) NOT NULL,
  `merch_id` int(11) NOT NULL,
  `Name` text NOT NULL,
  `Kind` varchar(25) NOT NULL,
  `Description` text NOT NULL,
  `Amount` int(11) DEFAULT NULL,
  `Status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `payout`
--

CREATE TABLE `payout` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `merchant_id` int(11) NOT NULL,
  `Kind` varchar(50) NOT NULL,
  `Bank` varchar(100) NOT NULL,
  `Currency` varchar(25) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Number` varchar(100) NOT NULL,
  `Comment` text NOT NULL,
  `Status` int(11) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `f_name` varchar(50) NOT NULL,
  `l_name` varchar(50) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Phone` varchar(50) NOT NULL,
  `Password` varchar(50) NOT NULL,
  `Created` timestamp NOT NULL DEFAULT current_timestamp(),
  `Comment` text NOT NULL,
  `Status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `withdraw`
--

CREATE TABLE `withdraw` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `merch_id` int(11) NOT NULL,
  `Amount` float NOT NULL,
  `Currency` varchar(25) NOT NULL,
  `payout_id` int(11) DEFAULT NULL,
  `Fee` float NOT NULL,
  `Initiated` timestamp NOT NULL DEFAULT current_timestamp(),
  `Completed` timestamp NULL DEFAULT NULL,
  `Comment` text NOT NULL,
  `Status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `xrate`
--

CREATE TABLE `xrate` (
  `id` int(11) NOT NULL,
  `from_cur` varchar(25) NOT NULL,
  `to_cur` varchar(25) NOT NULL,
  `amount` float NOT NULL,
  `Date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cards`
--
ALTER TABLE `cards`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `collect`
--
ALTER TABLE `collect`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `exchange`
--
ALTER TABLE `exchange`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `merchant`
--
ALTER TABLE `merchant`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `mgurush`
--
ALTER TABLE `mgurush`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `paylink`
--
ALTER TABLE `paylink`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `payout`
--
ALTER TABLE `payout`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `withdraw`
--
ALTER TABLE `withdraw`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `xrate`
--
ALTER TABLE `xrate`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cards`
--
ALTER TABLE `cards`
  MODIFY `id` int(1) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `collect`
--
ALTER TABLE `collect`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `exchange`
--
ALTER TABLE `exchange`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `merchant`
--
ALTER TABLE `merchant`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `mgurush`
--
ALTER TABLE `mgurush`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `paylink`
--
ALTER TABLE `paylink`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `payout`
--
ALTER TABLE `payout`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `withdraw`
--
ALTER TABLE `withdraw`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `xrate`
--
ALTER TABLE `xrate`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
