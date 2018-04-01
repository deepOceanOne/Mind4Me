var Botkit = require('botkit');
var os = require('os');

//將.env中的設定值，寫到 process.env 之中 
require('dotenv').config();

//新增 slack 耳朵來聽訊息
var slackEars = Botkit.slackbot({
    debug:true,
    //將資料存在 json 檔之中
    json_file_store: 'slackDataStore',
});

//開始接上 slack RTM (Real Time Messaging)
var slackBot = slackEars.spawn({
        token:process.env.SLACK_BOT_TOKEN
}).startRTM();

//聽到 hello 
slackEars.hears('hello','direct_message,direct_mention',function(bot,message) {  
    //回覆給使用者
    bot.reply(message,"您好! 我是 小亂 ^_^");
});
