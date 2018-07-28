import emoji
import telegram
import telegram.ext
from settings import TELEGRAM_TOKEN


class JenkinsTelegramBot(object):
    updater = None
    dispatcher = None

    def __init__(self):
        self.updater = telegram.ext.Updater(token=TELEGRAM_TOKEN)
        self.dispatcher = self.updater.dispatcher

        self.create_handlers()

    def start_bot(self):
        self.updater.start_polling()

    def stop_bot(self):
        self.updater.stop()

    def create_handlers(self):
        start_handler = telegram.ext.CommandHandler(
            'start', JenkinsTelegramBot.start)
        self.dispatcher.add_handler(start_handler)

        about_handler = telegram.ext.CallbackQueryHandler(
            JenkinsTelegramBot.about, pattern='about')
        self.dispatcher.add_handler(about_handler)

        add_server = telegram.ext.CallbackQueryHandler(
            JenkinsTelegramBot.add_server, pattern='add_server')
        self.dispatcher.add_handler(add_server)

        unknown_handler = telegram.ext.MessageHandler(
            telegram.ext.Filters.text, JenkinsTelegramBot.unknown)
        self.dispatcher.add_handler(unknown_handler)        

    @staticmethod
    def start(bot, update):
        username = "%s %s" % (
            update.message.from_user.first_name, update.message.from_user.last_name)
        keyboard = [[telegram.InlineKeyboardButton('Cadastrar um Servidor', callback_data='about')],
                    [telegram.InlineKeyboardButton('Saber no que posso lhe ajudar', callback_data='add_server')]]
        reply_markup=telegram.ReplyKeyboardMarkup(keyboard)

        bot.send_message(chat_id=update.message.chat_id,
                         text="Olá %s.  Reparei que nós nunca nos conhecemos antes... O que deseja fazer?" % username,
                         reply_markup=reply_markup)

    @staticmethod
    def about(bot, update):
        first_name=update.message.from_user.first_name
        bot.send_message(chat_id=update.message.chat_id,
                         text=emoji.emojize(("Bom %s, eu lhe ajudar com algumas tarefas simples no jenkins no momento."
                              " Por exemplo, eu posso iniciar uma nova build de um jogo para você, listar os"
                              " jobs que você criou em seu servidor, como também mostrar os seus status e mais"
                              " algumas informações diversas. Mas para isso preciso que você cadastre um servidor"
                              " junto a mim. Se quiser iniciar basta mandar um /start :simple_smile:") % first_name),
                         reply_markup=telegram.ReplyKeyboardRemove)

    @staticmethod
    def add_server(bot, update):
        first_name=update.message.from_user.first_name
        bot.send_message(chat_id=update.message.chat_id,
                         text=emoji.emojize(("Então... Essa função não está implementada no momento :bowtie:, eu sei que um"
                              " bot mentiroso não vale de nada, mas prometo que isso será resolvido logo. Para que isto não seja"
                              " em vão, que tal um chá? :tea:") % first_name),
                         reply_markup=telegram.ReplyKeyboardMarkup)

    @staticmethod
    def unknown(bot, update):
        keyboard=[['/start']]
        reply_markup=telegram.ReplyKeyboardMarkup(keyboard)
        bot.send_message(chat_id=update.message.chat_id,
                         text=("Olá eu sou um bot com o intuito de lhe ajudar em tarefas com o Jenkins."
                               " Para inciar aperte em start."),
                         reply_markup=reply_markup)
