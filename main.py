import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='$', intents=intents)

global context

game = False

# Set all possible winning combinations
winning_combs = [
    [0,1,2],
    [3,4,5],
    [6,7,8],
    [0,3,6],
    [1,4,7],
    [2,5,8],
    [0,4,8],
    [2,4,6]
]

# Set board to check for wins
visual_board = [
    "e","e","e",
    "e","e","e",
    "e","e","e"
]

async def end_game():
    """
    ends a tic-tac-toe game
    """
    global visual_board
    global game
    global tiles
    visual_board = [
        "e","e","e",
        "e","e","e",
        "e","e","e"
    ]
    await context.send("Game timed out")
    await board_message.delete()
    game = False
    tiles = 0

# Change button according to symbol
async def handle_click(view, button, interaction):
    """
    Handles a click from a sender
    """
    
    global current_turn
    global game
    global visual_board
    global tiles

    button.disabled = True
    button.label = current_turn['symbol']

    visual_board[int(button.custom_id)] = current_turn['visual_symbol']

    win = False
    for i in winning_combs:
        if visual_board[i[0]] == current_turn['visual_symbol'] and visual_board[i[1]] == current_turn['visual_symbol'] and visual_board[i[2]] == current_turn['visual_symbol']:
            win = True
            break
    
    if win:
        await context.send("<@{player}> Won!".format(player=current_turn['id']))
        await end_game()
    elif tiles == 8:
        await context.send("Its a draw!")
        await end_game()
    else:
        # Switch players
        if current_turn['user'] == player['user']:
            current_turn = friend
        else:
            current_turn = player

        tiles += 1
        await context.send("Its your turn <@{player}>".format(player=current_turn['id']))
        await interaction.response.edit_message(view=view)

async def incorrect_player(interaction):
        """
        Handles click in the event that it is not the senders' turn
        """
        
        sender = interaction.user.id
        message = "Not your turn <@{sender}>".format(sender=sender)
        await interaction.response.send_message(message)

# Check if sender is the correct player
async def check_player(interaction):
    """
    Ensures sender is in the current game and it is the senders turn

    Returns:
    Boolean: It is the senders turn
    """
    
    sender = interaction.user.name + "#" + interaction.user.discriminator

    if sender != current_turn['user']:
        await incorrect_player(interaction)
        return False
    
    return True

class Board(discord.ui.View):
    # ROW 0
    @discord.ui.button(custom_id="0", label="⬜", row=0, style=discord.ButtonStyle.primary)
    async def zero_callback(self, interaction, button):
        correct_player = await check_player(interaction)

        if correct_player:
            await handle_click(self, button, interaction)

    @discord.ui.button(custom_id="1", label="⬜", row=0, style=discord.ButtonStyle.primary)
    async def one_callback(self, interaction, button):
        correct_player = await check_player(interaction)

        if correct_player:
            await handle_click(self, button, interaction)
    
    @discord.ui.button(custom_id="2", label="⬜", row=0, style=discord.ButtonStyle.primary)
    async def two_callback(self, interaction, button):
        correct_player = await check_player(interaction)

        if correct_player:
            await handle_click(self, button, interaction)

    # ROW 1
    @discord.ui.button(custom_id="3", label="⬜", row=1, style=discord.ButtonStyle.primary)
    async def three_callback(self, interaction, button):
        correct_player = await check_player(interaction)

        if correct_player:
            await handle_click(self, button, interaction)

    @discord.ui.button(custom_id="4", label="⬜", row=1, style=discord.ButtonStyle.primary)
    async def four_callback(self, interaction, button):
        correct_player = await check_player(interaction)

        if correct_player:
            await handle_click(self, button, interaction)

    @discord.ui.button(custom_id="5", label="⬜", row=1, style=discord.ButtonStyle.primary)
    async def five_callback(self, interaction, button):
        correct_player = await check_player(interaction)

        if correct_player:
            await handle_click(self, button, interaction)

    # ROW 2
    @discord.ui.button(custom_id="6", label="⬜", row=2, style=discord.ButtonStyle.primary)
    async def six_callback(self, interaction, button):
        correct_player = await check_player(interaction)

        if correct_player:
            await handle_click(self, button, interaction)

    @discord.ui.button(custom_id="7", label="⬜", row=2, style=discord.ButtonStyle.primary)
    async def seven_callback(self, interaction, button):
        correct_player = await check_player(interaction)

        if correct_player:
            await handle_click(self, button, interaction)

    @discord.ui.button(custom_id="8", label="⬜", row=2, style=discord.ButtonStyle.primary)
    async def eight_callback(self, interaction, button):
        correct_player = await check_player(interaction)

        if correct_player:
            await handle_click(self, button, interaction)
    
    async def on_timeout(self):
        await end_game()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command()
async def ttt(ctx):
    """
    Discord: @ttt <user>

    Initialises a tic-tact-toe game between two users
    """
    global game
    if game:
        await ctx.send("A game is currently playing")
    else:
        global friend
        global player
        global current_turn
        global board_message
        global tiles
        tiles = 0

        game = True

        global context
        context = ctx

        friend = {}
        player = {}
        
        # Set first player
        player['user'] = ctx.author.name + "#" + ctx.author.discriminator
        player['symbol'] = "❌"
        player['id'] = ctx.author.id
        player['visual_symbol'] = "X"

        mess_arr = ctx.message.content.split()

        try:
            friend_id = mess_arr[1].replace('<', '').replace('>', '').replace('@', '')
            if int(friend_id) == player['id']:
                await ctx.send("You cant play against yourself!")
                game = False
            else:
                # Set friend to play with
                get_friend = await client.fetch_user(friend_id)
                friend['user'] = get_friend.name + "#" + get_friend.discriminator
                friend['symbol'] = "⭕"
                friend['id'] = friend_id
                friend['visual_symbol'] = "O"

                # Send initiation message
                message = "Initiating Game: <@{author}> vs <@{friend}>".format(author=ctx.author.id, friend=friend['id'])
                
                # Set who goes first (sender)
                current_turn = player

                await ctx.send(message)
                view = Board()
                view.timeout = 60.0
                board_message = await ctx.send("Hi!", view=view)
                await ctx.send("The timeout for this game is 60s")
                await ctx.send("Its your turn <@{player}>".format(player=current_turn['id']))
        except:
            await ctx.send("Please ensure you use the format: $ttt @friend")
            game = False


client.run("PLACE TOKEN HERE")
