Assume all parameters in every function is given input.

# For auth_register_v1:
1. Assume the first name and last name can only contain alphanumerical characters, dashes or spaces.
2. Assume the first and last name combined have to have at least 1 alphanumerical character.
(i.e. The handle also has at least 1 alphanumerical character and is not empty)
3. Assume we always return positive integer number for auth_user_id

# For channels_create_v1:
1. Assume the user who created this channel is always the owner of the channels.
2. Assume the name of the channel cannot be blank.
3. Assume the name of the channel has at least 1 alphanumerical character.
4. Assume we always return positive integer number for channel_id.
5. Assume the token is in encrypted form.

# For channel_messages_v1:
1. Assume the start index can never be a negative number.
2. Assume there is currently no function that implements adding messages to a channel.

# For message/send/v1:
1. Assume the function always returns a positive integer number for message_id. 

# For channel_add_owner:
1. Assume that the users must be in the channel before they become the owner

# For dm_create_v1:
1. Assume the dm_id always be positive
2. Assume the u_ids have distinct u_id
3. Assume the creator is a valid user

# For admin_user_remove_v1:
1. Assume everything but first name, last name and u_id are empty keys when we called user/profile

# For admin_userpermission_change_v1:
1. Assume nothing happened (i.e. no error will be raised) when the global owner changes their permission id 
to be 1