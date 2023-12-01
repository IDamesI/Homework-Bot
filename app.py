from balethon import Client
import re

bot = Client("1664217599:hAvPbUuJHOcbG4nGgEHzDruN8eTSgAVII4g1Iips")
homeworkList = [
    {"course": "شیمی", "desc": "کل فصل 1 و بخش های درس داده شده فصل 2 از کتاب تست"},
    {"course": "ریاضی", "desc": "کل فصل 2 از کتاب تست"},
]
adminList = ["ilia_soleimani_helli3", "pique", "mhk488"]


@bot.on_message()
async def greet(client, message):
    # match message.text:
    # case "/all":
    match = re.match(r"^/all\s+(.*)", message.text)
    matchadd = re.match(r"^/add\s+(.*)", message.text)
    if match or message.text == "/all":
        try:
            words_after_command = match.group(1)
        except:
            words_after_command = False
        messageResponse = ""
        if words_after_command:
            print(words_after_command)
            counter = 0
            for homework in homeworkList:
                if homework["course"] == words_after_command:
                    counter += 1
                    messageResponse += (
                        f"*{homework['course']}* \n {homework['desc']} \n\n"
                    )
            if counter == 0:
                messageResponse = "فعلا مشقی نداریم! \n"
        else:
            print("no")
            if len(homeworkList) > 0:
                for homework in homeworkList:
                    messageResponse += (
                        f"*{homework['course']}* \n {homework['desc']} \n\n"
                    )
            else:
                messageResponse = "فعلا مشقی نداریم! \n"
        messageResponse += "🤖 مشق هات رو با @helli3homeworkbot در بله بگیر!"
        await message.reply(messageResponse)
    elif matchadd or message.text == "/add":
        user = message.author.username
        if user not in adminList:
            await message.reply("شما این دسترسی را ندارید!")
            return

        userInp = message.text.splitlines()
        homeworkList.append({"course": userInp[1], "desc": userInp[2]})
        messageResponse = ""

        await message.reply("تکلیف مورد نظر ایجاد شد")
    else:
        await message.reply(
            "این دستور را متوجه نشدم! من تنها دو دستور '/all' و '/add' را متوجه میشوم"
        )


bot.run()
