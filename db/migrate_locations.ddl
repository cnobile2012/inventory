BEGIN;
-- LocationCodeDefault Table
RENAME TABLE `maintenance_locationcodedefault` TO `maintenance_locationformat`;
ALTER TABLE `maintenance_locationformat` DROP INDEX `maintenance_locationformat_403f60f`;

ALTER TABLE `maintenance_locationformat` CHANGE COLUMN `user_id` `updater_id` integer NOT NULL;
ALTER TABLE `maintenance_locationformat` CHANGE COLUMN `ctime` `created` datetime NOT NULL;
ALTER TABLE `maintenance_locationformat` CHANGE COLUMN `mtime` `updated` datetime NOT NULL;
ALTER TABLE `maintenance_locationformat` ADD COLUMN `creator_id` integer NOT NULL DEFAULT 1;
ALTER TABLE `maintenance_locationformat` ALTER COLUMN `creator_id` DROP DEFAULT;

ALTER TABLE `maintenance_locationformat` DROP INDEX `maintenance_locationcodedefault_45182cf4`;
CREATE INDEX `maintenance_locationformat_45182cf4` ON `maintenance_locationformat` (`char_definition`);
ALTER TABLE `maintenance_locationformat` ADD CONSTRAINT `updater_id_refs_id_2ca60cd7` FOREIGN KEY (`updater_id`) REFERENCES `accounts_user` (`id`);
CREATE INDEX `maintenance_locationformat_af4ed6b3` ON `maintenance_locationformat` (`updater_id`);

ALTER TABLE `maintenance_locationformat` ADD CONSTRAINT `creator_id_refs_id_2ca60cd7` FOREIGN KEY (`creator_id`) REFERENCES `accounts_user` (`id`);
CREATE INDEX `maintenance_locationformat_ad376f8d` ON `maintenance_locationformat` (`creator_id`);

-- LocationCodeCategory Table
RENAME TABLE `maintenance_locationcodecategory` TO `maintenance_locationcode`;
ALTER TABLE `maintenance_locationcode` DROP INDEX `maintenance_locationcode_403f60f`;

ALTER TABLE `maintenance_locationcode` ADD COLUMN `level` smallint NOT NULL DEFAULT 1;
ALTER TABLE `maintenance_locationcode` ALTER COLUMN `level` DROP DEFAULT;

ALTER TABLE `maintenance_locationcode` CHANGE COLUMN `user_id` `updater_id` integer NOT NULL;
ALTER TABLE `maintenance_locationcode` CHANGE COLUMN `ctime` `created` datetime NOT NULL;
ALTER TABLE `maintenance_locationcode` CHANGE COLUMN `mtime` `updated` datetime NOT NULL;
ALTER TABLE `maintenance_locationcode` ADD COLUMN `creator_id` integer NOT NULL DEFAULT 1;
ALTER TABLE `maintenance_locationcode` ALTER COLUMN `creator_id` DROP DEFAULT;

ALTER TABLE `maintenance_locationcode` ADD CONSTRAINT `updater_id_refs_id_0863530f` FOREIGN KEY (`updater_id`) REFERENCES `accounts_user` (`id`);
CREATE INDEX `maintenance_locationcode_af4ed6b3` ON `maintenance_locationcode` (`updater_id`);

ALTER TABLE `maintenance_locationcode` ADD CONSTRAINT `creator_id_refs_id_0863530f` FOREIGN KEY (`creator_id`) REFERENCES `accounts_user` (`id`);
CREATE INDEX `maintenance_locationcode_ad376f8d` ON `maintenance_locationcode` (`creator_id`);

-- items_item_location_code
ALTER TABLE `items_item_location_code` CHANGE COLUMN `locationcodecategory_id` `locationcode_id` integer NOT NULL;

COMMIT;
