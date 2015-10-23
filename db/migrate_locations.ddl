BEGIN;
-- LocationCodeDefault Table
ALTER TABLE `maintenance_locationcodedefault` DROP INDEX `maintenance_locationcodedefault_403f60f`;

ALTER TABLE `maintenance_locationcodedefault` CHANGE COLUMN `user_id` `updater_id` integer NOT NULL;
ALTER TABLE `maintenance_locationcodedefault` CHANGE COLUMN `ctime` `created` datetime NOT NULL;
ALTER TABLE `maintenance_locationcodedefault` CHANGE COLUMN `mtime` `updated` datetime NOT NULL;
ALTER TABLE `maintenance_locationcodedefault` ADD COLUMN `creator_id` integer NOT NULL DEFAULT 1;
ALTER TABLE `maintenance_locationcodedefault` ALTER COLUMN `creator_id` DROP DEFAULT;

ALTER TABLE `maintenance_locationcodedefault` ADD CONSTRAINT `updater_id_refs_id_2ca60cd7` FOREIGN KEY (`updater_id`) REFERENCES `accounts_user` (`id`);
CREATE INDEX `maintenance_locationcodedefault_af4ed6b3` ON `maintenance_locationcodedefault` (`updater_id`);

ALTER TABLE `maintenance_locationcodedefault` ADD CONSTRAINT `creator_id_refs_id_2ca60cd7` FOREIGN KEY (`creator_id`) REFERENCES `accounts_user` (`id`);
CREATE INDEX `maintenance_locationcodedefault_ad376f8d` ON `maintenance_locationcodedefault` (`creator_id`);

-- LocationCodeCategory Table
ALTER TABLE `maintenance_locationcodecategory` DROP INDEX `maintenance_locationcodecategory_403f60f`;

ALTER TABLE `maintenance_locationcodecategory` CHANGE COLUMN `user_id` `updater_id` integer NOT NULL;
ALTER TABLE `maintenance_locationcodecategory` CHANGE COLUMN `ctime` `created` datetime NOT NULL;
ALTER TABLE `maintenance_locationcodecategory` CHANGE COLUMN `mtime` `updated` datetime NOT NULL;
ALTER TABLE `maintenance_locationcodecategory` ADD COLUMN `creator_id` integer NOT NULL DEFAULT 1;
ALTER TABLE `maintenance_locationcodecategory` ALTER COLUMN `creator_id` DROP DEFAULT;

ALTER TABLE `maintenance_locationcodecategory` ADD CONSTRAINT `updater_id_refs_id_0863530f` FOREIGN KEY (`updater_id`) REFERENCES `accounts_user` (`id`);
CREATE INDEX `maintenance_locationcodecategory_af4ed6b3` ON `maintenance_locationcodecategory` (`updater_id`);

ALTER TABLE `maintenance_locationcodecategory` ADD CONSTRAINT `creator_id_refs_id_0863530f` FOREIGN KEY (`creator_id`) REFERENCES `accounts_user` (`id`);
CREATE INDEX `maintenance_locationcodecategory_ad376f8d` ON `maintenance_locationcodecategory` (`creator_id`);
COMMIT;
