-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Mar 15, 2026 at 09:08 AM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hotel_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('0001_initial');

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `id` int NOT NULL,
  `booking_code` varchar(20) NOT NULL,
  `customer_id` int NOT NULL,
  `room_id` int NOT NULL,
  `created_by` int NOT NULL,
  `check_in_date` date NOT NULL,
  `check_out_date` date NOT NULL,
  `actual_check_in` datetime DEFAULT NULL,
  `actual_check_out` datetime DEFAULT NULL,
  `num_adults` int NOT NULL DEFAULT '1',
  `num_children` int NOT NULL DEFAULT '0',
  `status` enum('PENDING','CONFIRMED','CHECKED_IN','CHECKED_OUT','CANCELLED') NOT NULL DEFAULT 'PENDING',
  `deposit_amount` decimal(12,2) NOT NULL DEFAULT '0.00',
  `total_amount` decimal(12,2) DEFAULT NULL,
  `special_requests` text,
  `notes` text,
  `cancelled_at` datetime DEFAULT NULL,
  `cancel_reason` text,
  `is_deleted` smallint NOT NULL DEFAULT '0',
  `deleted_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `bookings`
--

INSERT INTO `bookings` (`id`, `booking_code`, `customer_id`, `room_id`, `created_by`, `check_in_date`, `check_out_date`, `actual_check_in`, `actual_check_out`, `num_adults`, `num_children`, `status`, `deposit_amount`, `total_amount`, `special_requests`, `notes`, `cancelled_at`, `cancel_reason`, `is_deleted`, `deleted_at`, `created_at`, `updated_at`) VALUES
(1, 'HMS-20260308-000001', 1, 1, 2, '2026-03-08', '2026-03-10', '2026-03-08 14:00:00', '2026-03-10 12:00:00', 1, 0, 'CHECKED_OUT', '200000.00', '1320000.00', NULL, NULL, NULL, NULL, 0, NULL, '2026-03-15 04:59:07', '2026-03-15 04:59:07'),
(2, 'HMS-20260315-000002', 2, 4, 1, '2026-03-15', '2026-03-17', NULL, NULL, 2, 0, 'CONFIRMED', '500000.00', NULL, NULL, NULL, NULL, NULL, 0, NULL, '2026-03-15 04:59:07', '2026-03-15 04:59:07');

-- --------------------------------------------------------

--
-- Table structure for table `booking_services`
--

CREATE TABLE `booking_services` (
  `id` int NOT NULL,
  `booking_id` int NOT NULL,
  `service_id` int NOT NULL,
  `quantity` int NOT NULL DEFAULT '1',
  `unit_price` decimal(12,2) NOT NULL,
  `total_price` decimal(12,2) NOT NULL,
  `used_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `notes` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `booking_services`
--

