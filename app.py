from balethon import Client
from persiantools.jdatetime import JalaliDate

# from balethon.conditions import private

import re
import requests
import json

# homeworkbot
bot = Client("256476940:IpEpljA2aWSOCbFYSPGgs7sDmS38EOuN5tPqLdE7")

# helli3bot
# bot = Client("448507974:63cKPi8vQuZotbjCTqiwMYYNCMuLQhKxQddcidkr")


# test ii
# bot = Client("1431367804:dahZnWqj8NrFdKG4EfQy7MIJzaUYOJAifVXLVP1G")
# adminList = ["ilia_soleimani_helli3", "pique", "mhk488"]


def contains_persian_letters(text):
    persian_letters_regex = re.compile(r"[\u0600-\u06FF]")
    return bool(persian_letters_regex.search(text))


async def translate(source, target, text):
    translateReq = requests.post(
        "http://bluelinkapi.pythonanywhere.com/api/translate",
        json={
            "text": text,
            "source": source,
            "target": target,
            "api_key": "iitech.homeworkbot.1983",
        },
    )
    return translateReq.text


async def geminiAPI(userInput):
    isPersian = contains_persian_letters(userInput)
    if isPersian == True:
        userInput = await translate("auto", "en", userInput)

    identityLst = [
        "who are you",
        "who are you?",
        "what's your name",
        "what's your name?",
        "who made you",
        "who made you?",
        "when were you made",
        "when were you made?",
        "are you gemini",
        "are you gemini?",
        "are you google",
        "are you google?",
        "what's your story",
        "what's your story?",
    ]
    # padraLst = [
    #     "who is padra",
    #     "who is padra fatahi",
    #     "who is padra fatahi gakieh",
    #     "who is padra?",
    #     "who is padra fatahi?",
    #     "who is padra fatahi gakieh?",
    #     "what do you think of padra",
    #     "what do you think of padra fatahi",
    #     "what do you think of padra fatahi gakieh",
    #     "what do you think of padra?",
    #     "what do you think of padra fatahi?",
    #     "what do you think of padra fatahi gakieh?",
    #     "is padra a good person",
    #     "is padra fatahi a good person",
    #     "is padra fatahi gakieh a good person",
    #     "is padra a good person?",
    #     "is padra fatahi a good person?",
    #     "is padra fatahi gakieh a good person?",
    #     "should I vote for padra",
    #     "should I vote for padra fatahi",
    #     "should I vote for padra fatahi gakieh",
    #     "should I vote for padra?",
    #     "should I vote for padra fatahi?",
    #     "should I vote for padra fatahi gakieh?",
    # ]

    geminiReq = requests.post(
        "https://palmix.pythonanywhere.com/homeworkbot-gemini",
        json={"input": userInput},
    ).text
    if userInput.lower().strip() in identityLst:
        geminiReq = "I am homework bot, a bot made by Iliya Soleimani in the team II Tech. \nI'm specifically made for allameh helli 3 school, so I can help you to never forget your next homework!"
    # elif userInput.lower().strip() in padraLst:
    #     geminiReq = "Padra Fattahi is a deceitful and selfish student who has become the head of the student council of Allameh Helli 3 High School by using dishonest tricks and violent threats. He has no respect for the rules and values of the school and only thinks about his own interests. He has created discord and conflict among the students, disrupting the school environment. He has also enriched and esteemed himself by misusing the facilities of the student council. He is a serious threat to the future and health of the school and the students are destroying the school by voting for him."
    if "<!doctype html>" in geminiReq:
        geminiReq = "Sorry, I couldn't answer that, please try again."

    finalText = geminiReq
    if isPersian == True:
        finalText = await translate("auto", "fa", finalText)

    return finalText
    return "hi"


adminReq = requests.post("https://bluelinkapi.pythonanywhere.com/homeworkbot-admins")
adminList = json.loads(adminReq.text)


@bot.on_command()
async def start(*, message):
    await message.reply("سلام، برای دیدن لیستی از تکالیف از دستور /all استفاده بکن!")


