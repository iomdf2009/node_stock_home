var express = require("express");
var router = express.Router();

var template = require("../template.js");
var python_process = require("../py_process.js");

var fs = require("fs");
var sanitizeHtml = require("sanitize-html");

//middleware
router.use(express.static("charts"));
router.use(express.static("predict_charts"));

// router.use(function(req, res, next) {
//   fs.readdir(`./charts`, function(err, folderList){
//     i = 0;
//     if(folderList === undefined){
//       next();
//     } else {
//       while(i < folderList.length){
//         // console.log("predict.js/middleware :: folderList[" + i + "] = " +  folderList[i]);
//         // express.static(`./charts/${folderList[i]}`);
//         i = i + 1;
//       }
//       next();
//     }
//
//   });
// });

router.post(`/main`, function(req, res){

  var body = req.body;
  var sanitizedStock_id = sanitizeHtml(body.stock_id);
  var sanitizedStock_name = sanitizeHtml(body.stock_name);
  var columns = req.columns;
  console.log("/predict/main :: columns = " + columns)
  console.log("/predict/main :: predict_sanitizedStock_id = " + sanitizedStock_id);
  console.log("/predict/main :: predict_sanitizedStock_name = " + sanitizedStock_name);
  var week_day_text = sanitizedStock_id.toString().split('_')[1]
  // console.log("week_day_text :: ",week_day_text);

  fs.readdir(`./uploads/${sanitizedStock_id}/`, function(err, csv_name){
    fs.readdir(`./predict_charts/${sanitizedStock_id}`, function(err, file_name){
      // console.log("/main(/predict_charts) :: file_name = ", file_name);
      // console.log("/main(/predict_charts) :: file_name.length = ", file_name.length);

      console.log("/predict/main(./upload/)" + sanitizedStock_id + " : " + csv_name);
      console.log("/predict/main(err) : " + err);
      var csv_df_log = 0;

      if(csv_name === undefined){
        res.send(`<script>alert('분석파일이 없습니다. (파일업로드 하기)');
        location.href = '/ps/${sanitizedStock_id}'</script>`);
        res.end();
      } else {
        for(var i = 0; i <=csv_name.length ; i++){
          if(csv_name.toString().split('.')[i] === "csv_df"){
            csv_df_log = 1;
          }
        }

        if(csv_df_log === 0){
          res.send(`<script>alert('분석파일이 필요합니다.(Analysis 버튼 미실행)');
          location.href = '/ps/${sanitizedStock_id}'</script>`);
          res.end();
        } else {
          var predictCntChartbutton = template.predictCntChartbutton(sanitizedStock_id, sanitizedStock_name, file_name);
          var predictButton = template.predictButton(sanitizedStock_id, sanitizedStock_name, columns);
          var predictHTML = template.predictHTML(
            sanitizedStock_id,
            sanitizedStock_name,
            predictButton,
            `No chart`,
            predictCntChartbutton,
            week_day_text);
          res.send(predictHTML);
        }
      }
    });
  });
});

router.post(`/spec`, function(req, res){
  var body = req.body;
  var sanitizedStock_id = sanitizeHtml(body.stock_id);
  var sanitizedStock_name = sanitizeHtml(body.stock_name);
  var sanitizedStock_column = sanitizeHtml(body.stock_column);
  var columns = req.columns;
  console.log("/predict/main/spec :: columns = " + columns);
  console.log("/predict/main/spec :: predict_sanitizedStock_id = " + sanitizedStock_id);
  console.log("/predict/main/spec :: predict_sanitizedStock_name = " + sanitizedStock_name);
  console.log("/predict/main/spec :: predict_sanitizedStock_column = " + sanitizedStock_column);
  var week_day_text = sanitizedStock_id.toString().split('_')[1]
  // console.log("week_day_text :: ",week_day_text);
  fs.readdir(`./predict_charts/${sanitizedStock_id}`, function(err, file_name){
    var predictCntChartbutton = template.predictCntChartbutton(sanitizedStock_id, sanitizedStock_name, file_name);
    var predictButton = template.predictButton(sanitizedStock_id, sanitizedStock_name, columns);
    var predictHTML = template.predictHTML(
      sanitizedStock_id,
      sanitizedStock_name,
      predictButton,
      `<img src='./${sanitizedStock_id}/${sanitizedStock_column}_${sanitizedStock_id}_charts.png' alt="${sanitizedStock_column}.png"/>`,
      predictCntChartbutton,
      week_day_text);
    res.send(predictHTML);
  });

});

