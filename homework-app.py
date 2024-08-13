import os

from balethon import Client
from balethon.objects import InlineKeyboard
from persiantools.jdatetime import JalaliDate

# from balethon.conditions import private

import re
import requests
import json

import asyncio
import subprocess

# homeworkbot
bot = Client("256476940:IpEpljA2aWSOCbFYSPGgs7sDmS38EOuN5tPqLdE7")

# helli3bot
# bot = Client("448507974:63cKPi8vQuZotbjCTqiwMYYNCMuLQhKxQddcidkr")


# test ii
# bot = Client("1431367804:FAuaYDMVmedSlQx2C31vNo3qsEfh2vobPPKnQGyh")
# adminList = ["ilia_soleimani_helli3", "pique", "mhk488"]

adminReq = open("./admins.json", "r", encoding="utf-8").read()
adminList = json.loads(adminReq)
adminReq2 = open("./admins-class.json", "r", encoding="utf-8").read()
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
----------
برای عوض کردن کلاس خود و تنظیمات یادآوری تکالیف از دستور /settings استفاده کن!

سازنده: @ilia_soleimani_helli3
خوشبختم که در خدمتت باشم 😉
🤖 مشق هات رو با @hellihomeworkbot در بله بگیر!
            """
    )


async def all(message):
    classesDb = json.loads(open("./classes.json", "r", encoding="utf-8").read())
    if str(message.author.id) not in classesDb:
        await message.reply(
            "شما کلاس خود را انتخاب نکرده اید، لطفا کلاس خود را انتخاب کنید:",
            InlineKeyboard(
                [("۱۰۱", "101")],
                [("۱۰۲", "102")],
                [("۱۰۳", "103")],
                [("۱۰۴", "104")],
                [("۲۰۱", "201")],
                [("۲۰۲", "202")],
                [("۲۰۳", "203")],
                [("۲۰۴", "204")],
            ),
        )
        return
    userClass = classesDb[str(message.author.id)]

    with open(f"homework-db.json", "r", encoding="utf-8") as file:
        homeworkListFull = json.load(file)
    homeworkList = []
    for homework in homeworkListFull:
        if homework["class"] == userClass:
            homeworkList.append(homework)

    # match message.text:
    # case "/all":
    match = re.match(r"^/all\s+(.*)", message.text)

    try:
        words_after_command = match.group(1)
    except:
        words_after_command = False

    messageResponse = f"---------- *تکالیف کلاس {userClass}* ----------\n\n"
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
                messageResponse += f"*{homework['course']}* \n {homework['desc']}\n ```[...]\nدر {homework['date']} توسط @{homework['author']}``` "
        else:
            messageResponse = "فعلا مشقی نداریم! \n"
    messageResponse += "\n"
    if len(adminDic[userClass]) > 0:
        messageResponse += "_ادمین های کلاس شما: "
        for admin in adminDic[userClass]:
            messageResponse += "@" + admin + " "
        messageResponse += "_"
    else:
        messageResponse += "_کلاس شما ادمین ندارد، همین حالا به @ilia_soleimani_helli3 پیام دهید و ادمین این کلاس شوید!_"

    messageResponse += "\n\n"
    messageResponse += "🤖 مشق هات رو با @hellihomeworkbot در بله بگیر!"
    # await message.reply(messageResponse)

    analytics = json.loads(open("analytics.json", "r", encoding="utf-8").read())
    if str(JalaliDate.today()) not in analytics:
        analytics[str(JalaliDate.today())] = 0
    analytics[str(JalaliDate.today())] += 1
    with open("analytics.json", "w", encoding="utf-8") as file:
        json.dump(analytics, file, ensure_ascii=False, indent=4)

    await message.reply(messageResponse)


async def add(message):
    classesDb = json.loads(open("./classes.json", "r", encoding="utf-8").read())
    if str(message.author.id) not in classesDb:
        await message.reply(
            "شما کلاس خود را انتخاب نکرده اید، لطفا کلاس خود را انتخاب کنید:",
            InlineKeyboard(
                [("۱۰۱", "101")],
                [("۱۰۲", "102")],
                [("۱۰۳", "103")],
                [("۱۰۴", "104")],
                [("۲۰۱", "201")],
                [("۲۰۲", "202")],
                [("۲۰۳", "203")],
                [("۲۰۴", "204")],
            ),
        )
        return
    userClass = classesDb[str(message.author.id)]

    global adminList
    with open(f"homework-db.json", "r", encoding="utf-8") as file:
        homeworkList = json.load(file)

    user = str(message.author.id)
    if user not in adminList:
        return "شما این دسترسی را ندارید!"
    userInp = message.text.splitlines()
    homeworkList.append(
        {
            "course": userInp[1].strip(),
            "desc": userInp[2].strip(),
            "date": str(JalaliDate.today()).replace("-", "/"),
            "author": user,
            "class": userClass,
        }
    )
    messageResponse = ""

    with open(f"homework-db.json", "w", encoding="utf-8") as f:
        json.dump(homeworkList, f, ensure_ascii=False, indent=4)

    return "تکلیف مورد نظر ایجاد شد"


async def remove(message):
    classesDb = json.loads(open("./classes.json", "r", encoding="utf-8").read())
    if str(message.author.id) not in classesDb:
        await message.reply(
            "شما کلاس خود را انتخاب نکرده اید، لطفا کلاس خود را انتخاب کنید:",
            InlineKeyboard(
                [("۱۰۱", "101")],
                [("۱۰۲", "102")],
                [("۱۰۳", "103")],
                [("۱۰۴", "104")],
                [("۲۰۱", "201")],
                [("۲۰۲", "202")],
                [("۲۰۳", "203")],
                [("۲۰۴", "204")],
            ),
        )
        return
    userClass = classesDb[str(message.author.id)]

    global adminList
    finalRes = ""

    with open(f"homework-db.json", "r", encoding="utf-8") as file:
        homeworkList = json.load(file)

    user = str(message.author.id)
    if user not in adminList:
        return "شما این دسترسی را ندارید!"
    userInp = message.text.splitlines()
    found = False
    for homework in homeworkList:
        if homework["course"] == userInp[1] and homework["class"] == userClass:
            found = True
            homeworkList.remove(homework)
            finalRes = "تکلیف مورد نظر حذف شد"
    if found == False:
        return f"تکلیف مورد نظر پیدا نشد - کلاس شما {userClass} است"
    with open(f"homework-db.json", "w", encoding="utf-8") as f:
        json.dump(homeworkList, f, ensure_ascii=False, indent=4)

    return finalRes


async def settings(message):
    await message.reply(
        "یکی از گزینه های زیر را انتخاب کنید",
        InlineKeyboard(
            [("یادآوری تکالیف", "settings_remind"), ("کلاس", "settings_class")]
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
        await all(message)
    if message.text == "/settings":
        await settings(message)
    if message.text.startswith("/admin_add"):
        await add_admin(message)
    if message.text.startswith("/admin_remove"):
        await remove_admin(message)
    if message.text == "/help_admin":
        await message.reply(
            """*راهنمای ادمین ها*

