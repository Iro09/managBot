"""
MIT License

Copyright (c) 2021 TheHamkerCat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import asyncio
import importlib
import re
from contextlib import closing, suppress

from pyrogram import enums, filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from uvloop import install

from nezuko import BOT_NAME, BOT_USERNAME, LOG_GROUP_ID, aiohttpsession, app
from nezuko.modules import ALL_MODULES
from nezuko.modules.sudoers import bot_sys_stats
from nezuko.utils import paginate_modules
from nezuko.utils.constants import MARKDOWN
from nezuko.utils.dbfunctions import clean_restart_stage

loop = asyncio.get_event_loop()

HELPABLE = {}


async def start_bot():
    global HELPABLE

    for module in ALL_MODULES:
        imported_module = importlib.import_module(f"nezuko.modules.{module}")
        if (
            hasattr(imported_module, "__MODULE__")
            and imported_module.__MODULE__
        ):
            imported_module.__MODULE__ = imported_module.__MODULE__
            if (
                hasattr(imported_module, "__HELP__")
                and imported_module.__HELP__
            ):
                HELPABLE[imported_module.__MODULE__.lower()] = imported_module
    bot_modules = ""
    j = 1
    for i in ALL_MODULES:
        if j == 4:
            bot_modules += "|{:<15}|\n".format(i)
            j = 0
        else:
            bot_modules += "|{:<15}".format(i)
        j += 1
    print("+===============================================================+")
    print("|                              Nezuko                           |")
    print("+===============+===============+===============+===============+")
    print(bot_modules)
    print("+===============+===============+===============+===============+")
    print(f"[INFO]: BOT STARTED AS {BOT_NAME}!")

    restart_data = await clean_restart_stage()

    try:
        print("[INFO]: SENDING ONLINE STATUS")
        if restart_data:
            await app.edit_message_text(
                restart_data["chat_id"],
                restart_data["message_id"],
                "**Restarted Successfully**",
            )

        else:
            await app.send_message(LOG_GROUP_ID, "Bot started!")
    except Exception:
        pass

    await idle()

    await aiohttpsession.close()
    print("[INFO]: CLOSING AIOHTTP SESSION AND STOPPING BOT")
    await app.stop()
    print("[INFO]: Bye!")
    for task in asyncio.all_tasks():
        task.cancel()
    print("[INFO]: Turned off!")

PM_START_TEXT = """
*ʜᴇʟʟᴏ {} !*
✪ ɪ'ᴍ ʟᴀᴋsʜʏᴀ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ [✨](https://te.legra.ph/file/ded640cc97e4d4c37cda0.jpg)
────────────────────────
× *ᴜᴘᴛɪᴍᴇ:* `{}`
× `{}` *ᴜsᴇʀs, ᴀᴄʀᴏss* `{}` *ᴄʜᴀᴛs.*
────────────────────────
✪ ʜɪᴛ /help ᴛᴏ sᴇᴇ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs.
"""


home_keyboard_pm = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="ᴄᴏᴍᴍᴀɴᴅs", callback_data="bot_commands"
            ),
            InlineKeyboardButton(
                text="ʀᴇᴘᴏ",
                url="https://github.com/LaKsH-X/NezukoBot",
            ),
        ],
        [
            InlineKeyboardButton(
                text="sʏsᴛᴇᴍ sᴛᴀᴛᴜs",
                callback_data="stats_callback",
            ),
        ],
        [
            InlineKeyboardButton(
                text="+ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ +",
                url=f"http://t.me/{BOT_USERNAME}?startgroup=new",
            )
        ],
    ]
)

home_text_pm = (
    f"ʜᴇʏ! ᴛʜɪs ɪs  {BOT_NAME}."
    + "๏ ᴀ ғᴀsᴛ ᴀɴᴅ ᴀᴅᴠᴀɴᴄᴇᴅ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ | sᴜᴘᴘᴏʀᴛ :-  @xSupport_ies."
    + "๏ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴩ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs."
)


keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="ʜᴇʟᴘ",
                url=f"t.me/{BOT_USERNAME}?start=help",
            ),
            InlineKeyboardButton(
                text="ʀᴇᴘᴏ",
                url="https://github.com/LaKsH-X/NezukoBot",
            ),
        ],
        [
            InlineKeyboardButton(
                text="sʏsᴛᴇᴍ sᴛᴀᴛᴜs",
                callback_data="stats_callback",
            ),
        ],
    ]
)


@app.on_message(filters.command("start"))
async def start(_, message):
    if message.chat.type != enums.ChatType.PRIVATE:
        return await message.reply_photo(
            photo="https://te.legra.ph/file/ded640cc97e4d4c37cda0.jpg",
            caption="Pm Me For More Details.",
            reply_markup=keyboard,
        )
    if len(message.text.split()) > 1:
        name = (message.text.split(None, 1)[1]).lower()
        if name == "mkdwn_help":
            await message.reply(
                MARKDOWN, parse_mode="html", disable_web_page_preview=True
            )
        elif "_" in name:
            module = name.split("_", 1)[1]
            text = (
                f"Here is the help for **{HELPABLE[module].__MODULE__}**:\n"
                + HELPABLE[module].__HELP__
            )
            await message.reply(text, disable_web_page_preview=True)
        elif name == "help":
            text, keyb = await help_parser(message.from_user.first_name)
            await message.reply(
                text,
                reply_markup=keyb,
            )
    else:
        await message.reply_photo(
            photo="https://te.legra.ph/file/ded640cc97e4d4c37cda0.jpg",
            caption=home_text_pm,
            reply_markup=home_keyboard_pm,
        )
    return


@app.on_message(filters.command("help"))
async def help_command(_, message):
    if message.chat.type != enums.ChatType.PRIVATE:
        if len(message.command) >= 2:
            name = (message.text.split(None, 1)[1]).lower()
            if str(name) in HELPABLE:
                key = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="ᴄʟɪᴄᴋ ʜᴇʀᴇ",
                                url=f"t.me/{BOT_USERNAME}?start=help_{name}",
                            )
                        ],
                    ]
                )
                await message.reply(
                    f"ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟʟᴏᴡ ᴛᴏ ɢᴇᴛ ʜᴇʟᴘ ᴀʙᴏᴜᴛ  {name}",
                    reply_markup=key,
                )
            else:
                await message.reply(
                    "ᴘᴍ ᴍᴇ ғᴏʀ ᴍᴏʀᴇ ᴅᴇᴛᴀɪʟs.", reply_markup=keyboard
                )
        else:
            await message.reply(
                "ᴘᴍ ᴍᴇ ғᴏʀ ᴍᴏʀᴇ ᴅᴇᴛᴀɪʟs.", reply_markup=keyboard
            )
    elif len(message.command) >= 2:
        name = (message.text.split(None, 1)[1]).lower()
        if str(name) in HELPABLE:
            text = (
                f"*ʜᴇʀᴇ ɪs ᴛʜᴇ ʜᴇʟᴘ ғᴏʀ*{HELPABLE[name].__MODULE__}**:\n"
                + HELPABLE[name].__HELP__
            )
            await message.reply(text, disable_web_page_preview=True)
        else:
            text, help_keyboard = await help_parser(
                message.from_user.first_name
            )
            await message.reply(
                text,
                reply_markup=help_keyboard,
                disable_web_page_preview=True,
            )
    else:
        text, help_keyboard = await help_parser(message.from_user.first_name)
        await message.reply(
            text, reply_markup=help_keyboard, disable_web_page_preview=True
        )
    return


async def help_parser(name, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    return (
        """ʜᴇʟʟᴏ {first_name}, ᴍʏ ɴᴀᴍᴇ ɪs {bot_name}.
ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟʟᴏᴡ ᴛᴏ ɢᴇᴛ ᴅᴇsᴄʀɪᴘᴛɪᴏɴ ᴀʙᴏᴜᴛ sᴘᴇᴄɪғɪᴄs ᴄᴏᴍᴍᴀɴᴅ.
""".format(
            first_name=name,
            bot_name=BOT_NAME,
        ),
        keyboard,
    )


@app.on_callback_query(filters.regex("bot_commands"))
async def commands_callbacc(_, CallbackQuery):
    text, keyboard = await help_parser(CallbackQuery.from_user.mention)
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=text,
        reply_markup=keyboard,
    )

    await CallbackQuery.message.delete()


@app.on_callback_query(filters.regex("stats_callback"))
async def stats_callbacc(_, CallbackQuery):
    text = await bot_sys_stats()
    await app.answer_callback_query(CallbackQuery.id, text, show_alert=True)


@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(client, query):
    home_match = re.match(r"help_home\((.+?)\)", query.data)
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    create_match = re.match(r"help_create", query.data)
    top_text = f"""
