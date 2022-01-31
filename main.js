var express = require("express");
var app = express();

var fs = require('fs');
var bodyParser = require('body-parser');
var sanitizeHtml = require('sanitize-html');
var compression = require("compression");



var indexRouter = require("./routes/index");
var psRouter = require("./routes/ps_route");
var analysisRouter = require("./routes/analysis");
var predictRouter = require("./routes/predict");


//middleware
app.use(compression()); //compression use code
app.use(bodyParser.urlencoded({extended: false})); //bodyParser use code
app.use(function(req, res, next){
  fs.readdir(`./data/`, function(err, filelist){
    // console.log(filelist);
    req.list = filelist;
    next();
  });
});
app.use(function(req, res, next){
  fs.readdir(`./predict_column/`, function(err, column_name){
    req.columns = column_name;
    // console.log(column_name);
    next();
  });
});



app.use("/", indexRouter);
app.use("/ps", psRouter);
app.use("/analysis", analysisRouter);
app.use("/predict", predictRouter);

app.listen(3000, function() {
  console.log("Example app listening on port 3000!");
});