*ساخت جزوه* - باید از دستور /add استفاده کنید سپس در خط بعد اسم درس و خط بعد توضیحات تکلیف را بنویسید، توجه کنید که درس شما تنها و تنها به لیست کلاسی که در تنظیمات قرار داده اید اضافه میشود

/add
ریاضی
تست 1 تا 10

*حذف جزوه* - باید از دستور /remove استفاده کنید سپس در خط بعد اسم درس را بنویسید. توجه کنید که شما تنها و تنها توانایی حذف تکالیف کلاس خودتان را دارید که در تنظیمات قرار دادید

/remove
ریاضی"""
        )
    if message.text.startswith("/backup"):
        await send_backup(message)
    if message.text.startswith("/write_file"):
        await write_file(message)
    if message.text.startswith("/read_file"):
        await read_file(message)
    if message.text == "/help_master":
        await message.reply(
            """*Master Commands:*

/add
add
coursename
coursedesc

/remove
remove
coursename

/all
all coursename

/settings
settings

/admin_add
admin_add userid username( without @ ) class

/admin_remove
admin_remove userid username( without @ ) class

/help_admin
help_admin

/backup
backup

/write_file
write_file filename filedata

/read_file
read_file filename

/ls
ls"""
        )
    if message.text.startswith("/ls"):
        await ls(message)


@bot.on_callback_query()
async def answer_callback_query(callback_query):
    if callback_query.data in ["101", "102", "103", "104", "201", "202", "203", "204"]:
        classFile = open("./classes.json", "r", encoding="utf-8").read()
        classDb = json.loads(classFile)

        classDb[str(callback_query.author.id)] = str(callback_query.data)
        with open("./classes.json", "w", encoding="utf-8") as f:
            json.dump(classDb, f, ensure_ascii=False, indent=4)
        await callback_query.answer(f"شما وارد کلاس {callback_query.data} شدید!")
    elif callback_query.data == "settings_class":
        await callback_query.message.reply(
            "کلاس خود را انتخاب کنید",
            InlineKeyboard(
                [("۱۰۱", "101")],
                [("۱۰۲", "102")],
                [("۱۰۳", "103")],
                [("۱۰۴", "104")],
                [("۲۰۱", "201")],
                [("۲۰۲", "202")],
                [("۲۰۳", "203")],
                [("۲۰۴", "204")],
            ),
        )
    elif callback_query.data == "settings_remind":
        await callback_query.message.reply(
            "یادآوری روزانه تکالیف روشن باشد یا خاموش؟",
            InlineKeyboard(
                [("خاموش", "settings_remind_off")], [("روشن", "settings_remind_on")]
            ),
        )
    elif callback_query.data == "settings_remind_on":
        res = await add_remind(callback_query.message)
        await callback_query.message.reply(res)

    elif callback_query.data == "settings_remind_off":
        res = await remove_remind(callback_query.message)
        await callback_query.message.reply(res)


async def add_remind(message):
    chatFile = open(f"./chatids.json", encoding="utf-8").read()
    chatIds = json.loads(chatFile)
    chatIds.append(str(message.chat.id))
    with open(f"./chatids.json", "w", encoding="utf-8") as f:
        json.dump(chatIds, f, ensure_ascii=False, indent=4)

    return "شما با موفقیت به لیست یادآوری روزانه تکالیف اضافه شدید. از الان به بعد در این چت ساعت 5 هر روز به شما تکالیف پیش رو یادآوری خواهد شد 😃"


async def remove_remind(message):
    chatFile = open(f"./chatids.json", encoding="utf-8").read()
    chatIds = json.loads(chatFile)
    chatIds.remove(str(message.chat.id))
    with open(f"./chatids.json", "w", encoding="utf-8") as f:
        json.dump(chatIds, f, ensure_ascii=False, indent=4)

    return "شما با موفقیت از لیست یادآوری روزانه تکالیف حذف شدید ☹️"


async def add_admin(message):
    if len(message.text.split(" ")) != 4:
        await message.reply(
            "اشتباه است، باید اینطوری باشد \n /admin userid username( without @ ) class"
        )
        return
    userid = message.author.id
    newid = message.text.split(" ")[1].strip()
    newusername = message.text.split(" ")[2].strip()
    newidclass = message.text.split(" ")[3].strip()
    if str(userid) != "1215365851":
        await message.reply("شما دسترسی استفاده از این کامند را ندارید!")
        return

    if newid not in adminList:
        adminList.append(newid)
    if newusername not in adminDic[str(newidclass)]:
        adminDic[str(newidclass)].append(newusername)
    with open("./admins.json", "w", encoding="utf-8") as f:
        json.dump(adminList, f, ensure_ascii=False, indent=4)

    with open("./admins-class.json", "w", encoding="utf-8") as f:
        json.dump(adminDic, f, ensure_ascii=False, indent=4)
    await message.reply("دستور با موفقیت انجام شد")


async def remove_admin(message):
    if len(message.text.split(" ")) != 4:
        await message.reply(
            "اشتباه است، باید اینطوری باشد \n /admin userid username( without @ ) class"
        )
        return
    userid = message.author.id
    newid = message.text.split(" ")[1].strip()
    newusername = message.text.split(" ")[2].strip()
    newidclass = message.text.split(" ")[3].strip()
    if str(userid) != "1215365851":
        await message.reply("شما دسترسی استفاده از این کامند را ندارید!")
        return

    if newid in adminList:
        adminList.remove(newid)
    if newusername in adminDic[str(newidclass)]:
        adminDic[str(newidclass)].remove(newusername)
    with open("./admins.json", "w", encoding="utf-8") as f:
        json.dump(adminList, f, ensure_ascii=False, indent=4)

    with open("./admins-class.json", "w", encoding="utf-8") as f:
        json.dump(adminDic, f, ensure_ascii=False, indent=4)
    await message.reply("دستور با موفقیت انجام شد")


async def send_backup(message):
    userid = message.author.id
    if str(userid) != "1215365851":
        await message.reply("شما دسترسی استفاده از این کامند را ندارید!")
        return
    await bot.send_document(message.chat.id, "admins-class.json", "admins-class.json")
    await bot.send_document(message.chat.id, "admins.json", "admins.json")
    await bot.send_document(message.chat.id, "chatids.json", "chatids.json")
    await bot.send_document(message.chat.id, "classes.json", "classes.json")
    await bot.send_document(message.chat.id, "homework-db.json", "homework-db.json")


async def write_file(message):
    userid = message.author.id
    if str(userid) != "1215365851":
        await message.reply("شما دسترسی استفاده از این کامند را ندارید!")
        return

    fileName = message.text.split(" ")[1].strip()
    fileContent = " ".join(message.text.split(" ")[2:])

    if os.path.exists(fileName):
        fileData = open(fileName, "r", encoding="utf-8").read()
        await message.reply(f"*Prev:* \n{fileData} \n\n\n\n *New:* \n{fileContent}")
        with open(fileName, "w", encoding="utf-8") as f:
            f.write(fileContent)
        return
    await message.reply("File doesn't exist")
    return


async def read_file(message):
    userid = message.author.id
    if str(userid) != "1215365851":
        await message.reply("شما دسترسی استفاده از این کامند را ندارید!")
        return

    fileName = message.text.split(" ")[1].strip()

    if os.path.exists(fileName):
        fileData = open(fileName, "r", encoding="utf-8").read()
        await message.reply(f"*{fileName}:* \n{fileData}")
        return
    await message.reply("File doesn't exist")
    return


async def ls(message):
    userid = message.author.id
    if str(userid) != "1215365851":
        await message.reply("شما دسترسی استفاده از این کامند را ندارید!")
        return

    files = os.listdir()
    file_list = []
    for file in files:
        if os.path.isdir(file):
            file_list.append(f"{file}\t")
        else:
            file_list.append(file)

    await message.reply("\n".join(file_list))


bot.run()
