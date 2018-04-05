

  "每一个关键词背后，都有一群不同的人"

主要思路：
    通过词汇入口出口api、综合搜索api、提醒功能和推荐功能实现Mind系统

基本架构
    GET\PUT\QUERY\RECOM\REMIND\INFO  六个基本操作，实现数据规范化读取和存储

    其中，提醒功能单独实现：

        综合提醒 -- 
            ------ todaypro 专用条目提醒   bomb后端专用api
            ------ slack  channel提醒
            ------ 微信酱 提醒
            ------ 自建 RSS 提醒 
                        -------- Hexo 网站搭建 RSS推送插件 
                                            --------------- http://www.dongwm.com/archives/slackshang-de-xiao-huang-ji-slackbot/

         搜索功能单独实现：

        综合搜索 --  （pk baidu plan）
            ------ alpha  搜索远程记录分析提取
            ------ elastic 系统化搜索
            ------ 语音搜索界面  -- rss界面模仿技术探索，在线语音采集分析系统
                         -------- 复杂环境\远场声音提取  （百度）


         信息系统单独实现：

            根据语音识别的具体需求、关键词构建人的行为模型、人的世界模型和基本需求链

         RECOM系统单独实现：
            
            兴趣标签系统 
                ---------基于词汇
                            -------以电视频道节目单为例



基本数据示例：

种子词汇：
    好点子是从哪里来的？
    赚钱的动力
    逛收纳盒
    袜子收纳 
    github资源下载速度慢
    道西战争
    dns
    docker
    塘沽大爆炸
    电动自行车养护和维修 
    展览
    youtube推荐
      医生  神奇药
    许子东
    s  书籍  拍摄分享网
    不承担任何责任
    电话口语 
    电话套路
    语音输入组件
    alternatives  
    替代品
    互联网安全


人工智能机器人问答列表：
    找滴滴
    注册码寻找途径
    天气

问答列表：
    xxxxxx  --  xxxxxx

书  关键词库 ：
    礼物
    小家伙
    晚上
    喘息
    情急之下
    圣诞节
    情人节
    元旦
    食堂
    搞好关系

alpha 搜索人物引擎   人物列表：
    papi酱
    张巍（清澄君）
    民间股神  林园
    张轶  51社保

today + 专用条目：
    xxxxxx