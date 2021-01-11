from emoji import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

button0 = emojize(':hot_beverage:', use_aliases=True)
button1 = emojize(':keycap_1:', use_aliases=True)
button2 = emojize(':keycap_2:', use_aliases=True)
button3 = emojize(':keycap_3:', use_aliases=True)
button4 = emojize(':keycap_5:', use_aliases=True)
button5 = emojize(':keycap_8:', use_aliases=True)
button6 = emojize('End voting', use_aliases=True)

rotating_light = emojize(':rotating_light:', use_aliases=True)

keyboard = [
    [InlineKeyboardButton(button0, callback_data='0.5')],
    [InlineKeyboardButton(button1, callback_data='1')],
    [InlineKeyboardButton(button2, callback_data='2')],
    [InlineKeyboardButton(button3, callback_data='3')],
    [InlineKeyboardButton(button4, callback_data='5')],
    [InlineKeyboardButton(button5, callback_data='8')],
    [InlineKeyboardButton(button6, callback_data='End voting')],
]

rating_keyboard = InlineKeyboardMarkup(keyboard)

icons = [
    emojize(':comet:', use_aliases=True),
    emojize(':fire:', use_aliases=True),
    emojize(':firecracker:', use_aliases=True),
    emojize(':sparkles:', use_aliases=True),
    emojize(':party_popper:', use_aliases=True),
    emojize(':confetti_ball:', use_aliases=True),
    emojize(':military_medal:', use_aliases=True),
    emojize(':heart:', use_aliases=True),
    emojize(':purple_heart:', use_aliases=True),
    emojize(':purple_heart:', use_aliases=True),
    emojize(':black_heart:', use_aliases=True),
    emojize(':two_hearts:', use_aliases=True),
    emojize(':space_invader:', use_aliases=True),
    emojize(':hankey:', use_aliases=True),
    emojize(':robot:', use_aliases=True),
    emojize(':alien:', use_aliases=True),
    emojize(':unicorn_face:', use_aliases=True),
    emojize(':crab:', use_aliases=True),
    emojize(':boom:', use_aliases=True),
    emojize(':rainbow:', use_aliases=True),
    emojize(':rainbow_flag:', use_aliases=True),
    emojize(':lollipop:', use_aliases=True),
    emojize(':beer:', use_aliases=True),
    emojize(':beers:', use_aliases=True),
    emojize(':doughnut:', use_aliases=True),
    emojize(':cookie:', use_aliases=True),
    emojize(':8ball:', use_aliases=True),
    emojize(':trumpet:', use_aliases=True),
    emojize(':trumpet:', use_aliases=True),
    emojize(':guitar:', use_aliases=True),
    emojize(':game_die:', use_aliases=True),
    emojize(':dart:', use_aliases=True),
    emojize(':video_game:', use_aliases=True),
    emojize(':gem:', use_aliases=True),
    emojize(':moneybag:', use_aliases=True),
    emojize(':gun:', use_aliases=True),
    emojize(':bomb:', use_aliases=True),
    emojize(':balloon:', use_aliases=True),
    emojize(':zzz:', use_aliases=True),
    emojize(':mega:', use_aliases=True),
    emojize(':loudspeaker:', use_aliases=True),
]