router.post(`/run_process`, function(req, res){

  var body = req.body;
  var sanitizedStock_id = sanitizeHtml(body.stock_id);
  var columns = req.columns;
  var csv_df_log = 0;
  var sanitizedFile_name = '';

  fs.mkdir(`./models/${sanitizedStock_id}`, function(err) {
    if(err) {
      console.log(err.code);
    }

  });
  fs.mkdir(`./charts/${sanitizedStock_id}`, function(err) {
    if(err) {
      console.log(err.code);
    }
  });
  fs.mkdir(`./predict_charts/${sanitizedStock_id}`, function(err) {
    if(err) {
      console.log(err.code);
    }
  });

  fs.readdir(`./uploads/${sanitizedStock_id}`, function(err, csv_name){
    console.log("/predict/run_process(./uploads) :: csv_name = ", csv_name);

    if(csv_name === undefined){
      res.send(`<script> alert('분석파일이 없습니다. (파일업로드 하기)');
      location.href = '/ps/${sanitizedStock_id}'</script>`);
      res.end();
    } else {
      for(var i = 0; i <=csv_name.length ; i++){
        if(csv_name.toString().split('.')[i] === "csv_df"){
          csv_df_log = 1;
        }
      }
      if(csv_df_log === 0){
        res.send(`<script>alert('분석파일이 필요합니다.(Analysis 버튼 미실행)');
        location.href = '/ps/${sanitizedStock_id}'</script>`);
        res.end();
      } else {
        fs.readFile(`./data/${sanitizedStock_id}`, 'utf8', function(err, stock_text){
          var split_stock_text = stock_text.toString().split(',');
          console.log("split_stock_text :: ", split_stock_text);
          var predict_columns = [];
          var i = 0;
          while(i<split_Stock_name.length-7){
            predict_columns.push(split_Stock_name[i+7]);
            i = i + 1;
          }
          var splitDot_csv_name = csv_name.toString().split('.');
          console.log("/predict/run_process(./uploads) :: splitDot_csv_name = " + splitDot_csv_name[1]);
          var splitUnderbar_csv_name = splitDot_csv_name[1].toString().split('_');
          sanitizedFile_name = sanitizeHtml(splitUnderbar_csv_name[2])
          console.log("/predict/run_process(./uploads) :: splitUnderbar_csv_name = " + sanitizedFile_name);

          var py_Process = python_process.py_Model(`./stock_gru_model_spwan.py`,
            sanitizedStock_id,
            sanitizedFile_name,
            predict_columns);

          res.send(`<script> alert('Model 생성 완료 ([Predict] 버튼 눌러 확인하기)');
          location.href = '/ps/${sanitizedStock_id}'</script>`);
          res.end();
        });
      }
    }
  });
  // res.send("/predict/run_process page")
});

router.post(`/count_predict`, function(req, res){
  var post = req.body;

  var sanitizedStock_id = sanitizeHtml(post.stock_id);
  var sanitizedStock_name = sanitizeHtml(post.stock_name);
  var sanitizedPredict_count = sanitizeHtml(post.predict_count);
  var columns = req.columns;
  var sanitizedWeekDayText = sanitizeHtml(sanitizedStock_id.toString().split('_')[1])


  fs.readdir(`./uploads/${sanitizedStock_id}`, function(err, stock_filename){
    fs.readFile(`./data/${sanitizedStock_id}`, "utf8", function(err, stock_text){
      fs.readdir(`./predict_charts/${sanitizedStock_id}`, function(err, chart_filename){
        // console.log("predict/count_predict :: stock_text = ", stock_text);
        var split_stock_text = stock_text.toString().split(',');
        var predict_columns = [];
        var i = 0;
        while(i<split_stock_text.length-7){
          predict_columns.push(split_stock_text[i+7]);
          i = i + 1;
        }
        console.log("predict/count_predict :: predict_columns = ", predict_columns);

        // console.log("predict/count_predict :: stock_filename = ", stock_filename);
        var split_dot_filename = stock_filename.toString().split('.');
        var split_underbar_filename = split_dot_filename[0].toString().split('_');
        console.log("predict/count_predict :: split_underbar_filename = ", split_underbar_filename[2]);
        console.log("predict/count_predict :: sanitizedStock_id = ", sanitizedStock_id);
        console.log("predict/count_predict :: sanitizedStock_name = ", sanitizedStock_name);
        console.log("predict/count_predict :: sanitizedPredict_count = ", sanitizedPredict_count);


        var py_Process = python_process.py_Model2(`./models_predict_array_spwan.py`,
          sanitizedStock_id,
          split_underbar_filename[2],
          predict_columns,
          sanitizedPredict_count
        );
        var predictCntChartbutton = template.predictCntChartbutton(sanitizedStock_id, sanitizedStock_name, chart_filename);
        var predictButton = template.predictButton(sanitizedStock_id, sanitizedStock_name, columns)
        var predictHTML = template.predictHTML(sanitizedStock_id,
            sanitizedStock_name,
            predictButton,
            `<img src="./${sanitizedStock_id}/predict_${sanitizedStock_id}_${sanitizedPredict_count}datas_charts.png"
            alt="${sanitizedStock_id}_${sanitizedPredict_count}datas_charts">`,
            predictCntChartbutton,
            sanitizedWeekDayText);
        res.send(predictHTML);

      });
    });
  });
})

router.post(`/close_chart`, function(req, res){
  var post = req.body;
  var sanitizedStock_id = sanitizeHtml(post.stock_id);
  var sanitizedStock_name = sanitizeHtml(post.stock_name);
  var sanitizedPredict_count = sanitizeHtml(post.predict_count);
  var sanitizedWeekDayText = sanitizeHtml(post.week_day_text);

  var columns = req.columns;
  fs.readdir(`./predict_charts/${sanitizedStock_id}`, function(err, file_name){
    console.log("predict/close_chart :: sanitizedStock_id = ", sanitizedStock_id);
    console.log("predict/close_chart :: sanitizedStock_name = ", sanitizedStock_name);
    console.log("predict/close_chart :: sanitizedPredict_count = ", sanitizedPredict_count);
    console.log("predict/close_chart :: sanitizedWeekDayText = ", sanitizedWeekDayText);
    var predictCntChartbutton = template.predictCntChartbutton(sanitizedStock_id, sanitizedStock_name, file_name);
    var predictButton = template.predictButton(sanitizedStock_id, sanitizedStock_name, columns);
    var predictHTML = template.predictHTML(sanitizedStock_id,
        sanitizedStock_name,
        predictButton,
        `<img src="./${sanitizedStock_id}/predict_${sanitizedStock_id}_${sanitizedPredict_count}datas_charts.png",
         alt="${sanitizedStock_id}_${sanitizedPredict_count}datas_charts"`,
         predictCntChartbutton,
        sanitizedWeekDayText);

    res.send(predictHTML);
  });
});



module.exports = router;
