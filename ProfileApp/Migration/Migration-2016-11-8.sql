--Modified image field to store image extension.
ALTER TABLE `employee` ADD `active` BOOLEAN NOT NULL DEFAULT FALSE AFTER `public_profile`;
