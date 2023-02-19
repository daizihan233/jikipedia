const CryptoJS = require("crypto-js");


const CLIENT = "app"
const VERSION = "2.20.39"
const XID_SECRET = ""
let http = require('http')
const url = require("url");
function gen_xid() {
    let e;
    e = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (function (t) {
            let e = 16 * Math.random() | 0;
            return ("x" === t ? e : 3 & e | 8).toString(16)
        }
    ))
    return e;
}
function gen_iv(e) {
    return CryptoJS.lib.WordArray.random(e);
}
function gen_content(content) {
    return "jikipedia_xid_" + content || gen_xid();
}
function gen_key() {
    return CryptoJS.SHA256(CLIENT + "_" + VERSION + "_" + XID_SECRET);
}
function gen_n(content) {
    return CryptoJS.AES.encrypt(content || gen_content(content), gen_key(), {
        iv: gen_iv(16),
        padding: CryptoJS.pad.Pkcs7,
        mode: CryptoJS.mode.CBC
    })
}
//调用http的createServer方法 创建一个服务器实例
const server = http.createServer();
server.listen(3000, "0.0.0.0", () => console.log('启动了'));

// 只要有浏览器发来请求，就会触发下面的事件
server.on('request', (req, res) => {
    let str = '';
    req.on('data', (chunk) => {
        str += chunk; // 把接收到的一块数据拼接到str中
    });
    let data;
    let urlObj = url.parse(req.url ,true);
    let query = urlObj.query;
    req.on('end', () => {
        if (req.url.startsWith("/jiki/encrypt/xid")) {
            let t = gen_key();
            let content = gen_content(query.xid);
            let n = gen_n(content);
            let c = t.concat(n.ciphertext);
            data = CryptoJS.enc.Base64.stringify(c);
            console.debug(data)
            res.end(
                JSON.stringify(
                    {
                        status: 200,
                        msg: "OK!",
                        encode_xid: data
                    }
                )
            )
        } else {
            req.statusCode = 404
            res.end(
                JSON.stringify(
                    {
                        status: 404,
                        msg: "找不到此 API ！"
                    }
                )
            )
        }
    });

});
