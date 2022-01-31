var spawn = require("child_process").spawn;

var py_process = {
  py_Model : function(py_fileName, Stock_id, Stock_name, columns) {
    var python_process = null;
    var i = 0;
    var columns_string = '';
    console.log("var py_process :: columns = ", columns);
    // for(var j=0; j<columns.length;j++){
    //   columns_string = columns_string + columns[j];
    //   if(j !== columns.length-1){
    //     columns_string = columns_string + ',';
    //   }
    // console.log("var py_process :: columns_string = ",  columns_string)
    // }
    while(i < columns.length){
      console.log("py_process.js : py_Model :: column[" + i + "] = " + columns[i]);
      python_process = new spawn("python", [py_fileName, Stock_id, Stock_name, columns ,columns[i]]);

      python_process.stdout.on("data", function(data){
        console.log(data.toString());
      });
      python_process.stderr.on("data", function(data){
        console.log(data.toString());
      });

      i = i + 1;
    }
  },
  py_Model2 : function(py_fileName, Stock_id, Stock_name, columns, predict_count) {
    var python_process = null;
    var i = 0;
    var columns_string = '';
    console.log("var py_process :: columns = ", columns);
    // for(var j=0; j<columns.length;j++){
    //   columns_string = columns_string + columns[j];
    //   if(j !== columns.length-1){
    //     columns_string = columns_string + ',';
    //   }
    // console.log("var py_process :: columns_string = ",  columns_string)
    // }
    while(i < columns.length){
      console.log("py_process.js : py_Model2 :: column[" + i + "] = " + columns[i]);
      i = i + 1;
    }
    python_process = new spawn("python", [py_fileName, Stock_id, Stock_name, columns, predict_count]);

    python_process.stdout.on("data", function(data){
      console.log(data.toString());
    });
    python_process.stderr.on("data", function(data){
      console.log(data.toString());
    });

    i = i + 1;

  }
};

module.exports = py_process;
