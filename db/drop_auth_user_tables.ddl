BEGIN;
-- drop table authtoken_token;

drop table auth_user_user_permissions;
drop table auth_user_groups;

SET FOREIGN_KEY_CHECKS=0;
drop table auth_user;
SET FOREIGN_KEY_CHECKS=1;
COMMIT;
