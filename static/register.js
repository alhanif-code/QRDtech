const name = 'hanif'

function checkLogin(){
    const username = document.getElementById('username/email').value;
    const password = document.getElementById('login_password').value;

    const isEmail = username.includes('@');
    const body = {
        username: isEmail ? '' :username, 
        email: isEmail ? username : '',
        password: password
    }
    fetch('/login',{
        method: 'POST',
        headers: {'content-type': 'application/json'},
        body: JSON.stringify(body)
    })
    .then (response => response.json())
    .then (data => {
        if (data.status === 'success') {
            window.location.href='/';
        } else {
            alert('Login failed');
        }
    })
}

function checkRegister(){
    const username = document.getElementById('username').value;
    const password = document.getElementById('register_password').value;
    const email = document.getElementById('email').value;
    const body = {username, email, password};
    fetch('/register', {
        method: 'POST',
        headers: {'content-type': 'application/json'},
        body: JSON.stringify(body)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success'){
           alert('Registration successful');
           window.location.href='/login';
        } else {
            alert('Registration failed');
        }
    })
}