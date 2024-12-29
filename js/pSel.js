var userType = localStorage.getItem('userType') ?? 'j';
var team = localStorage.getItem('team') ?? '1';    
var stdName = localStorage.getItem('stdName') ?? '陳彥廷';    
var currentDate = new Date();  
var formJ2Date = localStorage.getItem('formJ2Date') ?? currentDate;
var formH2Date = localStorage.getItem('formH2Date') ?? currentDate;
var selectionTab = document.getElementById('selectionTab');
var userDisplay = document.getElementById("userDisplay");
var JSelRange = localStorage.getItem('JSelRange') ?? '6';
var HSelRange = localStorage.getItem('HSelRange') ?? '6';
var formtype;

function convertToChineseNumeral(num) {
    const chineseNumerals = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九'];
    if (num < 10) {
        return chineseNumerals[num];
    } else if (num < 20) {
        return '十' + (num % 10 === 0 ? '' : chineseNumerals[num % 10]);
    } else {
        return chineseNumerals[Math.floor(num / 10)] + '十' + (num % 10 === 0 ? '' : chineseNumerals[num % 10]);
    }
}

if (userType == 'j' && currentDate != formJ2Date) {
    document.getElementById('formType').innerHTML = '第一次選課｜國中部';
    formtype = 'j1';
    for (var i = 1; i <= JSelRange; i++) {
        if (i === 1) {
            var button = document.createElement('button');
            button.className = 'nav-link active';
            button.id = 'section-i-tab';
            button.setAttribute('data-bs-toggle', 'tab');
            button.setAttribute('data-bs-target', '#section1');
            button.type = 'button';
            button.role = 'tab';
            button.innerText = '第一節';
            selectionTab.appendChild(button);
        }
        else {
            var button = document.createElement('button');
            n = convertToChineseNumeral(i);
            button.className = 'nav-link';
            button.id = 'section-i-tab';
            button.setAttribute('data-bs-toggle', 'tab');
            button.setAttribute('data-bs-target', '#section' + i);
            button.type = 'button';
            button.role = 'tab';
            button.innerText = '第' + n + '節';
            selectionTab.appendChild(button);
        }
    }
} else if (userType == 'j' && currentDate == formJ2Date) {
    document.getElementById('formType').innerHTML = '第二次選課｜國中部';
    formtype = 'j2';
} else if(userType == 'h' && currentDate != formH2Date) {
    document.getElementById('formType').innerHTML = '第一次選課｜高中部';
    formtype = 'h1';
}
else if(userType == 'h' && currentDate == formH2Date) {
    document.getElementById('formType').innerHTML = '第二次選課｜高中部';
    formtype = 'h2';
}



// Classes Display



// display the user type and team
switch(team){
    case '1':
        userDisplay.appendChild(document.createTextNode('第一小隊 - ' + stdName));
        break;
    case '2':
        userDisplay.appendChild(document.createTextNode('第二小隊 - ' + stdName));
        break;
    case '3':
        userDisplay.appendChild(document.createTextNode('第三小隊 - ' + stdName));
        break;
    case '4':
        userDisplay.appendChild(document.createTextNode('第四小隊 - ' + stdName));
        break;
    case '5':
        userDisplay.appendChild(document.createTextNode('第五小隊 - ' + stdName));
        break;
    case '6':
        userDisplay.appendChild(document.createTextNode('第六小隊 - ' + stdName));
        break;
    case '7':
        userDisplay.appendChild(document.createTextNode('第七小隊 - ' + stdName));
        break;
    case '8':
        userDisplay.appendChild(document.createTextNode('第八小隊 - ' + stdName));
        break;
}

