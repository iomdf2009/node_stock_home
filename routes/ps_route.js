var express = require("express");
var router = express.Router();

var template = require("../template.js");
var fs = require('fs');
var sanitizeHtml = require("sanitize-html");
var path = require("path");
var multer = require('multer'); //express fileupload
var temp_filename = '';

var upload = multer({
  storage: multer.diskStorage({
    destination: function(req, file, cb){
      console.log("file info :: ", file);
      console.log("file.originalname.split('.')[0] :: ", file.originalname.split('.')[0]);
      fs.rmdirSync(`./uploads/${file.originalname.split('.')[0]}`, {recursive: true, force:true});
      fs.mkdir(`./uploads/${file.originalname.split('.')[0]}`, function(err){
        fs.readdir(`./uploads/${file.originalname.split('.')[0]}`, function(err, filelist){
          console.log(`Upload File :: ${filelist}`);
          cb(null, `./uploads/${file.originalname.split('.')[0]}`);
        });
      });
    },
    filename: function(req, file, cb){
      cb(null, `${file.originalname.split('.')[0]}_${Date.now()}.csv`);
    }
  })
});


router.post(`/create`, function(req, res){
  var list = template.list(req.list);
  // console.log(req.list);
  var i = 0;
  var html = template.HTML(list, ``,
    `<form  action="/ps/create_process" method="post">
        <p>종목번호(stock_id)<br><input type="text" name="stock_id" placeholder="종목번호"></p>
        <p>종목이름(stock_name)<br><input type="text" name=stock_name placeholder="종목이름"></p>
        <p>
          -데이터주기(stock_data)-<br>
          <input type="radio"  name="stock_data" value="day" checked>일별데이터<br>
          <input type="radio"  name="stock_data" value="week">주별데이터<br>
          <input type="radio"  name="stock_data" value="month">월별데이터<Br>
        </p>
        <p>
          -예측할 목록(predict_columns)-<Br>
    `
    +
      template.predict_checkbutton(req.columns)
    +
    `
        </p>
        <p><input type="submit" value="Insert"></p>
      </form>`,
        ``);

  res.send(html);
});

router.post(`/create_process`, function(req, res){
  var body = req.body;
  console.log(body.stock_id);
  console.log(body.stock_name);
  console.log(body.stock_data);
  console.log(body.predict_columns);

  var sanitizedStock_id = sanitizeHtml(body.stock_id);
  var sanitizedStock_name = sanitizeHtml(body.stock_name);
  var sanitizedStock_data = sanitizeHtml(body.stock_data);
  var sanitizedPredict_columns = sanitizeHtml(body.predict_columns);
  var text_area = "stock_id," + sanitizedStock_id + ",stock_name," + sanitizedStock_name;
  text_area = text_area + ",stock_data," + sanitizedStock_data + ",predict_columns," + sanitizedPredict_columns;


  fs.writeFile(`./data/${sanitizedStock_id}_${sanitizedStock_data}`, text_area, function(err){

    res.redirect(`/`);
    res.end();
  });
});

