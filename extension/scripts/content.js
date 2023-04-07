
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

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        let headerText = getHeaderText()
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
