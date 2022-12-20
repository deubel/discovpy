# discovpy
Discov is a Discord bot that tracks messages of server members and can generate messages based on a users data through a Markov chain. You can also request and/or delete your data stored by the bot.  
Discov keeps it's data in memory and persists it in a json file and does therefore not scale very well, so it's best suited for private use.

# commands
!markov @usermention - generates a message based on the mentioned user's data  
!markov - generates a message based on everyone's data  
!markov data - sends you your collected data in private  
!markov purge - deletes your collected data
