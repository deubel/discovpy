# discovpy
Discov is a Discord bot that tracks messages of server members and can generate messages based on a users data through a Markov chain. You can also request and/or delete your data stored by the bot.  
Discov keeps it's data in memory and persists it in a json file and does therefore not scale very well, so it's best suited for private use.

# usage
**mention the bot and another user anywhere in your message** to generate a message based on the mentioned user's data  
**mention only the bot anywhere in your message** to generate a message based on everyone's data  
**!discov data** - sends you your collected data in private  
**!discov purge** - deletes your collected data
