// runs in extension context; receives page metadata from grabPage and sends it to the server

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    var x = new XMLHttpRequest();
    x.open("POST", "http://localhost:5150/add", true);
    x.setRequestHeader("Content-Type", "application/json");
    x.send(JSON.stringify(request));
    console.log("request sent");
});

