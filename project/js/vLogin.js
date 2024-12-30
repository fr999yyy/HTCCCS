document.getElementById('vLogin').addEventListener('click', function() {
    var password = document.getElementById('pwdInput').value;
    if (password === '1234') {
        document.getElementById('pwdError').innerHTML = '';
        window.location.href = 'result.html';
    } else {
        document.getElementById('pwdInput').innerHTML = '';
        document.getElementById('pwdError').innerHTML = '密碼錯誤！';  
    }
});

