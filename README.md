# TGTranslateBot
Telegram Google Translate Bot 

## Requirements

 - Python >= 3.6
 - python-telegram-bot
 - googletrans


## Getting started

    pip install -r requirements.txt
    or
    pip3 install -r requirements.txt
    
    rename config.json.example to config.json.
    fill token area in config.json with your telegram bot token.
    start your bot.

## Profile Interpretation
Supported languages in [here](https://py-googletrans.readthedocs.io/en/latest/#googletrans-languages)

    {
    	"token":"",	//Your telegram bot token
    	"rateLimit":{	//Anti flood
    		"time":3,	//In second
    		"maxMessages":5	//Maximum number of messages allowed in a limited time
    	},
    	"commands":[	//The command must start with "translate_to_"
    		{
    			"command":"translate_to_en",
    			"destLang":"en"//Destnation language
    		},
    		{
    			"command":"translate_to_zh",
    			"destLang":"zh-CN"
    		},
    		{
    			"command":"translate_to_ja",
    			"destLang":"ja"
    		}
    	],
    	"helpInfo":[	//Help information will be automatically stitched
    		"Please use the reply method to use the bot.",
    		"/translate_to_en - Translate message to english.",
    		"/translate_to_zh - Translate message to chinese.",
    		"/translate_to_ja - Translate message to japanese."
    	]
    }
