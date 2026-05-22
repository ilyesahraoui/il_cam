from flask import Flask, request, jsonify, render_template_string
from groq import Groq

app = Flask(__name__)

# ضع API هنا
client = Groq(
    api_key="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"
)

messages = [
    {
        "role": "system",
        "content": """
        اسمك BMO.
        أنت ذكاء اصطناعي احترافي.
        تتكلم بالعربية.
        عندما تعطي كود اجعله مرتب داخل markdown.
        تم صنعك من طرف إلياس.
        لا تكرر التحية في كل رسالة.
        """
    }
]

HTML = """

<!DOCTYPE html>
<html lang="ar">
<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>BMO AI</title>

<style>

*{
margin:0;
padding:0;
box-sizing:border-box;
font-family:Arial;
}

body{
background:#0f172a;
color:white;
height:100vh;
display:flex;
flex-direction:column;
}

.top{
padding:20px;
background:#111827;
font-size:30px;
font-weight:bold;
border-bottom:1px solid #1e293b;
}

.messages{
flex:1;
overflow-y:auto;
padding:25px;
display:flex;
flex-direction:column;
gap:20px;
}

.user{
align-self:flex-end;
background:#2563eb;
padding:15px;
border-radius:18px;
max-width:80%;
line-height:1.7;
}

.bot{
background:#111827;
padding:20px;
border-radius:20px;
line-height:1.9;
border:1px solid #1e293b;
max-width:100%;
}

.bottom{
display:flex;
padding:20px;
gap:10px;
background:#111827;
border-top:1px solid #1e293b;
}

input{
flex:1;
padding:18px;
background:#1e293b;
border:none;
outline:none;
border-radius:15px;
color:white;
font-size:16px;
}

button{
padding:18px 25px;
background:#2563eb;
border:none;
border-radius:15px;
color:white;
cursor:pointer;
font-size:16px;
}

pre{
background:#020617;
padding:18px;
border-radius:15px;
overflow-x:auto;
margin-top:15px;
border:1px solid #334155;
}

code{
color:#38bdf8;
font-family:Consolas;
white-space:pre-wrap;
}

.typing{
color:#94a3b8;
font-size:15px;
}

@media(max-width:700px){

.top{
font-size:24px;
}

.user{
max-width:95%;
}

.bot{
padding:15px;
}

input{
font-size:15px;
}

button{
padding:15px;
}

}

</style>

</head>

<body>

<div class="top">
BMO AI
</div>

<div class="messages" id="messages">

<div class="bot">
سلام، أنا BMO 👋
</div>

</div>

<div class="bottom">

<input id="text" placeholder="اكتب رسالتك هنا...">

<button onclick="sendMessage()">
إرسال
</button>

</div>

<script>

let input = document.getElementById("text")

input.addEventListener("keypress", function(e){

if(e.key === "Enter"){
sendMessage()
}

})

function formatMessage(text){

text = text.replace(/```([\\s\\S]*?)```/g, function(match, code){

return `
<pre>
<code>${escapeHtml(code)}</code>
</pre>
`

})

text = text.replace(/\\n/g,"<br>")

return text
}

function escapeHtml(text){

return text
.replace(/&/g, "&amp;")
.replace(/</g, "&lt;")
.replace(/>/g, "&gt;")
}

async function sendMessage(){

let text = input.value.trim()

if(text === "") return

let messages = document.getElementById("messages")

messages.innerHTML += `
<div class="user">
${text}
</div>
`

input.value = ""

messages.innerHTML += `
<div class="typing" id="typing">
BMO يكتب...
</div>
`

messages.scrollTop = messages.scrollHeight

try{

let response = await fetch("/chat",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
message:text
})
})

let data = await response.json()

document.getElementById("typing").remove()

messages.innerHTML += `
<div class="bot">
${formatMessage(data.reply)}
</div>
`

messages.scrollTop = messages.scrollHeight

}catch(error){

document.getElementById("typing").remove()

messages.innerHTML += `
<div class="bot">
حدث خطأ في الاتصال بالذكاء الاصطناعي.
</div>
`

}

}

</script>

</body>
</html>

"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():

    try:

        user_message = request.json["message"]

        messages.append({
            "role":"user",
            "content":user_message
        })

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )

        reply = response.choices[0].message.content

        messages.append({
            "role":"assistant",
            "content":reply
        })

        return jsonify({
            "reply":reply
        })

    except Exception as e:

        return jsonify({
            "reply":str(e)
        })

app.run(host="0.0.0.0", port=5000, debug=True)