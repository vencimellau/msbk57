var login = document.getElementById("login");

login.setAttribute("onclick", "Login()");

async function Login(){
    let username = document.getElementById("username").value
    let password = document.getElementById("password").value
    const data = {"username" : username,
                "password" : password};
    fetch('http://localhost:8001/login', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
      },
        body: JSON.stringify(data)
      })
      .then(response => {
        if (response.status !== 401) {
          window.location.href = 'http://localhost:8001/protected'
        }
        else{
          console.log("Bad auth")
        }
      });
    }