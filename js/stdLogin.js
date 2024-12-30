document.getElementById('stdLogin').addEventListener('click', function() {
    var studentId = document.getElementById('stdIdInput').value;
    var team = document.getElementById('teamInput').value;
    var sabt = document.getElementById('sabtInput').value;
    console.log(studentId, team, sabt);
    if (studentId == '1' && team == '1' && sabt =='s') {
        document.getElementById('stdError').innerHTML = '';
        // Perform your login logic here
        console.log('Login successful with Student ID:', studentId, 'Team:', team, 'Sabt:', sabt);
        localStorage.setItem('userType', 'j');
        localStorage.setItem('team', '1');
        window.location.href = 'pSel.html'; 
    } else if (studentId == '2' && team == '1' && sabt =='s') {
        document.getElementById('stdError').innerHTML = '';
        // Perform your login logic here
        console.log('Login successful with Student ID:', studentId, 'Team:', team, 'Sabt:', sabt);
        localStorage.setItem('userType', 'h');
        localStorage.setItem('team', '1');
        window.location.href = 'pSel.html'; 
    } else {
        document.getElementById('stdError').innerHTML = '無法登入，請檢查資料是否正確';
    }
});