
console.log("YES LOADED CONTENT");

const header = document.getElementById("maincontent");
headerText = header.textContent;

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        console.log("HEADER TEXT");
        console.log(headerText);
        console.log("REQUEST");
        console.log(request);

        if (request.type == "getHeader") {
            console.log("SENDING HEADER");
            chrome.runtime.sendMessage({
                header: headerText.trim(),
                type: "sendHeader"
            });
        }
    }
)