router.get(`/:stock_id`, function(req, res){
  var stock_id = req.params.stock_id;
  var sanitizedStock_id = sanitizeHtml(stock_id);
  var list = template.list(req.list);
  // console.log(sanitizedStock_id);
  fs.readFile(`./data/${sanitizedStock_id}`, 'utf8', function(err, stock_name){
    fs.readdir(`./uploads/${sanitizedStock_id}`, function(err, uploadedFilename){
      var sanitizedUploadedFilename = sanitizeHtml(uploadedFilename);
      console.log(sanitizedUploadedFilename);
      if(sanitizedUploadedFilename === "undefined") {
        sanitizedUploadedFilename = "Un_uploaded_File";
      }
      sanitizedStock_name = sanitizeHtml(stock_name);
      split_Stock_name = sanitizedStock_name.toString().split(',');
      var sanitizedStock_name = sanitizeHtml(split_Stock_name[3]);
      var sanitizedStock_data = sanitizeHtml(split_Stock_name[5]);
      var predict_columns = [];
      var i = 0;
      while(i<split_Stock_name.length-7){
        predict_columns.push(split_Stock_name[i+7]);
        i = i + 1;
      }
      console.log("predict_columns :: ", predict_columns);


      console.log(split_Stock_name);

      var html = template.HTML(
        list,
        `<td width=300>
          <h2> Stock ID ${sanitizedStock_id}</h2>
          <table>
            <tr>
              <td>
                <form action="/analysis/analysis_process" method="post" onsubmit="return confirm('분석하시겠습니까?')">
                  <input type="hidden" name="stock_id" value=${sanitizedStock_id}>
                  <input type="hidden" name="stock_name" value=${sanitizedStock_name}>
                  <input type="submit" value="Analysis">
                </form>
              </td>
              <td>
                <form action="/analysis/main" method="post">
                  <input type="hidden" name="stock_id" value=${sanitizedStock_id}>
                  <input type="hidden" name="stock_name" value=${sanitizedStock_name}>
                  <input type="submit" value="AnalysisConclusion">
                </form>
              </td>
              <td>
                <form action="/predict/run_process" method="post">
                  <input type="hidden" name="stock_id" value=${sanitizedStock_id}>
                  <input type="hidden" name="stock_name" value=${sanitizedStock_name}>
                  <input type="submit" value="PredictRun">
                </form>
              </td>
              <td>
                <form action="/predict/main" method="post">
                  <input type="hidden" name="stock_id" value=${sanitizedStock_id}>
                  <input type="hidden" name="stock_name" value=${sanitizedStock_name}>
                  <input type="submit" value="Predict">
                </form>
              </td>
            </tr>
          </table>
         </td>`,
          `<form action="./delete_process" method="post"
          onsubmit="return confirm('정말로 삭제하시겠습니까?');">
            <input type="hidden" name="stock_id" value="${sanitizedStock_id}">
            <input type="submit" value="Delete">
          </form>`,
          `<td width=400>
            <h3>Stock name</h3>
            <p>
            종목이름 : ${sanitizedStock_name}<br>
            종목데이터 : ${sanitizedStock_data}<br>
            예측목록 : ${predict_columns}

            </p>

            <form action="./upload" method="post" enctype="multipart/form-data">
              <input type="file" name="stock_dataset">
              <input type="hidden" name="stock_id" value=${sanitizedStock_id}>
              <input type="submit" value="csv올리기">
            </form>
            uploadedFilename : ${sanitizedUploadedFilename}
           </td>`);
      res.send(html);
    });
  });
});

router.post(`/upload`, upload.single("stock_dataset"), function(req, res){
  var body = req.body;
  var sanitizedStock_id = sanitizeHtml(body.stock_id);
  temp_filename = sanitizedStock_id;

  console.log("req.file = " + req.file);
  console.log("sanitizedStock_id = " + sanitizedStock_id);
  var sanitizedreqFile = sanitizeHtml(req.file)
  console.log("reqfileStatus = " + sanitizedreqFile);

  if( sanitizedreqFile === "undefined") {
    res.send(`<script> alert('파일을 업로드해주세요');
    location.href = '/ps/${sanitizedStock_id}'</script>`);
  } else {
    res.redirect(`./${req.file.originalname.split('.')[0]}`);
    res.end();
  }

});


router.post(`/delete_process`, function(req, res){
  var body = req.body;
  var sanitizedStock_id = body.stock_id;
  // console.log(`stock_id = ${sanitizedStock_id}`);
  fs.unlink(`./data/${sanitizedStock_id}`, function(err){
    console.log(`unlinked ${sanitizedStock_id}`);
    fs.rmdirSync(`./uploads/${sanitizedStock_id}`, {recursive: true, force: true});
    fs.rmdirSync(`./models/${sanitizedStock_id}`, {recursive: true, force: true});
    fs.rmdirSync(`./charts/${sanitizedStock_id}`, {recursive: true, force: true});
    fs.rmdirSync(`./predict_charts/${sanitizedStock_id}`, {recursive: true, force: true});
    console.log(`./uploads :: removed_directory ${sanitizedStock_id}`);
    console.log(`./models :: removed_directory ${sanitizedStock_id}`);
    console.log(`./charts :: removed_directory ${sanitizedStock_id}`);
    console.log(`./predict_charts :: removed_directory ${sanitizedStock_id}`);
    res.redirect(`/`);
    res.end();
  });
});


module.exports = router;
