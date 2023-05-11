let data = [{
    values:[1,1,1],
    labels:['Negative','Neutral','Positive'],
    type:'pie'
}];

let layout = {
    height:500,
    width:500
};

$(function(){
    // setInterval(readData,5000);
    readData();
});

function readData(){
    //Read data
    let url = "https://yakitateenglish.azurewebsites.net/reviews";
    $.getJSON(url)
     .done(function(msg){
        console.log(msg);
        data[0].values[0] = 0;
        data[0].values[1] = 0;
        data[0].values[2] = 0;
        let sentiments = ['negative','neutral','positive'];
        for(let x=0; x<msg.length;x++){
            for(let y=0;y<sentiments.length;y++){
                if(msg[x].sentiment == sentiments[y]){
                    data[0].values[y] += 1;
                }
            }
        }
         Plotly.newPlot("myDiv", data, layout);
     })
     .fail(function(msg){console.log("Fail");});
}