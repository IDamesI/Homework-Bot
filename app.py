from balethon import Client
from balethon.objects import InlineKeyboard
from persiantools.jdatetime import JalaliDate

# from balethon.conditions import private

import re
import requests
import json

# homeworkbot
# bot = Client("256476940:IpEpljA2aWSOCbFYSPGgs7sDmS38EOuN5tPqLdE7")

# helli3bot
# bot = Client("448507974:63cKPi8vQuZotbjCTqiwMYYNCMuLQhKxQddcidkr")


# test ii
bot = Client("1431367804:FAuaYDMVmedSlQx2C31vNo3qsEfh2vobPPKnQGyh")
# adminList = ["ilia_soleimani_helli3", "pique", "mhk488"]

adminReq = open("./admins.json", "r", encoding="utf-8").read()
adminReq2 = open("./admins-class.json", "r", encoding="utf-8").read()
adminList = json.loads(adminReq)
adminDic = json.loads(adminReq2)


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

    messageResponse += "ادمین های کلاس شما: "
    for admin in adminDic["101"]:
        messageResponse += "@" + admin + " "
    messageResponse += "\n"
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
            "course": userInp[1].strip(),
            "desc": userInp[2].strip(),
            "date": str(JalaliDate.today()).replace("-", "/"),
            "author": user,
        }
    )
    messageResponse = ""

    with open(f"homework-db.json", "w", encoding="utf-8") as f:
        json.dump(homeworkList, f, ensure_ascii=False, indent=4)

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

    return finalRes


async def setClass(message):
    await message.reply(
        "کلاس خود را انتخاب کنید",
        InlineKeyboard(
            [("۱۰۱", "101")], [("۱۰۲", "102")], [("۱۰۳", "103")], [("۱۰۴", "104")]
        ),
    )


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
    if message.text == "/class":
        await setClass(message)


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


@bot.on_callback_query()
async def answer_callback_query(callback_query):
    classFile = open("./classes.json", "r", encoding="utf-8").read()
    classDb = json.loads(classFile)

    classDb[str(callback_query.author.id)] = str(callback_query.data)
    with open("./classes.json", "w", encoding="utf-8") as f:
        json.dump(classDb, f, ensure_ascii=False, indent=4)
    await callback_query.answer(f"شما وارد کلاس {callback_query.data} شدید!")


bot.run()
