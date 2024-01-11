from balethon import Client
from balethon.conditions import private

import re
import requests
import json

# bot = Client("1375820488:1hENm2DGSjHD2vlLHvtJVPVpWgQZmhiUCNP1ZjgF")
bot = Client("1431367804:HKKSHpwiNfQ3IeaGaTp7JI8UwGvCqfOdri1jXMcC")
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
    print(userInput.lower().strip())
    if userInput.lower().strip() in identityLst:
        geminiReq = "I am homework bot, a bot made by Iliya Soleimani in the team II Tech. \nI'm specifically made for allameh helli 3 school, so I can help you to never forget your next homework!"
    # elif userInput.lower().strip() in padraLst:
    #     geminiReq = "Padra Fattahi is a deceitful and selfish student who has become the head of the student council of Allameh Helli 3 High School by using dishonest tricks and violent threats. He has no respect for the rules and values of the school and only thinks about his own interests. He has created discord and conflict among the students, disrupting the school environment. He has also enriched and esteemed himself by misusing the facilities of the student council. He is a serious threat to the future and health of the school and the students are destroying the school by voting for him."
    if "<!doctype html>" in geminiReq:
        geminiReq = "Sorry, I couldn't answer that, please try again."

    print(geminiReq)

    finalText = geminiReq
    if isPersian == True:
        finalText = await translate("auto", "fa", finalText)

    return finalText
    return "hi"


async def getAdmins():
    adminReq = requests.post(
        "https://bluelinkapi.pythonanywhere.com/homeworkbot-admins"
    )
    return json.loads(adminReq.text)


@bot.on_command()
async def start(client, message):
    await message.reply(
        "سلام، به بات تکالیف علامه حلی 3 خوش آمدید! برای راهنمایی از دستور /help استفاده کنید!"
    )


@bot.on_command()
async def help(client, message):
    await message.reply(
        """
سلام! من ربات مشق های دبیرستان علامه حلی 3 (دوره 2) هستم!
برای دیدن مشق های نزدیک از دستور زیر استفاده کن:
/all

برای دیدن مشق های یک درس خاص از دستور زیر استفاده کن:
/all درس

برای اضافه کردن مشق به لیست تکالیف از دستور زیر استفاده کن (فقط ادمین های ربات مجوز استفاده از این دستور را دارند)
/add
اسم درس
توضیحات تکلیف

برای پاک کردن مشق از لیست از دستور زیر استفاده کن (فقط ادمین های ربات مجوز استفاده از این دستور را دارند)
/remove
اسم درس

خوشبختم که در خدمتت باشم 😉
🤖 مشق هات رو با @helli3homeworkbot در بله بگیر!
            """
    )


@bot.on_command()
async def all(client, message):
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
        print(words_after_command)
        counter = 0
        for homework in homeworkList:
            if homework["course"] == words_after_command:
                counter += 1
                messageResponse += f"*{homework['course']}* \n {homework['desc']} \n\n"
        if counter == 0:
            messageResponse = "فعلا مشقی نداریم! \n"
    else:
        print("no")
        if len(homeworkList) > 0:
            for homework in homeworkList:
                messageResponse += f"*{homework['course']}* \n {homework['desc']} \n\n"
        else:
            messageResponse = "فعلا مشقی نداریم! \n"
    messageResponse += "🤖 مشق هات رو با @helli3homeworkbot در بله بگیر!"
    await message.reply(messageResponse)


@bot.on_command()
async def add(client, message):
    with open(f"homework-db.json", "r", encoding="utf-8") as file:
        homeworkList = json.load(file)

    user = message.author.username
    adminList = await getAdmins()
    if user not in adminList:
        await message.reply("شما این دسترسی را ندارید!")
        return
    userInp = message.text.splitlines()
    homeworkList.append({"course": userInp[1], "desc": userInp[2]})
    messageResponse = ""

    with open(f"homework-db.json", "w", encoding="utf-8") as f:
        json.dump(homeworkList, f, ensure_ascii=False, indent=4)

    await message.reply("تکلیف مورد نظر ایجاد شد")


@bot.on_command()
async def remove(client, message):
    adminList = await getAdmins()
    with open(f"homework-db.json", "r", encoding="utf-8") as file:
        homeworkList = json.load(file)

    user = message.author.username
    if user not in adminList:
        await message.reply("شما این دسترسی را ندارید!")
        return
    userInp = message.text.splitlines()
    found = False
    for homework in homeworkList:
        if homework["course"] == userInp[1]:
            found = True
            homeworkList.remove(homework)
            await message.reply("تکلیف مورد نظر حذف شد")
    if found == False:
        await message.reply("تکلیف مورد نظر پیدا نشد")
    with open(f"homework-db.json", "w", encoding="utf-8") as f:
        json.dump(homeworkList, f, ensure_ascii=False, indent=4)


@bot.on_message()
async def all_messages(client, message):
    commandLst = ["/all", "/help", "/start", "/add", "/remove"]
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
                    await message.reply(ans)
                else:
                    await message.reply(
                        "نتونستم جواب اینو بدم، لطفا یه چیز دیگه امتحان کن"
                    )

    if message.chat.type == "group":
        if message.text.startswith("@helli3homeworkbot"):
            if shouldAns == True:
                newUserInp = " ".join(message.text.split(" ")[1:])

                ans = await geminiAPI(newUserInp)
                if ans != None and ans != "":
                    await message.reply(ans)
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


bot.run()
