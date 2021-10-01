## For auth_register_v1 & auth_login_v1:
1. First and last names can consist of all characters such as,
numbers, symbols (!,-,) or spaces.
2. Assume user always enters input for email and password

## For auth_register_v1:
1. That handle duplications don't go over 99. ie a handle of
'abcdefghijklmnopqrst100' is not possible
2. The combination of name_first and name_last to produce a handle
has at least 1 alphabetical or numerical character so that the 
handle produced in not empty.

## For channels_create_v1:
1. Assume the user alawys inputs auth_user_id that exist
2. Assume the user always inputs valid is_public either 0 or 1
3. Assume the user who created this channel is always the owner of the channels
4. Assume the name cannot be blank
5. Assume the channel name cannot be duplicate (?)
6. Assume one can only create one channel(?)


    
 


