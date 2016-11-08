--Modified image field to store image extension.
ALTER TABLE `employee` CHANGE `image` `image_extension` VARCHAR(6) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL;
