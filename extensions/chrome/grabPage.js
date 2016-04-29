/* Runs in browser context; grabs the page title, url, HTML and sends it to sendPage */
var t = document.querySelector("title"), title = location.href;
if (t && t.textContent) { title = t.textContent; }
chrome.runtime.sendMessage({
    url: location.href,
    title: title,
    content: document.documentElement.outerHTML
}, function(response) {});
