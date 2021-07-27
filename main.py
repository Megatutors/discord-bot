import discord
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime

def read_token():
    with open('token.txt', 'r') as f:
        lines = f.readlines()
        return lines[0].strip()

# Setup 
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
intents = discord.Intents().default()
intents.members = True
client = discord.Client(intents=intents)

# When member joins # change channel id
@client.event
async def on_member_join(member):
    channel = client.get_channel(836802783071174669)
    db.collection('users').document(str(member.id)).set({"modlog":[],"SwearCount":0})
    await channel.purge(limit=1)   # NOT SURE IF THERE IS A FUNCTION TO REMOVE DEFAULT WELCOME
    await channel.send(f"""Welcome to the server {member.mention}""")   # CHANGE WELCOME MESSAGE


@client.event
async def on_message(message):

    # Bad Words FILL IN LIST BELOW
    bad_words = []
    for word in bad_words:
        if message.content.count(word) > 0:
            print("A bad word was said")
            db.collection('users').document(str(message.author.id)).update({"SwearCount":firestore.Increment(1)})
            await message.channel.purge(limit=1)
            break

    # Kicking / Banning
    for role in message.author.roles:
        if role.name=="Admin":
            if message.content.startswith('>'):
                moderate = message.content.split(" ")
                db.collection('users').document(str(message.mentions[0].id)).update({"modlog":firestore.ArrayUnion([{"action":moderate[0][1:], "reason":' '.join(moderate[2:]), "date":datetime.now()}])})
            if message.content.startswith('>kick'):
                await message.mentions[0].kick()

client.run(read_token())