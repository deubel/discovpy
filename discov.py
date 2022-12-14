import disnake
import json
import sys
import random
import time
import os

args = sys.argv[1:]
token = args[0]
file = args[1]

with open(file, encoding='utf-8') as input_file:
    markovs = json.load(input_file)
    print(f"Discov is keeping track of {len(markovs)} users")
    input_file.close()


def add_phrase(markov, text: str, min_words: int = 4):
    words = text.split(' ')
    if len(words) < min_words:
        print(f"Phrase has less words than the minimum of {min_words}")
        return

    for index, word in enumerate(words):
        if index == 0:
            if "_start" not in markov:
                markov["_start"] = []
            markov["_start"].append(word)

            if index != len(words) - 1:
                if word not in markov:
                    markov[word] = []
                markov[word].append(words[index + 1])

        elif index == len(words) - 1:
            if "_end" not in markov:
                markov["_end"] = []
            markov["_end"].append(word)

        else:
            if word not in markov:
                markov[word] = []
            markov[word].append(words[index + 1])


def generate(markov):
    phrase = []
    starts = markov["_start"]
    if not starts:
        return None
    word = random.choice(starts)
    phrase.append(word)

    while word and not word.endswith(('.', '?', '!')):
        if word not in markov:
            return None
        word = random.choice(markov[word])
        phrase.append(word)

    result = ' '.join(phrase)
    print(f"Generated Markov chain: {result}")
    return result


def write_data_file(user_id):
    if not os.path.exists("tmp"):
        os.mkdir("tmp")
    write_path = f"tmp/markovs_{user_id}.json"
    with open(write_path, "w", encoding='utf-8') as write_file:
        json.dump(markovs[user_id], write_file, indent=3)
    return write_path


class DiscovClient(disnake.Client):
    def __init__(self, **options):
        super().__init__(**options)
        self.last_save = 0

    async def on_ready(self):
        print(f"Logged in as {self.user} ({self.user.id})")

    async def on_message(self, message):
        author_id = str(message.author.id)
        self_id = str(self.user.id)
        content = message.content
        if not content.startswith("!markov"):
            if author_id != self_id:
                if author_id not in markovs:
                    markovs[author_id] = dict()
                if self_id not in markovs:
                    markovs[self_id] = dict()
                formatted = content.capitalize() if content.endswith(('.', '?', '!')) else f"{content.capitalize()}."
                print(f"Adding phrase \"{formatted}\" to user {author_id}")
                add_phrase(markovs[author_id], formatted)
                print(f"Adding phrase \"{formatted}\" to user {self_id}")
                add_phrase(markovs[self_id], formatted)

                if time.time() - self.last_save > 900:
                    with open(file, 'w', encoding='utf-8') as output_file:
                        json.dump(markovs, output_file)
                        self.last_save = time.time()
                        output_file.close()
        elif author_id != self_id:
            if content.startswith("!markov purge"):
                del markovs[author_id]
                await message.add_reaction('👍')
            elif content.startswith("!markov data"):
                author = message.author
                read_path = write_data_file(author_id)
                with open(read_path, "r", encoding='utf-8') as read_file:
                    await author.create_dm()
                    await author.dm_channel.send(
                        f'Hi {author.name}, here is everything I know about you. If you\'d like me to forget, '
                        f'just use the `!markov purge` command here or in a server I\'m in.',
                        file=disnake.File(read_file))
                    await message.add_reaction('👍')
            else:
                user_id = str(message.mentions[0].id) if message.mentions else self_id
                if user_id in markovs:
                    markov = markovs[user_id]
                    if markov:
                        generated = generate(markov)
                        if generated:
                            await message.channel.send(generated)


client = DiscovClient(intents=disnake.Intents.all(),
                      activity=disnake.Activity(name='you', type=disnake.ActivityType.watching))
client.run(token)
