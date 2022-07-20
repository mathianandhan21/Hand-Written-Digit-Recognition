function sendResponse() {
    // var url = "http://127.0.0.1:5000/get_response"
    var url = window.location.origin + "/get_response";
    $.get(url,function(data, status){
        if(data !== "undefined"){
            console.log(data)
           
            
        }
    })
  }