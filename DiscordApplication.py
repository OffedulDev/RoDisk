import interactions
import requests
import json
Route = "localhost:8080"

# Client Initialization
token = open("private.env").read()
Bot = interactions.Client(token=token)

# Client Run
def init():
  global Chace
  Bot.start()

# Client Commands
@Bot.command(
    name="check",
    description="Accesses the given key in the database and returns the content. (generates token)",
    options=[
      interactions.Option(
        name="key",
        description="The key to access in the database",
        type=interactions.OptionType.STRING,
        required=True
      )  
    ],
    default_member_permissions = interactions.Permissions.ADMINISTRATOR
)
async def check(ctx, key):
    Token = requests.get("http://" + Route + "/token?passphrase=" + json.loads(open("Data.json", "r+").read())["passphrase"])
    if Token != None:
        Chace = Token.json()["data"]["token"]
        await ctx.send("Token generated: " + Chace, ephemeral=True)
    
    return

if __name__ == "__main__":
  init()
