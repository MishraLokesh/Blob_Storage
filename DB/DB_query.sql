# Inserting a new user with a new file
INSERT INTO `blob`.`user` (`user_id`, `email`, `password`) VALUES ('4', 'U4', 'user4');
INSERT INTO `blob`.`files` (`file_id`, `file_name`, `file_path`) VALUES ('4', 'F4', '/Pictures');
INSERT INTO `blob`.`relation` (`user_id`, `file_id`, `is_owner`) VALUES ('4', '4', '1');

# Giving file access to another user
# first check if the person giving access is the owner by validating is_owner in relation table is set to 1 for that person. If so then
INSERT INTO `blob`.`relation` (`user_id`, `file_id`, `is_owner`) VALUES ('1', '4', '0');

# Querying all files that any particular user has access to
SELECT * FROM blob.files where file_id in (SELECT file_id FROM blob.relation where user_id=1);

# EASY PEASY :)
