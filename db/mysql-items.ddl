BEGIN;
CREATE TABLE `items_distributor` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `ctime` datetime NOT NULL,
    `mtime` datetime NOT NULL,
    `name` varchar(248) NOT NULL,
    `address_01` varchar(50),
    `address_02` varchar(50),
    `city` varchar(30),
    `state_id` integer,
    `postal_code` varchar(15),
    `country_id` integer,
    `phone` varchar(20),
    `fax` varchar(20),
    `email` varchar(75),
    `url` varchar(248)
)
;
ALTER TABLE `items_distributor` ADD CONSTRAINT `country_id_refs_id_1a60f3b7` FOREIGN KEY (`country_id`) REFERENCES `regions_country` (`id`);
ALTER TABLE `items_distributor` ADD CONSTRAINT `state_id_refs_id_671dcd5c` FOREIGN KEY (`state_id`) REFERENCES `regions_region` (`id`);
ALTER TABLE `items_distributor` ADD CONSTRAINT `user_id_refs_id_290a8161` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `items_manufacturer` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `ctime` datetime NOT NULL,
    `mtime` datetime NOT NULL,
    `name` varchar(248) NOT NULL,
    `address_01` varchar(50),
    `address_02` varchar(50),
    `city` varchar(30),
    `state_id` integer,
    `postal_code` varchar(15),
    `country_id` integer,
    `phone` varchar(20),
    `fax` varchar(20),
    `email` varchar(75),
    `url` varchar(248)
)
;
ALTER TABLE `items_manufacturer` ADD CONSTRAINT `country_id_refs_id_7e808480` FOREIGN KEY (`country_id`) REFERENCES `regions_country` (`id`);
ALTER TABLE `items_manufacturer` ADD CONSTRAINT `state_id_refs_id_3a88ca45` FOREIGN KEY (`state_id`) REFERENCES `regions_region` (`id`);
ALTER TABLE `items_manufacturer` ADD CONSTRAINT `user_id_refs_id_52fbdeb6` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `items_category` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `ctime` datetime NOT NULL,
    `mtime` datetime NOT NULL,
    `parent_id` integer,
    `name` varchar(248) NOT NULL,
    `path` varchar(1016) NOT NULL
)
;
ALTER TABLE `items_category` ADD CONSTRAINT `user_id_refs_id_1e44f65` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `items_category` ADD CONSTRAINT `parent_id_refs_id_5736307d` FOREIGN KEY (`parent_id`) REFERENCES `items_category` (`id`);
CREATE TABLE `items_currency` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `ctime` datetime NOT NULL,
    `mtime` datetime NOT NULL,
    `symbol` varchar(1) NOT NULL,
    `currency` varchar(20) NOT NULL
)
;
ALTER TABLE `items_currency` ADD CONSTRAINT `user_id_refs_id_162e4458` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `items_cost` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `ctime` datetime NOT NULL,
    `mtime` datetime NOT NULL,
    `value` numeric(10, 4) NOT NULL,
    `currency_id` integer NOT NULL,
    `date_acquired` date,
    `invoice_number` varchar(20),
    `item_id` integer NOT NULL,
    `distributor_id` integer,
    `manufacturer_id` integer
)
;
ALTER TABLE `items_cost` ADD CONSTRAINT `currency_id_refs_id_2c531a3d` FOREIGN KEY (`currency_id`) REFERENCES `items_currency` (`id`);
ALTER TABLE `items_cost` ADD CONSTRAINT `user_id_refs_id_760a46a2` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `items_cost` ADD CONSTRAINT `manufacturer_id_refs_id_79a7aa71` FOREIGN KEY (`manufacturer_id`) REFERENCES `items_manufacturer` (`id`);
ALTER TABLE `items_cost` ADD CONSTRAINT `distributor_id_refs_id_6b9e98dc` FOREIGN KEY (`distributor_id`) REFERENCES `items_distributor` (`id`);
CREATE TABLE `items_specification` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `ctime` datetime NOT NULL,
    `mtime` datetime NOT NULL,
    `name` varchar(248),
    `value` varchar(248),
    `item_id` integer NOT NULL
)
;
ALTER TABLE `items_specification` ADD CONSTRAINT `user_id_refs_id_4c29d2cd` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `items_item_location_code` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `item_id` integer NOT NULL,
    `locationcodecategory_id` integer NOT NULL,
    UNIQUE (`item_id`, `locationcodecategory_id`)
)
;
ALTER TABLE `items_item_location_code` ADD CONSTRAINT `locationcodecategory_id_refs_id_1656b609` FOREIGN KEY (`locationcodecategory_id`) REFERENCES `maintenance_locationcodecategory` (`id`);
CREATE TABLE `items_item_categories` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `item_id` integer NOT NULL,
    `category_id` integer NOT NULL,
    UNIQUE (`item_id`, `category_id`)
)
;
ALTER TABLE `items_item_categories` ADD CONSTRAINT `category_id_refs_id_3ed4445c` FOREIGN KEY (`category_id`) REFERENCES `items_category` (`id`);
CREATE TABLE `items_item` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `ctime` datetime NOT NULL,
    `mtime` datetime NOT NULL,
    `title` varchar(248) NOT NULL,
    `item_number` varchar(50) NOT NULL,
    `item_number_mfg` varchar(50),
    `item_number_dst` varchar(50),
    `package` varchar(30),
    `condition` smallint NOT NULL,
    `quantity` integer UNSIGNED NOT NULL,
    `distributor_id` integer,
    `manufacturer_id` integer,
    `active` bool NOT NULL,
    `obsolete` bool NOT NULL,
    `purge` bool NOT NULL,
    `notes` longtext
)
;
ALTER TABLE `items_item` ADD CONSTRAINT `distributor_id_refs_id_1aa75902` FOREIGN KEY (`distributor_id`) REFERENCES `items_distributor` (`id`);
ALTER TABLE `items_item` ADD CONSTRAINT `user_id_refs_id_6ce394c4` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `items_item` ADD CONSTRAINT `manufacturer_id_refs_id_2067aec3` FOREIGN KEY (`manufacturer_id`) REFERENCES `items_manufacturer` (`id`);
ALTER TABLE `items_cost` ADD CONSTRAINT `item_id_refs_id_2e1c6ddf` FOREIGN KEY (`item_id`) REFERENCES `items_item` (`id`);
ALTER TABLE `items_specification` ADD CONSTRAINT `item_id_refs_id_34fd5536` FOREIGN KEY (`item_id`) REFERENCES `items_item` (`id`);
ALTER TABLE `items_item_location_code` ADD CONSTRAINT `item_id_refs_id_74153a0b` FOREIGN KEY (`item_id`) REFERENCES `items_item` (`id`);
ALTER TABLE `items_item_categories` ADD CONSTRAINT `item_id_refs_id_47da26c5` FOREIGN KEY (`item_id`) REFERENCES `items_item` (`id`);
CREATE INDEX `items_distributor_403f60f` ON `items_distributor` (`user_id`);
CREATE INDEX `items_distributor_52094d6e` ON `items_distributor` (`name`);
CREATE INDEX `items_distributor_469f723e` ON `items_distributor` (`state_id`);
CREATE INDEX `items_distributor_534dd89` ON `items_distributor` (`country_id`);
CREATE INDEX `items_manufacturer_403f60f` ON `items_manufacturer` (`user_id`);
CREATE INDEX `items_manufacturer_52094d6e` ON `items_manufacturer` (`name`);
CREATE INDEX `items_manufacturer_469f723e` ON `items_manufacturer` (`state_id`);
CREATE INDEX `items_manufacturer_534dd89` ON `items_manufacturer` (`country_id`);
CREATE INDEX `items_category_403f60f` ON `items_category` (`user_id`);
CREATE INDEX `items_category_63f17a16` ON `items_category` (`parent_id`);
CREATE INDEX `items_currency_403f60f` ON `items_currency` (`user_id`);
CREATE INDEX `items_cost_403f60f` ON `items_cost` (`user_id`);
CREATE INDEX `items_cost_41f657b3` ON `items_cost` (`currency_id`);
CREATE INDEX `items_cost_67b70d25` ON `items_cost` (`item_id`);
CREATE INDEX `items_cost_3bf6f7bc` ON `items_cost` (`distributor_id`);
CREATE INDEX `items_cost_4ac7f441` ON `items_cost` (`manufacturer_id`);
CREATE INDEX `items_specification_403f60f` ON `items_specification` (`user_id`);
CREATE INDEX `items_specification_67b70d25` ON `items_specification` (`item_id`);
CREATE INDEX `items_item_403f60f` ON `items_item` (`user_id`);
CREATE INDEX `items_item_7d2df0dd` ON `items_item` (`item_number`);
CREATE INDEX `items_item_45efa85a` ON `items_item` (`item_number_mfg`);
CREATE INDEX `items_item_726e3f23` ON `items_item` (`item_number_dst`);
CREATE INDEX `items_item_3bf6f7bc` ON `items_item` (`distributor_id`);
CREATE INDEX `items_item_4ac7f441` ON `items_item` (`manufacturer_id`);
COMMIT;
