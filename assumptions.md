Assume all parameters in every function is given input.

# For auth/register/v2:
1. Assume the first name and last name can only contain alphanumerical characters, dashes or spaces.
2. Assume the first and last name combined have to have at least 1 alphanumerical character.
(i.e. The handle also has at least 1 alphanumerical character and is not empty)
3. Assume we always return positive integer number for auth_user_id

# For channels/create/v2:
1. Assume the user who created this channel is always the owner of the channels.
2. Assume the name of the channel cannot be blank.
3. Assume the name of the channel has at least 1 alphanumerical character.
4. Assume we always return positive integer number for channel_id.
5. Assume the token is in encrypted form.

# For channel/messages/v2:
1. Assume the start index can never be a negative number.
2. Assume there is currently no function that implements adding messages to a channel.

# For message/send/v1:
1. Assume the function always returns a positive integer number for message_id. 

# For dm/create/v1:
1. Assume the dm_id always be positive
2. Assume the u_ids are distinct u_ids
3. Assume the creator is a valid user

# For admin/user/remove/v1:
1. Assume other keys except for first name, last name and u_id of the removed users are empty.
2. Assume the token will be invalidated after the user is removed.

# For admin/userpermission/change/v1:
1. Assume no error will be raised when the global owner changes their permission id to be 1.

# For notifications/get/v1:
1. Assume when a user is tagged multiple times in one message, they only get one notification. 
2. Assume that users get a notification when they tag themselves

# For search/v1:
1. Assume that the search is not case-sensitive. 
2. Assume that message must contain the exact query string (i.e. ' ' or spaces affect the search)

# For user/profile/uploadphoto/v1:
1. Assume that user always inputs x_start, y_start, x_end, y_end when uploading new photo. 
