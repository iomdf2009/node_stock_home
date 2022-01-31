var express = require("express");
var router = express.Router();

var template = require("../template.js")



router.get(`/`, function(req, res){
  var list = template.list(req.list);
  var html = template.HTML(list,``, `
    <form action="/ps/create" method="post">
      <input type="submit" name="" value="Create">
    </form>`,``);

  res.send(html);
});


module.exports = router;
