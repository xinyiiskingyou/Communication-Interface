Assume all parameters in every function is given input. 


For auth_register_v1:
Assume the first name and last name can only contain alphanumerical characters, dashes or spaces.
Assume the first and last name combined have to have at least 1 alphanumerical character.
(i.e. The handle also has at least 1 alphanumerical handle)


For channels_create_v1:
Assume the user who created this channel is always the owner of the channels.
Assume the name of the channel cannot be blank. 
Assume the name of the channel has at least 1 alphanumerical character.


For channel_messages_v1:
Assume the start index can never be a negative number. 
Assume there is currently no function that implements adding messages to a channel. 


    
 


