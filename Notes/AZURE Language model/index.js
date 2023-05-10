'use strict';
const line = require('@line/bot-sdk'),
      express = require('express'),
      configGet = require('config');//({
//        path: '/Users/anderson/Desktop/Data Science/config/default.json' //指定檔案的絕對路徑
//      });
const {TextAnalyticsClient, AzureKeyCredential} = require("@azure/ai-text-analytics");

//Line config
const configLine = {
  channelAccessToken:configGet.get("CHANNEL_ACCESS_TOKEN"),
  channelSecret:configGet.get("CHANNEL_SECRET")
};

//Azure Text Sentiment
const endpoint = configGet.get("ENDPOINT");
const apiKey = configGet.get("TEXT_ANALYTICS_API_KEY");

const client = new line.Client(configLine);
const app = express();

const port = process.env.PORT || process.env.port || 3001;

app.listen(port, ()=>{
  console.log(`listening on ${port}`);
   
});

async function MS_TextSentimentAnalysis(thisEvent){
    console.log("[MS_TextSentimentAnalysis] in");
    const analyticsClient = new TextAnalyticsClient(endpoint, new AzureKeyCredential(apiKey));
    let documents = [];
    documents.push(thisEvent.message.text);
    // documents.push("我覺得櫃檯人員很親切");
    // documents.push("熱水都不熱，爛死了，很生氣！");
    // documents.push("房間陳設一般般");
    //const results = await analyticsClient.analyzeSentiment(documents);
    const results = await analyticsClient.analyzeSentiment(documents,"zh-Hant",{
      includeOpinionMining: true
    });
    //const results = await analyticsClient.AnalyzeSentimentOptions(documents);
    console.log("[results] ", JSON.stringify(results));
    

    //回傳內容改變
    const score = results[0].confidenceScores;
    const state = results[0].sentiment;

    const echo1 = {
      type: 'text',
      text: `謝謝你提供了一個 ${state === 'neutral' ? '中性' : state === 'positive' ? '正向' : state === 'negative' ? '負面':''} 
      的回饋意見，正向指數 ${score["positive"]}`
    };
    const echo2 = {
      type: 'text',
      text: `謝謝你提供了一個 ${state === 'neutral' ? '中性' : state === 'positive' ? '正向' : state === 'negative' ? '負面':''} 
      的回饋意見，正向指數 ${score["positive"]}`
    };
    return client.replyMessage(thisEvent.replyToken, [echo1,echo2]);


}

app.post('/callback', line.middleware(configLine),(req, res)=>{
  Promise
    .all(req.body.events.map(handleEvent))
    .then((result)=>res.json(result))
    .catch((err)=>{
      console.error(err);
      res.status(500).end();
    });
});

function handleEvent(event){
  if(event.type !== 'message' || event.message.type !== 'text'){
    return Promise.resolve(null);
  }

  MS_TextSentimentAnalysis(event)
    .catch((err) => {
      console.error("Error:", err);
    }); 
}
