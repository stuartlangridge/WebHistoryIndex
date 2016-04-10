var t = document.querySelector("title"), title = location.href;
if (t && t.textContent) { title = t.textContent; }
var send = {
    url: location.href,
    title: title,
    content: document.documentElement.outerHTML
};
var x = new XMLHttpRequest();
x.open("POST", "https://localhost:5150/add", true);
x.setRequestHeader("Content-Type", "application/json");
x.send(JSON.stringify(send));