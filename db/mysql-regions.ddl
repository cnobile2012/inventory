BEGIN;
CREATE TABLE `regions_country` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `ctime` datetime NOT NULL,
    `mtime` datetime NOT NULL,
    `country` varchar(100) NOT NULL,
    `country_code_2` varchar(2) NOT NULL UNIQUE,
    `country_code_3` varchar(3) UNIQUE,
    `country_number_code` integer UNSIGNED
)
;
ALTER TABLE `regions_country` ADD CONSTRAINT `user_id_refs_id_3edfaec5` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `regions_region` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `ctime` datetime NOT NULL,
    `mtime` datetime NOT NULL,
    `country_id` integer NOT NULL,
    `region_code` varchar(10) NOT NULL,
    `region` varchar(100) NOT NULL,
    `primary_level` varchar(50),
    UNIQUE (`country_id`, `region`)
)
;
ALTER TABLE `regions_region` ADD CONSTRAINT `country_id_refs_id_55334be` FOREIGN KEY (`country_id`) REFERENCES `regions_country` (`id`);
ALTER TABLE `regions_region` ADD CONSTRAINT `user_id_refs_id_5233f1f8` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE INDEX `regions_country_user_id` ON `regions_country` (`user_id`);
CREATE INDEX `regions_region_user_id` ON `regions_region` (`user_id`);
CREATE INDEX `regions_region_country_id` ON `regions_region` (`country_id`);
CREATE INDEX `regions_region_region_code` ON `regions_region` (`region_code`);
COMMIT;
