var ajax = {};
ajax.x = function() {
  var xhr = new XMLHttpRequest();
  return xhr;
};


ajax.send = function(url, method, data, responseCallback, sync) {
  var xhr = ajax.x();
  xhr.open(method, url, sync);
  xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  xhr.onreadystatechange = function () {
    if(xhr.readyState == 4 && xhr.status == 200) {
      var result = xhr.responseText;
      console.log("Result: " + result);
    }
  };
  xhr.send(data);
};

ajax.CreateForm = function(data) {
  form_data = new FormData();
  for(item in data) {
    form_data.append(item, data[item]);
  }
  return form_data;
}
  


var app = {};
app.init = function () {
  console.log('app initiatated');
  responseBox = document.getElementById('responseBox');
  responseCallback = function (response){
    responseObject = JSON.parse(response);
    console.log(responseObject);
    if (responseObject.success !== 1) {
      responseBox.innerHTML = responseObject.msg;
    }
  }

  // Button Actions
  document.getElementById("Light-ON").onclick = function (event) {
    event.preventDefault();
    console.log("light ON button clicked");
    var info = {state: 1};
    var data = ajax.CreateForm(info);
    ajax.send('/php/Light_Control.php', 'POST', data, responseCallback, false);
  }


  document.getElementById("Light-OFF").onclick = function (event) {
    event.preventDefault();
    console.log('light OFF button pressed');
    var info = {state: 0};
    var data = ajax.CreateForm(info);	
    ajax.send('/php/Light_Control.php', 'POST', data, responseCallback, false);
  }

 

  document.getElementById("Take-Picture").onclick = function (event) {
    event.preventDefault();
    console.log("Take photo button clicked");
    var info = {state: 1};
    var data = ajax.CreateForm(info);
    ajax.send("/php/Take_Photo.php", 'POST', data, responseCallback, false);
  }
  // end of init function.
}


app.init();
