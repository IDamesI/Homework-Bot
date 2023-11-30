from balethon import Client

bot = Client("1664217599:hAvPbUuJHOcbG4nGgEHzDruN8eTSgAVII4g1Iips")
homeworkList = [
    {"course": "شیمی", "desc": "کل فصل 1 و بخش های درس داده شده فصل 2 از کتاب تست"},
    {"course": "ریاضی", "desc": "کل فصل 2 از کتاب تست"},
]


@bot.on_message()
async def greet(client, message):
    match message.text:
        case "/all":
            messageResponse = ""
            if len(homeworkList) > 0:
                for homework in homeworkList:
                    messageResponse += (
                        f"*{homework['course']}* \n {homework['desc']} \n\n"
                    )
            else:
                messageResponse = "فعلا مشقی نداریم! \n"
            messageResponse += "🤖 مشق هات رو با @helli3homeworkbot در بله بگیر!"
            await message.reply(messageResponse)
        case "/add":
            await message.reply("You can't do that")
        case _:
            await message.reply("That's not a command")


bot.run()
