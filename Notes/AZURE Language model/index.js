'use strict';
const line = require('@line/bot-sdk'),
      express = require('express'),
      axios = require('axios'),
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
    //save to Json Server
    let newData = {
      "sentiment":results[0].sentiment,
      "confidenceScore":results[0].confidenceScores[results[0].sentiment],
      "opinionText":""
    };

    if (results[0].sentences[0].opinions.length!=0){
      newData.opinionText = results[0].sentences[0].opinions[0].target.text;
    }
    let axios_add_data = {
      method:"post",
      url:"https://yakitateenglish.azurewebsites.net/reviews",
      headers:{
        "content-type":"application/json"
      },
      data:newData
    };

    axios(axios_add_data)
    .then(function(response){
      console.log(JSON.stringify(response.data));
    })
    .catch(function(){console.log("error");});


    //回傳內容改變
    const state = results[0].sentiment;
    const score = results[0].confidenceScores[results[0].sentiment];
    const object = newData.opinionText;

    let object_adj = "";
    if (object === ""){
      object_adj = "相關"
    } else {
      object_adj = object
    }
    
    let feedbackType = '';
    let feedback = '';
    if (state === 'neutral') {
      feedbackType = '中性',
      feedback = "進行了解。";
    } else if (state === 'positive') {
      feedbackType = '正向',
      feedback = "向您致上誠摯的感謝。";
    } else if (state === 'negative') {
      feedbackType = '負面',
      feedback = "立刻進行改善，並向您致上誠摯的歉意。";
    }



    const echo1 = {
      type: 'text',
      text: state
    };
    const echo2 = {
      type: 'text',
      text: `謝謝你提供了一個 ${feedbackType} 的回饋意見，${feedbackType}指數 ${score}`
    };
    const echo3 = {
      type: 'text',
      text: `謝謝你提供了一個關於 ${object} 的 ${feedbackType} 回饋意見，${feedbackType}指數 ${score}。我們會盡快請 ${object_adj} 的負責單位 ${feedback}`
    };
    return client.replyMessage(thisEvent.replyToken, [echo1,echo2,echo3]);


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
