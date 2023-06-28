
console.log("YES LOADED POPUP");

const lambdaUrl = "https://o45bmhjq3ww4s72qfz7n2drnqa0vwsjh.lambda-url.us-east-2.on.aws/"

const articlesButton = document.getElementById("article-button");
const summaryButton = document.getElementById("summary-button");
const buttonWrapper = document.getElementById("button-wrapper");

recievedHeader = false;

tabTitle = "";

chrome.tabs.query({ active: true, lastFocusedWindow: true },
    function(tabs) {
        console.log(tabs)
        console.log(tabs[0])
        tabTitle = tabs[0].title
        console.log(tabTitle)
        headerNode = document.createTextNode(tabTitle);

        if (!recievedHeader) {
            buttonWrapper.insertBefore(headerNode, button);
        }
        recievedHeader = true;
    }
)

function getArticles(articleTitle) {
    console.log(articleTitle);

    fetch(lambdaUrl, {
        method: "POST",
        body: JSON.stringify({
            "title": articleTitle
        }),
        headers: {
            "Content-Type": "application/json; charset=UTF-8",
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST'
        }
    }).then((response) => response.json())
        .then((json) => fillInArticles(json));

}

async function getTitle() {
    let [tab] = await chrome.tabs.query({ active: true, lastFocusedWindow: true });
    let headerText = await tab.title

    return headerText
}

articlesButton.addEventListener('click', function() {
    console.log("CLICKED");
    getArticles(tabTitle)
});

summaryButton.addEventListener('click', function() {
    console.log("CLICKED SUMMARY");
    chrome.tabs.sendMessage(tabs[0].id, {type: "getText"}, function(response) {
        console.log("RECIEVED RESPONSE");
        console.log(response);
    })
})

const listContainer = document.getElementById("article-list");

function getArticleEntry(article) {
    text = document.createTextNode(article.title);
    title = document.createElement("a");
    title.appendChild(text);
    title.href = article.url;

    linebreak = document.createElement("br");

    website = new URL(article.url);
    domain = website.hostname;
    domain = domain.replace('www.','');
    domainNode = document.createTextNode(domain);

    entry = document.createElement('li');
    entry.appendChild(title);
    entry.appendChild(linebreak);
    entry.appendChild(domainNode);
    return entry
}

function fillInArticles(articles) {
    console.log(articles);
    listNode = document.createElement("ul");
    for (let i = 0; i < articles.length; i++) {
        article = articles[i];
        entry = getArticleEntry(article);
        listNode.appendChild(entry);
    }
    listContainer.appendChild(listNode);
}

function getSummary(text) {
    console.log(text)
}

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        console.log("RECIEVED MESSAGE")
        console.log(request)

        if (request.type == "sendText") {
            getSummary(request.text)
        }
    }
)

window.addEventListener('click',function(e){
    if(e.target.href!==undefined){
      chrome.tabs.create({url:e.target.href, active:false})
    }
  })

