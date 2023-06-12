$(document).ready(function(){
    //do something
    $("#thisButton").click(function(){
        processImage();
    });
    $("#inputImageFile").change(function(e){
        processImageFile(e.target.files[0]);
    });
});
document.cookie = "cookieName=cookieValue; SameSite=None; Secure";


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
            if (data.categories[0].detail) {
                // 圖片中有地標的情況
                $("#picDescription").append("請點擊下方維基百科連結，學習圖中地標的知識");
                var name = encodeURIComponent(data.categories[0].detail.landmarks[0].name);
                var url = 'https://en.wikipedia.org/wiki/' + name;
                $("#picDescription").append('<a href="' + url + '">' + url + '</a>');
                var wiki_content = displaySearchResults(data.categories[0].detail.landmarks[0].name);
                $("#wikiContent").html(wiki_content);
            } else {
                // 圖片中沒有地標的情況
                $("#picDescription").append("照片裡沒有地標");
                $("#wikiContent").empty(); // 清空 wiki 內容
            }
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
        $("#picDescription").empty(); // 清空之前的內容
        if (data.categories[0].detail) {
            // 圖片中有地標的情況
            $("#picDescription").append("請點擊下方維基百科連結，學習圖中地標的知識");
            var name = encodeURIComponent(data.categories[0].detail.landmarks[0].name);
            var url = 'https://en.wikipedia.org/wiki/' + name;
            $("#picDescription").append('<a href="' + url + '">' + url + '</a>');
            var wiki_content = displaySearchResults(data.categories[0].detail.landmarks[0].name);
            $("#wikiContent").html(wiki_content);
        } else {
            // 圖片中沒有地標的情況
            $("#picDescription").append("照片裡沒有地標");
            $("#wikiContent").empty(); // 清空 wiki 內容
        }
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        //丟出錯誤訊息
        var errorString = (errorThrown === "") ? "Error. " : errorThrown + " (" + jqXHR.status + "): ";
        errorString += (jqXHR.responseText === "") ? "" : jQuery.parseJSON(jqXHR.responseText).message;
        alert(errorString);
    });
};

function displaySearchResults(pages) {
    var pageId = Object.keys(pages)[0];
    var title = pages[pageId].title;
    var apiUrl = "https://en.wikipedia.org/w/api.php";
    var params = {
        action: "parse",
        page: title,
        format: "json",
        prop: "text"
    };

    // 發送搜尋請求
    $.ajax({
        url: apiUrl,
        dataType: "jsonp",
        data: params,
        success: function(data) {
            //var contentHtml = data.parse.text["*"];
            //$("#wikiContent").html(contentHtml);
            console.log(data);
            //var content = '<div class="mw-parser-output">\n<!-- \nNewPP limit report\nParsed by mw2434\nCached time: 20230609175808\nCache expiry: 1814400\nReduced expiry: false\nComplications: []\nCPU time usage: 0.002 seconds\nReal time usage: 0.003 seconds\nPreprocessor visited node count: 0/1000000\nPost‐expand include size: 0/2097152 bytes\nTemplate argument size: 0/2097152 bytes\nHighest expansion depth: 0/100\nExpensive parser function count: 0/500\nUnstrip recursion depth: 0/20\nUnstrip post‐expand size: 0/5000000 bytes\nNumber of Wikibase entities loaded: 0/400\n-->\n<!--\nTransclusion expansion time report (%,ms,calls,template)\n100.00%    0.000      1 -total\n-->\n</div>';
            var content = data.parse.text["*"];
            document.getElementById("wikiContent").innerHTML = content;
            console.log(content);
        },
        error: function(xhr, status, error) {
            console.log(error);
        }
    });
}
//難以讓wikipedia內容出現
