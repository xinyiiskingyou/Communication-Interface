For auth_register_v1 & auth_login_v1:
First and last names can consist of all characters such as, 
numbers, symbols (!,-,) or spaces.
Assume user always enters input for email and password

For auth_register_v1:
That handle duplications don't go over 99. ie a handle of
'abcdefghijklmnopqrst100' is not possible

For channels_create_v1:
Assume the user alawys inputs auth_user_id that exist
Assume the user always inputs valid is_public either 0 or 1
Assume the user who created this channel is always the owner of the channels
Assume the name cannot be blank