INSERT INTO `booking_services` (`id`, `booking_id`, `service_id`, `quantity`, `unit_price`, `total_price`, `used_at`, `notes`) VALUES
(1, 1, 1, 2, '100000.00', '200000.00', '2026-03-09 08:00:00', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `id` int NOT NULL,
  `full_name` varchar(200) NOT NULL,
  `id_number` varchar(20) NOT NULL,
  `id_type` enum('CCCD','PASSPORT','DRIVER_LICENSE') NOT NULL DEFAULT 'CCCD',
  `gender` enum('MALE','FEMALE','OTHER') DEFAULT 'MALE',
  `date_of_birth` date DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `nationality` varchar(100) DEFAULT 'Việt Nam',
  `address` text,
  `avatar_path` varchar(500) DEFAULT NULL,
  `notes` text,
  `is_deleted` smallint NOT NULL DEFAULT '0',
  `deleted_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`id`, `full_name`, `id_number`, `id_type`, `gender`, `date_of_birth`, `phone`, `email`, `nationality`, `address`, `avatar_path`, `notes`, `is_deleted`, `deleted_at`, `created_at`, `updated_at`) VALUES
(1, 'Nguyễn Văn Anh', '079123456001', 'CCCD', 'MALE', '1990-05-15', '0901111001', 'vananh@email.com', 'Việt Nam', '123 Lê Lợi, Q1, TP.HCM', 'images/avatars/customer_1.jpg', NULL, 0, NULL, '2026-03-15 04:59:07', '2026-03-15 04:59:07'),
(2, 'Trần Thị Bình', '079123456002', 'CCCD', 'FEMALE', '1988-03-22', '0902222002', 'thibinh@email.com', 'Việt Nam', '45 Nguyễn Huệ, Q1, TP.HCM', 'images/avatars/customer_2.jpg', NULL, 0, NULL, '2026-03-15 04:59:07', '2026-03-15 04:59:07'),
(3, 'John Smith', 'US98765432', 'PASSPORT', 'MALE', NULL, '+1-555-0101', 'jsmith@corp.com', 'Mỹ', NULL, 'images/avatars/customer_8.jpg', 'Business traveler', 0, NULL, '2026-03-15 04:59:07', '2026-03-15 04:59:07');

-- --------------------------------------------------------

--
-- Table structure for table `invoices`
--

CREATE TABLE `invoices` (
  `id` int NOT NULL,
  `invoice_code` varchar(20) NOT NULL,
  `booking_id` int NOT NULL,
  `created_by` int NOT NULL,
  `room_charge` decimal(12,2) NOT NULL DEFAULT '0.00',
  `service_charge` decimal(12,2) NOT NULL DEFAULT '0.00',
  `discount_amount` decimal(12,2) NOT NULL DEFAULT '0.00',
  `tax_rate` decimal(5,2) NOT NULL DEFAULT '10.00',
  `tax_amount` decimal(12,2) NOT NULL DEFAULT '0.00',
  `total_amount` decimal(12,2) NOT NULL DEFAULT '0.00',
  `deposit_amount` decimal(12,2) NOT NULL DEFAULT '0.00',
  `amount_due` decimal(12,2) NOT NULL DEFAULT '0.00',
  `payment_method` enum('CASH','CARD','TRANSFER','MIXED') NOT NULL DEFAULT 'CASH',
  `payment_status` enum('UNPAID','PARTIAL','PAID') NOT NULL DEFAULT 'UNPAID',
  `paid_at` datetime DEFAULT NULL,
  `notes` text,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `invoices`
--

INSERT INTO `invoices` (`id`, `invoice_code`, `booking_id`, `created_by`, `room_charge`, `service_charge`, `discount_amount`, `tax_rate`, `tax_amount`, `total_amount`, `deposit_amount`, `amount_due`, `payment_method`, `payment_status`, `paid_at`, `notes`, `created_at`, `updated_at`) VALUES
(1, 'INV-20260310-000001', 1, 2, '1000000.00', '200000.00', '0.00', '10.00', '120000.00', '1320000.00', '200000.00', '1120000.00', 'CASH', 'PAID', '2026-03-10 12:00:00', NULL, '2026-03-15 04:59:07', '2026-03-15 04:59:07');

-- --------------------------------------------------------

--
-- Table structure for table `rooms`
--

CREATE TABLE `rooms` (
  `id` int NOT NULL,
  `room_number` varchar(10) NOT NULL,
  `floor` int NOT NULL DEFAULT '1',
  `room_type_id` int NOT NULL,
  `bed_type` enum('SINGLE','DOUBLE','TWIN','TRIPLE','SUITE','PRESIDENTIAL','FAMILY') NOT NULL DEFAULT 'DOUBLE',
  `status` enum('AVAILABLE','RESERVED','OCCUPIED','CLEANING','MAINTENANCE') NOT NULL DEFAULT 'AVAILABLE',
  `price_override` decimal(12,2) DEFAULT NULL,
  `description` text,
  `image_paths` json DEFAULT NULL,
  `is_deleted` smallint NOT NULL DEFAULT '0',
  `deleted_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `rooms`
--

INSERT INTO `rooms` (`id`, `room_number`, `floor`, `room_type_id`, `bed_type`, `status`, `price_override`, `description`, `image_paths`, `is_deleted`, `deleted_at`, `created_at`, `updated_at`) VALUES
(1, '203', 2, 1, 'SINGLE', 'AVAILABLE', NULL, 'Phòng đơn, view sân vườn', '[\"images/rooms/room_101_1.jpg\"]', 0, NULL, '2026-03-15 04:59:07', '2026-03-15 05:04:56'),
(2, '102', 1, 1, 'DOUBLE', 'OCCUPIED', NULL, NULL, '[\"images/rooms/room_102_1.jpg\"]', 0, NULL, '2026-03-15 04:59:07', '2026-03-15 04:59:07'),
(3, '103', 1, 1, 'TWIN', 'AVAILABLE', NULL, NULL, '[\"images/rooms/room_103_1.jpg\"]', 0, NULL, '2026-03-15 04:59:07', '2026-03-15 04:59:07'),
(4, '201', 2, 2, 'DOUBLE', 'AVAILABLE', NULL, NULL, '[\"images/rooms/room_201_1.jpg\", \"images/rooms/room_201_2.jpg\"]', 0, NULL, '2026-03-15 04:59:07', '2026-03-15 04:59:07'),
(5, '202', 2, 2, 'SUITE', 'RESERVED', NULL, NULL, '[\"images/rooms/room_202_1.jpg\", \"images/rooms/room_202_2.jpg\"]', 0, NULL, '2026-03-15 04:59:07', '2026-03-15 04:59:07'),
(6, '301', 3, 3, 'SUITE', 'AVAILABLE', NULL, NULL, '[\"images/rooms/room_301_1.jpg\", \"images/rooms/room_301_2.jpg\"]', 0, NULL, '2026-03-15 04:59:07', '2026-03-15 04:59:07'),
(7, '401', 4, 4, 'PRESIDENTIAL', 'AVAILABLE', NULL, NULL, '[\"images/rooms/room_401_1.jpg\", \"images/rooms/room_401_2.jpg\", \"images/rooms/room_401_3.jpg\"]', 0, NULL, '2026-03-15 04:59:07', '2026-03-15 04:59:07'),
(8, '204', 2, 5, 'FAMILY', 'AVAILABLE', NULL, NULL, NULL, 0, NULL, '2026-03-15 04:59:07', '2026-03-15 04:59:07');

-- --------------------------------------------------------

--
-- Table structure for table `room_types`
--

CREATE TABLE `room_types` (
  `id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text,
  `base_price` decimal(12,2) NOT NULL DEFAULT '0.00',
  `max_adults` int NOT NULL DEFAULT '2',
  `max_children` int NOT NULL DEFAULT '1',
  `amenities` json DEFAULT NULL,
  `image_path` varchar(500) DEFAULT NULL,
  `is_deleted` smallint NOT NULL DEFAULT '0',
  `deleted_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `room_types`
--

INSERT INTO `room_types` (`id`, `name`, `description`, `base_price`, `max_adults`, `max_children`, `amenities`, `image_path`, `is_deleted`, `deleted_at`, `created_at`, `updated_at`) VALUES
(1, 'Standard', 'Phòng tiêu chuẩn thoải mái, đầy đủ tiện nghi cơ bản.', '500000.00', 2, 1, '[\"WiFi\", \"Điều hoà\", \"TV\", \"Minibar\"]', 'images/room_types/standard.jpg', 0, NULL, '2026-03-15 04:59:07', '2026-03-15 04:59:07'),
(2, 'Deluxe', 'Không gian cao cấp hơn, view đẹp, tiện nghi nâng cấp.', '900000.00', 2, 2, '[\"WiFi\", \"Điều hoà\", \"Smart TV\", \"Minibar\", \"Ban công\"]', 'images/room_types/deluxe.jpg', 0, NULL, '2026-03-15 04:59:07', '2026-03-15 04:59:07'),
(3, 'Suite', 'Phòng Suite sang trọng với phòng khách và phòng ngủ riêng biệt.', '1800000.00', 3, 2, '[\"WiFi\", \"Điều hoà\", \"Smart TV\", \"Jacuzzi\"]', 'images/room_types/suite.jpg', 0, NULL, '2026-03-15 04:59:07', '2026-03-15 04:59:07'),
(4, 'Presidential Suite', 'Hạng cao nhất, dịch vụ cá nhân hoàn hảo.', '5000000.00', 4, 2, '[\"WiFi\", \"Butler\", \"Jacuzzi\", \"Xe đưa đón\"]', 'images/room_types/presidential.jpg', 0, NULL, '2026-03-15 04:59:07', '2026-03-15 04:59:07'),
(5, 'Family', 'Phòng gia đình rộng rãi, phù hợp gia đình.', '1200000.00', 4, 3, '[\"WiFi\", \"Điều hoà\", \"2 phòng ngủ\"]', 'images/room_types/family.jpg', 0, NULL, '2026-03-15 04:59:07', '2026-03-15 04:59:07');

-- --------------------------------------------------------

--
-- Table structure for table `services`
--

CREATE TABLE `services` (
  `id` int NOT NULL,
  `name` varchar(200) NOT NULL,
  `category` enum('FOOD','LAUNDRY','TRANSPORT','SPA','OTHER') NOT NULL DEFAULT 'OTHER',
  `unit_price` decimal(12,2) NOT NULL DEFAULT '0.00',
  `unit` varchar(50) DEFAULT 'lần',
  `description` text,
  `is_deleted` smallint NOT NULL DEFAULT '0',
  `deleted_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `services`
--

INSERT INTO `services` (`id`, `name`, `category`, `unit_price`, `unit`, `description`, `is_deleted`, `deleted_at`, `created_at`, `updated_at`) VALUES
(1, 'Ăn sáng', 'FOOD', '100000.00', 'người', NULL, 0, NULL, '2026-03-15 04:59:07', '2026-03-15 04:59:07'),
(2, 'Giặt ủi', 'LAUNDRY', '80000.00', 'kg', NULL, 0, NULL, '2026-03-15 04:59:07', '2026-03-15 04:59:07'),
(3, 'Đặt xe', 'TRANSPORT', '200000.00', 'chuyến', NULL, 0, NULL, '2026-03-15 04:59:07', '2026-03-15 04:59:07'),
(4, 'Spa', 'SPA', '600000.00', 'lần', NULL, 0, NULL, '2026-03-15 04:59:07', '2026-03-15 04:59:07');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `full_name` varchar(200) NOT NULL,
  `role` enum('ADMIN','RECEPTIONIST') NOT NULL DEFAULT 'RECEPTIONIST',
  `phone` varchar(15) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `avatar_path` varchar(500) DEFAULT NULL,
  `is_active` smallint NOT NULL DEFAULT '1',
  `last_login` datetime DEFAULT NULL,
  `login_attempts` int NOT NULL DEFAULT '0',
  `is_deleted` smallint NOT NULL DEFAULT '0',
  `deleted_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password_hash`, `full_name`, `role`, `phone`, `email`, `avatar_path`, `is_active`, `last_login`, `login_attempts`, `is_deleted`, `deleted_at`, `created_at`, `updated_at`) VALUES
(1, 'admin', '$2b$12$v6IZ0jO4QPC7DMTPVPMMduVavkhmwF4uzxYrxnHE0IDeaoK.Ee8b2', 'Nguyễn Quản Lý', 'ADMIN', '0901234567', 'admin@hotel.com', 'images/avatars/user_admin.jpg', 1, '2026-03-15 08:01:38', 0, 0, NULL, '2026-03-15 04:59:07', '2026-03-15 08:01:38'),
(2, 'letan1', '$2b$12$xgUxC2PCj/XD8hzSQLbBqO/vurkPgvXeJfRpkZMLFMPKcGxZVNjiy', 'Trần Thị Lễ Tân', 'RECEPTIONIST', '0912345678', 'letan1@hotel.com', 'images/avatars/user_recept1.jpg', 1, NULL, 0, 0, NULL, '2026-03-15 04:59:07', '2026-03-15 07:18:49'),
(3, 'letan2', '$2b$12$tS4ZJVTTwui5ygKtGvt4tumU5m0oUjcysmFHxrGmuG3v5X8P3wYSW', 'Phạm Văn Tiếp Đón', 'RECEPTIONIST', '0923456789', NULL, 'images/avatars/user_recept2.jpg', 1, NULL, 0, 0, NULL, '2026-03-15 04:59:07', '2026-03-15 04:59:07');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `booking_code` (`booking_code`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `ix_bookings_is_deleted` (`is_deleted`),
  ADD KEY `idx_bookings_code` (`booking_code`),
  ADD KEY `idx_bookings_status` (`status`),
  ADD KEY `idx_bookings_checkin` (`check_in_date`),
  ADD KEY `idx_bookings_checkout` (`check_out_date`),
  ADD KEY `idx_bookings_customer` (`customer_id`),
  ADD KEY `idx_bookings_room` (`room_id`),
  ADD KEY `idx_bookings_deleted` (`is_deleted`);

--
-- Indexes for table `booking_services`
--
ALTER TABLE `booking_services`
  ADD PRIMARY KEY (`id`),
  ADD KEY `service_id` (`service_id`),
  ADD KEY `idx_booking_services_booking` (`booking_id`);

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id_number` (`id_number`),
  ADD KEY `ix_customers_is_deleted` (`is_deleted`),
  ADD KEY `idx_customers_id_number` (`id_number`),
  ADD KEY `idx_customers_phone` (`phone`),
  ADD KEY `idx_customers_full_name` (`full_name`),
  ADD KEY `idx_customers_deleted` (`is_deleted`);

--
-- Indexes for table `invoices`
--
ALTER TABLE `invoices`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `invoice_code` (`invoice_code`),
  ADD UNIQUE KEY `booking_id` (`booking_id`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `idx_invoices_code` (`invoice_code`),
  ADD KEY `idx_invoices_status` (`payment_status`),
  ADD KEY `idx_invoices_date` (`created_at`);

--
-- Indexes for table `rooms`
--
ALTER TABLE `rooms`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `room_number` (`room_number`),
  ADD KEY `room_type_id` (`room_type_id`),
  ADD KEY `ix_rooms_is_deleted` (`is_deleted`),
  ADD KEY `idx_rooms_status` (`status`),
  ADD KEY `idx_rooms_floor` (`floor`),
  ADD KEY `idx_rooms_deleted` (`is_deleted`);

--
-- Indexes for table `room_types`
--
ALTER TABLE `room_types`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_room_types_is_deleted` (`is_deleted`),
  ADD KEY `idx_room_types_deleted` (`is_deleted`);

--
-- Indexes for table `services`
--
ALTER TABLE `services`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_services_is_deleted` (`is_deleted`),
  ADD KEY `idx_services_category` (`category`),
  ADD KEY `idx_services_deleted` (`is_deleted`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD KEY `ix_users_is_deleted` (`is_deleted`),
  ADD KEY `idx_username` (`username`),
  ADD KEY `idx_role` (`role`),
  ADD KEY `idx_users_deleted` (`is_deleted`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bookings`
--
ALTER TABLE `bookings`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `booking_services`
--
ALTER TABLE `booking_services`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `invoices`
--
ALTER TABLE `invoices`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `rooms`
--
ALTER TABLE `rooms`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `room_types`
--
ALTER TABLE `room_types`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `services`
--
ALTER TABLE `services`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bookings`
--
ALTER TABLE `bookings`
  ADD CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `bookings_ibfk_3` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `booking_services`
--
ALTER TABLE `booking_services`
  ADD CONSTRAINT `booking_services_ibfk_1` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `booking_services_ibfk_2` FOREIGN KEY (`service_id`) REFERENCES `services` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `invoices`
--
ALTER TABLE `invoices`
  ADD CONSTRAINT `invoices_ibfk_1` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `invoices_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `rooms`
--
ALTER TABLE `rooms`
  ADD CONSTRAINT `rooms_ibfk_1` FOREIGN KEY (`room_type_id`) REFERENCES `room_types` (`id`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
