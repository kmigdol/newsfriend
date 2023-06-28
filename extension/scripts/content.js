
console.log("YES LOADED CONTENT");


function getHeader() {
    if (location.host == "www.cnn.com") {
        return document.getElementById("maincontent")
    } else if (location.host == "www.nytimes.com") {
        return document.getElementsByClassName("ehdk2mb0")[0]
    }
}


async function getHeaderText() {
    // const header = getHeader();
    // const headerText = header.textContent;

    let [tab] = await chrome.tabs.query({ active: true, lastFocusedWindow: true });
    let headerText = tab.title

    return headerText
}

function getBodyText() {
    const body = document.body
    return body.innerText
}

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        console.log("REQUEST");
        console.log(request);

        if (request.type == "getHeader") {
            let headerText = getHeaderText()
            console.log("HEADER TEXT");
            console.log(headerText);
            console.log("SENDING HEADER");

            chrome.runtime.sendMessage({
                header: headerText.trim(),
                type: "sendHeader"
            });
        }

        if (request.type == "getText") {
            let bodyText = getBodyText();
            console.log("BODY TEXT");
            console.log(bodyText);
            console.log("SENDING BODY TEXT");
            chrome.runtime.sendMessage({
                text: bodyText,
                type: "sendText"
            })
        }
    }
)
