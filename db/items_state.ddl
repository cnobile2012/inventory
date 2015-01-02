alter table items_manufacturer drop state;
alter table items_distributor drop state;
alter table items_manufacturer add state_id integer;
alter table items_distributor add state_id integer;
ALTER TABLE `items_distributor` ADD CONSTRAINT `state_id_refs_id_671dcd5c` FOREIGN KEY (`state_id`) REFERENCES `regions_region` (`id`);
ALTER TABLE `items_manufacturer` ADD CONSTRAINT `state_id_refs_id_3a88ca45` FOREIGN KEY (`state_id`) REFERENCES `regions_region` (`id`);
CREATE INDEX `items_distributor_state_id` ON `items_distributor` (`state_id`);
CREATE INDEX `items_manufacturer_state_id` ON `items_manufacturer` (`state_id`);
