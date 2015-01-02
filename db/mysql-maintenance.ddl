BEGIN;
CREATE TABLE `maintenance_locationcodedefault` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `ctime` datetime NOT NULL,
    `mtime` datetime NOT NULL,
    `segment_length` integer UNSIGNED NOT NULL,
    `segment_separator` varchar(3) NOT NULL,
    `char_definition` varchar(248) NOT NULL,
    `segment_order` integer UNSIGNED NOT NULL,
    `description` varchar(1024) NOT NULL
)
;
ALTER TABLE `maintenance_locationcodedefault` ADD CONSTRAINT `user_id_refs_id_8389b9a` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `maintenance_locationcodecategory` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `ctime` datetime NOT NULL,
    `mtime` datetime NOT NULL,
    `parent_id` integer,
    `segment` varchar(248) NOT NULL,
    `path` varchar(248) NOT NULL,
    `char_definition_id` integer NOT NULL
)
;
ALTER TABLE `maintenance_locationcodecategory` ADD CONSTRAINT `char_definition_id_refs_id_119ac735` FOREIGN KEY (`char_definition_id`) REFERENCES `maintenance_locationcodedefault` (`id`);
ALTER TABLE `maintenance_locationcodecategory` ADD CONSTRAINT `user_id_refs_id_1c74a66a` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `maintenance_locationcodecategory` ADD CONSTRAINT `parent_id_refs_id_6cb4ef49` FOREIGN KEY (`parent_id`) REFERENCES `maintenance_locationcodecategory` (`id`);
CREATE INDEX `maintenance_locationcodedefault_403f60f` ON `maintenance_locationcodedefault` (`user_id`);
CREATE INDEX `maintenance_locationcodedefault_45182cf4` ON `maintenance_locationcodedefault` (`char_definition`);
CREATE INDEX `maintenance_locationcodecategory_403f60f` ON `maintenance_locationcodecategory` (`user_id`);
CREATE INDEX `maintenance_locationcodecategory_63f17a16` ON `maintenance_locationcodecategory` (`parent_id`);
CREATE INDEX `maintenance_locationcodecategory_15a4e919` ON `maintenance_locationcodecategory` (`segment`);
CREATE INDEX `maintenance_locationcodecategory_33f26e6b` ON `maintenance_locationcodecategory` (`char_definition_id`);
COMMIT;
