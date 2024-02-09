from balethon import Client
from balethon.conditions import private

bot = Client("1431367804:dahZnWqj8NrFdKG4EfQy7MIJzaUYOJAifVXLVP1G")


@bot.on_command(private)
async def start(*, message):
    await message.reply("Hello, I'm the commands bot\nUse /help to see my commands")


@bot.on_command(private, name="help")
async def help_command(*, message):
    await message.reply("/say_hello\n/count_to_ten")


@bot.on_command(private)
async def say_hello(*, message):
    await message.reply("Hello my dear and precious user!")


@bot.on_command(private)
async def count_to_ten(*, message):
    counting_message = await message.reply("I will start to count to ten now")
    for i in range(1, 11):
        await counting_message.edit_text(str(i))


@bot.on_message()
async def all_messages(*, message):
    print("hi")


bot.run()
