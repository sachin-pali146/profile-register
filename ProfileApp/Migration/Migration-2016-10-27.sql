-- Added Email field in employee table
ALTER TABLE `employee` ADD `email` VARCHAR(50) NOT NULL AFTER `lastName`;
