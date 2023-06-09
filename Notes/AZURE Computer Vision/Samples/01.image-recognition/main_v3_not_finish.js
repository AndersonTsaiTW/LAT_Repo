$(document).ready(function(){
    //do something
    $("#thisButton").click(function(){
        processImage();
        var keyword = $("#inputKeyword").val();
        searchWikipedia(keyword);
    });
    $("#inputImageFile").change(function(e){
        processImageFile(e.target.files[0]);
    });
});

function searchWikipedia(keyword) {
    var apiUrl = "https://en.wikipedia.org/w/api.php";
    var params = {
        action: "query",
        list: "search",
        srsearch: keyword,
        format: "json"
    };

    // 發送搜尋請求
    $.ajax({
        url: apiUrl,
        dataType: "jsonp",
        data: params,
        success: function(data) {
            displaySearchResults(data.query.search);
        },
        error: function(xhr, status, error) {
            console.log(error);
        }
    });
}


function processImageFile(imageObject) {

    //確認區域與所選擇的相同或使用客製化端點網址
    var url = "https://eastus.api.cognitive.microsoft.com/";
    var uriBase = url + "vision/v2.1/analyze";

    var params = {
        "visualFeatures": "Adult,Brands,Categories,Color,Description,Faces,ImageType,Objects,Tags",
        "details": "Landmarks",
        //"maxCandidates": "10",
        "language": "en",
    };
    //顯示分析的圖片
    // var sourceImageUrl = document.getElementById("inputImage").value;
    //下面這個做法可以製造出圖片網址
    var sourceImageUrl = URL.createObjectURL(imageObject);
    document.querySelector("#sourceImage").src = sourceImageUrl;
    //送出分析
    $.ajax({
        url: uriBase + "?" + $.param(params),
        // Request header
        beforeSend: function (xhrObj) {
            xhrObj.setRequestHeader("Content-Type", "application/octet-stream");
            xhrObj.setRequestHeader("Ocp-Apim-Subscription-Key", subscriptionKey);
        },
        //直接送圖片，要關成false
        type: "POST",
        processData:false,
        contentType:false,
        // Request body
        data: imageObject
    })
        .done(function (data) {
            //顯示JSON內容
            $("#responseTextArea").val(JSON.stringify(data, null, 2));
            $("#picDescription").empty();
            $("#picDescription").append("https://en.wikipedia.org/wiki/"+data.categories[0].detail.landmarks.name);
            //for (var x = 0; x < data.description.captions.length; x++) {
            //    $("#picDescription").append(data.description.captions[x].text + "<br>");
            //}
            // $("#picDescription").append("這裡有"+data.faces.length+"個人");
        })
        .fail(function (jqXHR, textStatus, errorThrown) {
            //丟出錯誤訊息
            var errorString = (errorThrown === "") ? "Error. " : errorThrown + " (" + jqXHR.status + "): ";
            errorString += (jqXHR.responseText === "") ? "" : jQuery.parseJSON(jqXHR.responseText).message;
            alert(errorString);
        });
};


function processImage() {
    
    //確認區域與所選擇的相同或使用客製化端點網址
    var url = "https://eastus.api.cognitive.microsoft.com/";
    var uriBase = url + "vision/v2.1/analyze";
    
    var params = {
        "visualFeatures": "Adult,Brands,Categories,Color,Description,Faces,ImageType,Objects,Tags",
        "details": "Landmarks",
        //"maxCandidates": "10",
        "language": "en",
    };
    //顯示分析的圖片
    var sourceImageUrl = document.getElementById("inputImage").value;
    document.querySelector("#sourceImage").src = sourceImageUrl;
    //送出分析
    $.ajax({
        url: uriBase + "?" + $.param(params),
        // Request header
        beforeSend: function(xhrObj){
            xhrObj.setRequestHeader("Content-Type","application/json");
            xhrObj.setRequestHeader("Ocp-Apim-Subscription-Key", subscriptionKey);
        },
        type: "POST",
        // Request body
        data: '{"url": ' + '"' + sourceImageUrl + '"}',
    })
    .done(function(data) {
        //顯示JSON內容
        $("#responseTextArea").val(JSON.stringify(data, null, 2));
        $("#picDescription").empty();
        var name = encodeURIComponent(data.categories[0].detail.landmarks[0].name);
        var url = 'https://en.wikipedia.org/wiki/' + name;
        $("#picDescription").append('<a href="'+ url +'">' + url + '</a>');
        $("#WikiPedia").val
        //$("#picDescription").append("https://en.wikipedia.org/wiki/"+name);
        //console.log(name);
        //for (var x = 0; x < data.description.captions.length;x++){
        //    $("#picDescription").append(data.description.captions[x].text + "<br>");
        //}
        // $("#picDescription").append("這裡有"+data.faces.length+"個人");
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        //丟出錯誤訊息
        var errorString = (errorThrown === "") ? "Error. " : errorThrown + " (" + jqXHR.status + "): ";
        errorString += (jqXHR.responseText === "") ? "" : jQuery.parseJSON(jqXHR.responseText).message;
        alert(errorString);
    });
};