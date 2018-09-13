var ws = require("nodejs-websocket");
console.log("开始建立连接...")
 
var html = null,game2 = null , game1Ready = false , game2Ready = false;
var server = ws.createServer(function(conn){
    conn.on("text", function (str) {
        console.log("收到的信息为:"+str)
        if(str==="html"){
            html = conn;
            htmlReady = true;
            // conn.sendText("success");

            // setTimeout(function(){conn.sendText("success");},25000);

        }else {         
            html.sendText(str);
        }

      
 
        // conn.sendText(str)
    })
    conn.on("close", function (code, reason) {
        console.log("关闭连接")
    });
    conn.on("error", function (code, reason) {
        console.log("异常关闭")
    });
}).listen(9001)
console.log("WebSocket建立完毕")