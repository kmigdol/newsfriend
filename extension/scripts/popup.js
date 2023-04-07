
console.log("YES LOADED POPUP");

const lambdaUrl = "https://o45bmhjq3ww4s72qfz7n2drnqa0vwsjh.lambda-url.us-east-2.on.aws/"

const button = document.getElementById("news-button");
const buttonWrapper = document.getElementById("button-wrapper");

recievedHeader = false;

button.addEventListener('click', () => {
    console.log("CLICKED");

    chrome.tabs.query({active: true, currentWindow: true}, 
        function(tabs) {
            console.log("SENDING MESSAGE");
            chrome.tabs.sendMessage(tabs[0].id, {type: "getHeader"})
        }
    )
});

const listContainer = document.getElementById("article-list");

function fillInArticles(articles) {
    console.log(articles);
    listNode = document.createElement("ul");
    for (let i = 0; i < articles.length; i++) {
        article = articles[i];
        text = document.createTextNode(article.title);
        a = document.createElement("a");
        a.appendChild(text);
        a.href = article.url;
        entry = document.createElement('li');
        entry.appendChild(a);
        listNode.appendChild(entry);
    }
    listContainer.appendChild(listNode);
}

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        console.log("RECIEVED MESSAGE");
        console.log(request);

        if (request.type == "sendHeader") {
            console.log(request.header);
            headerNode = document.createTextNode(request.header);
            
            if (!recievedHeader) {
                buttonWrapper.insertBefore(headerNode, button);
            }

            fetch(lambdaUrl, {
                method: "POST",
                body: JSON.stringify({
                    "title": request.header
                }),
                headers: {
                    "Content-Type": "application/json; charset=UTF-8",
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST'
                }
            }).then((response) => response.json())
              .then((json) => fillInArticles(json));

            recievedHeader = true;
        }
    }
);

window.addEventListener('click',function(e){
    if(e.target.href!==undefined){
      chrome.tabs.create({url:e.target.href, active:false})
    }
  })

