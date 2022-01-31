var express = require("express");
var router = express.Router();

var template = require("../template.js");
var fs = require("fs");
var path = require("path");
var sanitizeHtml = require("sanitize-html");


router.post(`/analysis_process`, function(req, res){
  var body = req.body;
  var sanitizedStock_id = body.stock_id;
  var sanitizedStock_name = body.stock_name;


  fs.readdir(`./uploads/${sanitizedStock_id}`, function(err, csv_name){
    console.log(`csv_name = ${csv_name}`);

    if(csv_name === undefined){
      res.send(`<script> alert('분석 파일이 없습니다.');
      location.href = '/ps/${sanitizedStock_id}'</script>`);
      res.end();
    } else {

      var spawn = require("child_process").spawn;  //python 구동을 위한 자식프로세스 생
      var pyProcess = spawn('python', ['./stock_parser_args_v2.py',
      `./uploads/${sanitizedStock_id}/${csv_name[0]}`,
      `./uploads/${sanitizedStock_id}/${csv_name[0]}_df.csv`]);
      //spawn([구동 프로세스 언어], [args0, args1, args2 ....])

      pyProcess.stdout.on('data', function(data){
        console.log(data.toString());
      }); // pyProcess이름의 자식 프로세서 구동시 출력데이터 를 data 변수화 하여 console.log 출
      pyProcess.stderr.on('data', function(data){
        console.log(data.toString());
      }); //pyProcess 자식프로세서 구동시 에러일 경우 data 변수화 하여 console.log 출

      res.redirect(`/ps/${sanitizedStock_id}`);
      res.end();
    }
  });
});


router.post(`/main`, function(req, res){
  var body = req.body;
  var sanitizedStock_id = body.stock_id;
  var sanitizedStock_name = body.stock_name;

  fs.readdir(`./uploads/${sanitizedStock_id}`, function(err, csv_name){
    console.log(`csv_name = ${csv_name}`);
    // console.log(`${csv_name.toString().split('.')[3]}`);
    if(csv_name === undefined) {
      res.send(`<script> alert('분석 파일이 없습니다.');
      location.href = '/ps/${sanitizedStock_id}'</script>`);
      res.end();
    } else {
        // console.log("sss" + csv_name.toString().split('.')[2])
        if(csv_name.toString().split('.')[2] === "csv_df") {
          fs.readFile(`./uploads/${sanitizedStock_id}/${csv_name[0]}_df.csv`, 'utf8', function(err, csv_data){
            console.log(`./uploads/${sanitizedStock_id}/${csv_name[0]}_df.csv`);
            var html = template.analysisHTML(sanitizedStock_id, sanitizedStock_name, `
              <h2> Stock Analysis Dataframe </h2>
              <form action="/ps/${sanitizedStock_id}" method="get">
                <p>
                  <input type="submit" value="StockList">
                </p>
              </form>
              <form action="index.html" method="post">
                <textarea name="analysis_df_textarea" rows="30" cols="250">${csv_data}</textarea>
              </form>
              `);
            res.send(html);
          });
        } else {
          res.send(`<script> alert('분석을 수행하지 않았습니다. (Analysis 버튼 실행)');
          location.href = '/ps/${sanitizedStock_id}'</script>`);
          res.end();
        }
    }

  });
});

module.exports = router;
