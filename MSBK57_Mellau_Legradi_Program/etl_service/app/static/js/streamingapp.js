var counter = 0;

var radios = document.querySelectorAll('input[type="radio"]')
var play = document.getElementById('play')

play.setAttribute("onclick", 'sendWatchMin()')

for(var i=0;i<radios.length;i++){
    radios[i].setAttribute("onclick", 'sendRating('+ radios[i].id +')')
   }

function getMovieID(){
    return "1";
}

function getUserIDFromtStreamingPlatform(){
    return "1";
}

async function sendWatchMin() {
    if(counter == 0){
        document.getElementById('video').play();
        var start = new Date().getTime();
        counter++;
    }
    else{
        document.getElementById('video').pause();
        var end = new Date().getTime();
        counter = 0;
        var time = end - start;
        data = {"movideID" : getMovieID(),
                "userID" : getUserIDFromtStreamingPlatform(),
                "WatchMin" : time}
        postData('http://localhost:8002/watchmin',data)
    }
};

async function sendRating(button) {
    data = {"movideID" : getMovieID(),
                "userID" : getUserIDFromtStreamingPlatform(),
                "Rating" : button.value}
    var result = postData('http://localhost:8002/watchmin',data)
    .then(postData('http://localhost:8003/teach_svd',data))
    .then(function (response) {
        return response.json();
    })
    .catch(function (error) {
        console.log('Error', error)
    })
    return result
}

async function postData(url, data) {
    const response = await fetch(url, {
      method: 'POST',
      mode: 'cors', 
      cache: 'no-cache', 
      credentials: 'same-origin', 
      headers: {
        'Content-Type': 'application/json'
      },
      redirect: 'follow', 
      referrerPolicy: 'no-referrer', 
      body: JSON.stringify(data) 
    });
    return response.json(); 
  }