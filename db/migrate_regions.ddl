BEGIN;
-- Country Table
ALTER TABLE `regions_country` DROP INDEX `regions_country_user_id`;

ALTER TABLE `regions_country` CHANGE COLUMN `user_id` `updater_id` integer NOT NULL;
ALTER TABLE `regions_country` CHANGE COLUMN `ctime` `created` datetime NOT NULL;
ALTER TABLE `regions_country` CHANGE COLUMN `mtime` `updated` datetime NOT NULL;
ALTER TABLE `regions_country` ADD COLUMN `creator_id` integer NOT NULL DEFAULT 1;
ALTER TABLE `regions_country` ALTER COLUMN `creator_id` DROP DEFAULT;
ALTER TABLE `regions_country` ADD COLUMN `active` tinyint(1) NOT NULL DEFAULT 1;

ALTER TABLE `regions_country` ADD CONSTRAINT `updater_id_refs_id_country` FOREIGN KEY (`updater_id`) REFERENCES `auth_user` (`id`);
CREATE INDEX `regions_country_updater_id` ON `regions_country` (`updater_id`);

ALTER TABLE `regions_country` ADD CONSTRAINT `creator_id_refs_id_country` FOREIGN KEY (`creator_id`) REFERENCES `auth_user` (`id`);
CREATE INDEX `regions_country_creator_id` ON `regions_country` (`creator_id`);

-- Region Table
ALTER TABLE `regions_region` DROP INDEX `regions_region_user_id`;

ALTER TABLE `regions_region` CHANGE COLUMN `user_id` `updater_id` integer NOT NULL;
ALTER TABLE `regions_region` CHANGE COLUMN `ctime` `created` datetime NOT NULL;
ALTER TABLE `regions_region` CHANGE COLUMN `mtime` `updated` datetime NOT NULL;
ALTER TABLE `regions_region` ADD COLUMN `creator_id` integer NOT NULL DEFAULT 1;
ALTER TABLE `regions_region` ALTER COLUMN `creator_id` DROP DEFAULT;
ALTER TABLE `regions_region` ADD COLUMN `active` tinyint(1) NOT NULL DEFAULT 1;

ALTER TABLE `regions_region` ADD CONSTRAINT `updater_id_refs_id_region` FOREIGN KEY (`updater_id`) REFERENCES `auth_user` (`id`);
CREATE INDEX `regions_region_updater_id` ON `regions_region` (`updater_id`);

ALTER TABLE `regions_region` ADD CONSTRAINT `creator_id_refs_id_region` FOREIGN KEY (`creator_id`) REFERENCES `auth_user` (`id`);
CREATE INDEX `regions_region_creator_id` ON `regions_region` (`creator_id`);

COMMIT;
