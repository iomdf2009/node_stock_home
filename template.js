var template = {
  HTML: function(list, title ,body1, body2){
    return `<html>
      <head>
        <meta charset="utf-8">
        <title>stock_precdiction_system</title>
      </head>
        <body>
        <h1><a href="/">Stock Prediction System</a></h1>
        <h2>${title}</h2>
        <table border="1" >
          <tr>
            <td width=400 align="top">
            <h2>Stock insert</h2>
            </td>
            ${title}
          </tr>
          <tr>
            <td>
              ${list}
              ${body1}
            </td>
              ${body2}
          </tr>
        </table>

        </body>
      </html>
      `;
  },
  list : function(filelist) {
    var list = `<ul>`;
    var i = 0;
    while(i < filelist.length)
    {
      list = list + `<li><a href="/ps/${filelist[i]}">${filelist[i]}</a></li>`
      i = i + 1;

    }
    list = list + `</ul>`;

    return list;
  },
  analysisHTML : function(title, name, body1) {
    return `<html>
        <head><title>${title} analysis</title></head>
        <body>
          <p>
          <h2> Stock ID : ${title}</h2>
          <p>${name}</p>
          <p>${body1}</p>


          </p>
          </table>
        </body>
      </html>`;
  },
  predictHTML : function(title, name, body1, body2, body3, week_day_text) {
    return `<!DOCTYPE html>
    <html lang="en" dir="ltr">
      <head>
        <meta charset="utf-8">
        <title>predict ${title}</title>
      </head>
      <body>
      <h1>predict</h1>
      <h2> Stock_id : ${title} </h2>
      <h3> stock_name : ${name} </h3>
      <table border>
        <tr>
          <td>
            <form action="/ps/${title}" method="get">
              <p>
                <input type="submit" value="StockList">
              </p>
            </form>
          </td>
          <td>
            <form action="/predict/count_predict" method="post">
              <p>prediction
                <input type="hidden" name="stock_id" value=${title}>
                <input type="hidden" name="stock_name" value=${name}>
                <select name="predict_count">
                  <option value="5" selected>5</option>
                  <option value="10">10</option>
                  <option value="20">20</option>
                  <option value="30">30</option>
                </select>
                ${week_day_text} <input type="submit" value="PredictRun">
              </p>
            </form>
          </td>
        </tr>
      </table>
      <table border>
        <tr>
          <td>
            <h3>Training Model based charts</h3>
            ${body1}
          </td>
          <td rowspan="2">
            ${body2}
          </td>
        </tr>
        <tr>
          <td>
            <h3>Prediction ${week_day_text} charts</h3>
            ${body3}
          </td>
        </tr>
      </table>
      </body>
    </html>`;
  },
  predictButton : function(stock_id, stock_name, columns) {
    var i = 0;
    var button = '';
    while(i < columns.length){
      var button = button + `
        <form action="./spec" method="post">
          <input type="hidden" name="stock_id" value=${stock_id}>
          <input type="hidden" name="stock_name" value=${stock_name}>
          <input type="hidden" name="stock_column" value=${columns[i]}>
          <input type="submit" value="${columns[i]} Training Model">
        </form>
      `;
      i = i + 1;
    }
    return button;
  },
  predict_checkbutton : function(columns) {
    var i = 0;
    var button = '';
    while(i < columns.length){
      button = button + `
        <input type="checkbox" name="predict_columns" value="${columns[i]}" checked>${columns[i]}<Br>
      `;
      i = i + 1;
    }
    return button;
  },
  predictCntChartbutton : function(stock_id, stock_name, file_name){
    var i = 0;
    var button = '';
    var split_file_name = '';
    while(i < file_name.length){
      // console.log("template :: file_name.split('_') : ", file_name[i].toString().split('_'));
      split_file_name = file_name[i].toString().split('_');
      button = button + `
        <form action="/predict/close_chart" method="post">
        <input type="hidden" name="stock_id" value=${stock_id}>
        <input type="hidden" name="stock_name" value=${stock_name}>
        <input type="hidden" name="predict_count" value=${split_file_name[3].toString().replace(/[^0-9]/g,'')}> <!-- 숫자만 추출 -->
        <input type="hidden" name="week_day_text" value=${split_file_name[2]}>
        <input type="submit" value= "${split_file_name[2]} ${split_file_name[3]} predict">
        </form>
        `;
      i = i + 1;
    }

    return button;
  }
};



module.exports = template;