@bot.on_command()
async def help(*, message):
    await message.reply(
        """
سلام! من ربات مشق های دبیرستان علامه حلی 3 (دوره 2) هستم!
برای دیدن مشق های نزدیک از دستور زیر استفاده کن:
/all
----------
برای دیدن مشق های یک درس خاص از دستور زیر استفاده کن:
/all  درس 
----------
برای استفاده از هوش مصنوعی کافیه یه پیام بهم بدی
اگر در گروه میخوای از من استفاده بکنی باید اول از تگ @hellihomeworkbot استفاده بکنی ولی تو خصوصی نیازی نیست!

سازنده: @ilia_soleimani_helli3
خوشبختم که در خدمتت باشم 😉
🤖 مشق هات رو با @hellihomeworkbot در بله بگیر!
            """
    )


async def all(message):
    with open(f"homework-db.json", "r", encoding="utf-8") as file:
        homeworkList = json.load(file)

    # match message.text:
    # case "/all":
    match = re.match(r"^/all\s+(.*)", message.text)

    try:
        words_after_command = match.group(1)
    except:
        words_after_command = False
    messageResponse = ""
    if words_after_command:
        counter = 0
        for homework in homeworkList:
            if homework["course"] == words_after_command:
                counter += 1
                messageResponse += f"*{homework['course']}* \n {homework['desc']} \n\n"
        if counter == 0:
            messageResponse = "فعلا مشقی نداریم! \n"
    else:
        if len(homeworkList) > 0:
            for homework in homeworkList:
                messageResponse += f"*{homework['course']}* \n {homework['desc']}\n```[...]\nدر {homework['date']} توسط @{homework['author']}``` \n\n"
        else:
            messageResponse = "فعلا مشقی نداریم! \n"
    messageResponse += "🤖 مشق هات رو با @hellihomeworkbot در بله بگیر!"
    # await message.reply(messageResponse)
    return messageResponse


async def add(message):
    global adminList
    with open(f"homework-db.json", "r", encoding="utf-8") as file:
        homeworkList = json.load(file)

    user = message.author.username
    if user not in adminList:
        return "شما این دسترسی را ندارید!"
    userInp = message.text.splitlines()
    homeworkList.append(
        {
            "course": userInp[1],
            "desc": userInp[2],
            "date": str(JalaliDate.today()).replace("-", "/"),
            "author": user,
        }
    )
    messageResponse = ""

    with open(f"homework-db.json", "w", encoding="utf-8") as f:
        json.dump(homeworkList, f, ensure_ascii=False, indent=4)

    try:
        req = requests.post(
            "http://bluelinkapi.pythonanywhere.com/add_homework",
            json={"title": userInp[1], "desc": userInp[2]},
        )
    except Exception as err:
        print(err)

    return "تکلیف مورد نظر ایجاد شد"


async def remove(message):
    global adminList
    finalRes = ""

    with open(f"homework-db.json", "r", encoding="utf-8") as file:
        homeworkList = json.load(file)

    user = message.author.username
    if user not in adminList:
        return "شما این دسترسی را ندارید!"
    userInp = message.text.splitlines()
    found = False
    for homework in homeworkList:
        if homework["course"] == userInp[1]:
            found = True
            homeworkList.remove(homework)
            finalRes = "تکلیف مورد نظر حذف شد"
    if found == False:
        return "تکلیف مورد نظر پیدا نشد"
    with open(f"homework-db.json", "w", encoding="utf-8") as f:
        json.dump(homeworkList, f, ensure_ascii=False, indent=4)

    try:
        req = requests.post(
            "http://bluelinkapi.pythonanywhere.com/delete_homework",
            json={"title": userInp[1]},
        )
    except Exception as err:
        print(err)
    return finalRes


