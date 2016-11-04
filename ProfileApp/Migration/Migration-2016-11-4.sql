-- Added public_profile field to store type of profile.
ALTER TABLE `employee` ADD `public_profile` BOOLEAN NOT NULL DEFAULT FALSE AFTER `preferCommun`;
