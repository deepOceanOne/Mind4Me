var Botkit = require('botkit');
var os = require('os');

//將.env中的設定值，寫到 process.env 之中 
require('dotenv').config();

// for DingDing function
// by jxc 20180603
const ChatBot = require('dingtalk-robot-sender');
const robot = new ChatBot({
  webhook: 'https://oapi.dingtalk.com/robot/send?access_token=123ca88c4607e7b4a484ad83ad55a67434cd84325c044ad1fd9afc7761064167'
});
// end of DingDing function


//新增 slack 耳朵來聽訊息
var slackEars = Botkit.slackbot({
    debug:true,
    //將資料存在 json 檔之中
    json_file_store: 'slackDataStore',
});

//開始接上 slack RTM (Real Time Messaging)
var slackBot = slackEars.spawn({
      //  token:process.env.SLACK_BOT_TOKEN
      token:'xoxb-336339618310-fYG6j2YzFfG9paBQhLn9GX8Q'
}).startRTM();

//聽到 hello 
slackEars.hears('hello','direct_message,direct_mention',function(bot,message) {  
    //回覆給使用者
    bot.reply(message,"您好! 我是 小亂 ^_^");
});
// 听到链接
slackEars.hears('http(.*)','direct_message,direct_mention',function(bot,message) {  
    // 回覆給使用者
    // bot.reply(message,"您好! 我是 小亂 ^_^");
    
    var link = {
      "text":"放入一些推荐的内容",
      "title": "放入一些推荐的标题",
      "picUrl": "放入一些推荐的图片",
	  "messageUrl": message.text
	};
    robot.link(link);
    
    // robot.text(message.text)
});
// 链接里还可以进行以下细分

// 听到 “查找。。。”
slackEars.hears('查找(.*)','direct_message,direct_mention',function(bot,message) {  
    // 回覆給使用者
    // bot.reply(message,"您好! 我是 小亂 ^_^");
    robot.text(message);
});

// 听到图片
slackEars.hears('(.*)jpg','direct_message,direct_mention',function(bot,message) {  
    // 回覆給使用者
    var title = "可以填充的推荐标题";
    var pic_text = "![推荐的新闻标题]("+message.text+")";
    robot.markdown(title,ic_text);
});


// 进行随机的推送，使用actionCard
var  card = {
  "title": "乔布斯 20 年前想打造一间苹果咖啡厅，而它正是 Apple Store 的前身",
  "text": `![screenshot](@lADOpwk3K80C0M0FoA) 
                ### 乔布斯 20 年前想打造的苹果咖啡厅 
                Apple Store 的设计正从原来满满的科技感走向生活化，而其生活化的走向其实可以追溯到 20 年前苹果一个建立咖啡馆的计划`,
  "hideAvatar": "0",
  "btnOrientation": "0",
  "btns": [
    {
      "title": "内容不错",
      "actionURL": "https://www.dingtalk.com/"
    },
    {
      "title": "不感兴趣",
      "actionURL": "https://www.dingtalk.com/"
    }
  ]
};
// robot.actionCard(card);
// end of 随机推送



// for DingDing function
// by jxc 20180603
// var message="我就是我, 是不一样的烟火";
// robot.text(message);
// end of DingDing function