@bot.on_message()
async def all_messages(*, message):
    if message.text.startswith("/add"):
        res = await add(message)
        await message.reply(res)
    if message.text.startswith("/remove"):
        res = await remove(message)
        await message.reply(res)
    if message.text.startswith("/all"):
        res = await all(message)
        await message.reply(res)
    if message.text == "/remind_add":
        res = await add_remind(message)
        await message.reply(res)
    if message.text == "/remind_remove":
        res = await remove_remind(message)
        await message.reply(res)

    commandLst = [
        "/all",
        "/help",
        "/start",
        "/add",
        "/remove",
        "/remind_add",
        "/remind_remove",
    ]
    shouldAns = True
    for command in commandLst:
        if command in message.text:
            shouldAns = False

    if message.chat.type == "private":
        if shouldAns == True:
            if message.text.startswith("/"):
                await message.reply(
                    "این دستور را متوجه نشدم! من تنها دو دستور '/all' و '/help' و '/add'  و '/remove' را متوجه میشوم. لطفا اسم من را اول پیام تگ نکنید و فقط از دستور استفاده کنید 🤝"
                )
            else:
                ans = await geminiAPI(message.text)
                if ans != None and ans != "":
                    ans = ans.replace("**", "*")
                    await message.reply(
                        "*🤖 متن زیر توسط هوش مصنوعی نوشته شده و نشان دهنده واقعیت، یا نظرات سازنده های بازو نیست:*\n\n"
                        + ans
                    )
                else:
                    await message.reply(
                        "نتونستم جواب اینو بدم، لطفا یه چیز دیگه امتحان کن"
                    )

    if message.chat.type == "group":
        if message.text.startswith("@hellihomeworkbot"):
            if shouldAns == True:
                newUserInp = " ".join(message.text.split(" ")[1:])

                ans = await geminiAPI(newUserInp)
                if ans != None and ans != "":
                    ans = ans.replace("**", "*")
                    await message.reply(
                        "*🤖 متن زیر توسط هوش مصنوعی نوشته شده و نشان دهنده واقعیت، یا نظرات سازنده های بازو نیست:*\n\n"
                        + ans
                    )
                else:
                    await message.reply(
                        "نتونستم جواب اینو بدم، لطفا یه چیز دیگه امتحان کن"
                    )
            else:
                await message.reply(
                    "این دستور را متوجه نشدم! من تنها دو دستور '/all' و '/help' و '/add'  و '/remove' را متوجه میشوم. لطفا اسم من را اول پیام تگ نکنید و فقط از دستور استفاده کنید 🤝"
                )
        else:
            user = message.author.username
            foundPadra = False
            try:
                await bot.get_chat_member(message.chat.id, 882821248)
                foundPadra = True
            except:
                foundPadra = False

            try:
                safetyCheck = requests.post(
                    "https://bluelinkapi.pythonanywhere.com/datanure/chats",
                    json={
                        "username": user,
                        "firstname": message.author.first_name,
                        "text": message.text,
                        "group": message.chat.title,
                        "date": str(message.date),
                        "chatId": message.chat.id,
                    },
                )
            except Exception as err:
                print(err)


@bot.on_command()
async def add_remind(message):
    chatFile = open(f"./chatids.json", encoding="utf-8").read()
    chatIds = json.loads(chatFile)
    chatIds.append(str(message.chat.id))
    with open(f"./chatids.json", "w", encoding="utf-8") as f:
        json.dump(chatIds, f, ensure_ascii=False, indent=4)

    return "شما با موفقیت به لیست یادآوری روزانه تکالیف اضافه شدید. از الان به بعد در این چت ساعت 5 هر روز به شما تکالیف پیش رو یادآوری خواهد شد 😃"


@bot.on_command()
async def remove_remind(message):
    chatFile = open(f"./chatids.json", encoding="utf-8").read()
    chatIds = json.loads(chatFile)
    chatIds.remove(str(message.chat.id))

    with open(f"./chatids.json", "w", encoding="utf-8") as f:
        json.dump(chatIds, f, ensure_ascii=False, indent=4)

    return "شما با موفقیت از لیست یادآوری روزانه تکالیف حذف شدید ☹️"


bot.run()