๏ ʜᴇʟʟᴏ {query.from_user.first_name}, ᴍʏ ɴᴀᴍᴇ ɪs  {BOT_NAME}.
๏ ɪ'ᴍ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ ᴡɪᴛʜ sᴏᴍᴇ ᴜsᴇғᴜʟ ғᴇᴀᴛᴜʀᴇs.
๏ You can choose an option below,ʏᴏᴜ ᴄᴀɴ ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴘᴛɪᴏɴ ʙᴇʟᴏᴡ ʙʏ ᴄʟɪᴄᴋɪɴɢ ᴀ ʙᴜᴛᴛᴏɴ. 
๏ ᴀʟsᴏ ʏᴏᴜ ᴄᴀɴ ᴀsᴋ ᴇᴠᴇʀʏᴛʜɪɴɢ ɪɴ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ.

ɢᴇɴᴇʀᴀʟ ᴄᴏᴍᴍᴀɴᴅ  ʜᴇʀᴇ:
 ๏ /start: sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ
 ๏ /help: ɢɪᴠᴇ ᴛʜɪs ᴍᴇssᴀɢᴇ
 """
    if mod_match:
        module = mod_match.group(1)
        text = (
            "{} **{}**:\n".format(
                "Here is the help for", HELPABLE[module].__MODULE__
            )
            + HELPABLE[module].__HELP__
        )

        await query.message.edit(
            text=text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("back", callback_data="help_back")]]
            ),
            disable_web_page_preview=True,
        )
    elif home_match:
        await app.send_message(
            query.from_user.id,
            text=home_text_pm,
            reply_markup=home_keyboard_pm,
        )
        await query.message.delete()
    elif prev_match:
        curr_page = int(prev_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(curr_page - 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif next_match:
        next_page = int(next_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(next_page + 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif back_match:
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif create_match:
        text, keyboard = await help_parser(query)
        await query.message.edit(
            text=text,
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )

    return await client.answer_callback_query(query.id)


if __name__ == "__main__":
    install()
    with closing(loop):
        with suppress(asyncio.exceptions.CancelledError):
            loop.run_until_complete(start_bot())
        loop.run_until_complete(asyncio.sleep(3.0))  # task cancel wait
