#coding:utf-8

from random import randint
import time
import json
import re
import unicodedata
import logging

logging.basicConfig(level=logging.DEBUG,format="[%(asctime)s][%(levelname)s][%(thread)d][%(filename)s:%(lineno)d]%(message)s")

from googletrans import Translator
from telegram.ext import Updater,CommandHandler,MessageHandler,RegexHandler,Filters

config = {}
lastSent = 0
msgCount = 0

def reloadConfig():
	global config
	try:
		with open("config.json","r",encoding="utf-8") as f:
			config = json.loads(f.read())
			f.close()
		return True
	except:
		logging.exception("")
		return False

def checkRateLimit():
	global lastSent
	global msgCount
	try:
		nowTime = time.time()
	#	logging.debug("checkRateLimit")
		logging.debug((lastSent,msgCount))
		if (nowTime - lastSent >= config["rateLimit"]["time"]):
			lastSent = nowTime
			msgCount = 1
			return False
		elif (msgCount < config["rateLimit"]["maxMessages"]):
			msgCount += 1
			return False
		logging.info("Reached rate limit.%d messages in %.2f s" % (msgCount,nowTime - lastSent))
		return True
	except:
		logging.exception("")
		return True

def removeEmojis(text):
	return ''.join(c for c in unicodedata.normalize('NFC', text) if c <= '\uFFFF')

def translate(text="",dest="en"):
	trans = Translator()
	return trans.translate(text,dest).text

def logMessage(bot,update):
	try:
		logging.info(update)
	except:
		logging.exception("")

def translateReply(bot,update):
	try:
		if (checkRateLimit()):return
		dest = ""
		for item in config["commands"]:
	#		logging.debug(update.message.text[1:])
	#		logging.debug(item["command"])
			if (item["command"] == update.message.text[1:]):
				dest = item["destLang"]
				break
		if (dest == ""):return
	#	logging.debug(dest)
		chatId = update.message.chat_id
		replyToMessageId = update.message.message_id
		try:
			translateText = removeEmojis(update.message.reply_to_message.text)
		except:
			bot.send_message(chat_id=chatId,reply_to_message_id=replyToMessageId,text="You need reply a message!")
			return
		translatedText = translate(translateText,dest)
		bot.send_message(chat_id=chatId,reply_to_message_id=replyToMessageId,text=translatedText)
	except:
		logging.exception("")
		bot.send_message(chat_id=chatId,reply_to_message_id=replyToMessageId,text="Bot internal error,please contact administrators.")

def helpReply(bot,update):
	if (checkRateLimit()):return
	chatId = update.message.chat_id
	replyToMessageId = update.message.message_id
	helpInfo = ""
	for item in config["helpInfo"]:
		helpInfo += item
		helpInfo += "\n"
	helpInfo += "This group set %d messages in %.2f s" % (config["rateLimit"]["maxMessages"],config["rateLimit"]["time"])
	bot.send_message(chat_id=chatId,reply_to_message_id=replyToMessageId,text=helpInfo)
	
if (__name__ == "__main__"):
	reloadConfig()
	logging.info("Initlizating bot.")
	updater = Updater(token=config["token"])

	dispatcher = updater.dispatcher
	logHandler = MessageHandler(Filters.all,logMessage)
	helpHandler = CommandHandler("help",helpReply)
	translateReHandler = RegexHandler("^\/translate_to_",translateReply)

#	dispatcher.add_handler(logHandler)
	dispatcher.add_handler(helpHandler)
	dispatcher.add_handler(translateReHandler)

	logging.info("Starting bot with %d messages in %.2f s,%d commands." % (config["rateLimit"]["maxMessages"],config["rateLimit"]["time"],len(config["commands"])))
	updater.start_polling()
