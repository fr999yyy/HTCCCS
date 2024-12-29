var userType = localStorage.getItem('userType') ?? 'j';
var team = localStorage.getItem('team') ?? '1';    
var stdName = localStorage.getItem('stdName') ?? '陳彥廷';    
var currentDate = new Date();  
var formJ2Date = localStorage.getItem('formJ2Date') ?? currentDate;
var formH2Date = localStorage.getItem('formH2Date') ?? currentDate+1;
var sectionTab = document.getElementById('sectionTab');
var userDisplay = document.getElementById("userDisplay");
var JSelRange = localStorage.getItem('JSelRange') ?? 6;
var HSelRange = localStorage.getItem('HSelRange') ?? 6;
var totalSections = 12;
var formtype = 'j1';
function appendHtml(sectionNumber, className, classInfo, pfp) {
    const container = document.getElementById('section-tabContent');
    if (!container) {
        console.error('Element with id "section-tabContent" not found.');
        return;
    }
    className = className ?? '皇后搖滾街舞';
    classInfo = classInfo ?? '一百字街舞課程';
    pfp = pfp ?? 'profile';
    const newDiv = document.createElement('div');
    newDiv.classList.add('tab-pane', 'fade', 'p-3');
    newDiv.id = `section${sectionNumber}`;
    newDiv.setAttribute('role', 'tabpanel');
  
    const newHTML = `
      <h2 id="sectionTime${sectionNumber}" class="text-center mb-3">7/11 (四) 14:00~17:00</h2>
      <ul class="list-group">
         <li class="list-group-item">
          <div class="d-flex align-items-center">
                <select
                        class="form-select form-select-sm text-center"
                        name=""
                        id=""
                        style="width:auto;"
                    >
                        <option selected>選擇志願</option>
                        <option value="">1</option>
                        <option value="">2</option>
                        <option value="">3</option>
                        <option value="">4</option>
                </select>
                <div id="className${sectionNumber}" class="lead fw-bold mx-2">${className}</div>
                <button class="btn btn-secondary ms-auto me-3" type="button" data-bs-toggle="collapse" data-bs-target="#collapseC${sectionNumber}1" aria-expanded="false" aria-controls="collapseC${sectionNumber}">詳細資訊</button>
          </div>
          <div class="collapse" id="collapseC${sectionNumber}1">
            <div class="card card-body border-0 d-flex flex-row align-items-start ps-0">
              <img src="assets/${pfp}.jpg" class="rounded-circle profile mx-3" alt="" id="pfp${sectionNumber}" />
              <div id="classInfo${sectionNumber}" class="info">${classInfo}</div>
            </div>
          </div>
            </li>
            <li class="list-group-item">A third item</li>
            <li class="list-group-item">A fourth item</li>
            <li class="list-group-item">And a fifth one</li>
        </ul>  
    `;
  
    newDiv.innerHTML = newHTML;
    container.appendChild(newDiv);
  }
  
for (let i = 1; i <= 15; i++) {
console.log(i);
appendHtml(i, `皇后搖滾街舞${i}`, `一百字街舞課程${i}`);
}

if (formtype == 'j1') {
    document.title = '第一次選課｜國中部';
    document.getElementById('formType').innerHTML = '第一次選課｜國中部';
    document.getElementById('section-1-tab').classList.add('active');
    document.getElementById('section1').classList.add('active', 'show');
    for (var i = JSelRange; i < 15; i++) {
        document.getElementById('section-' + (i+1) + '-tab').remove();
    }
} else if (formtype == 'j2') {
    document.title = '第二次選課｜國中部';
    document.getElementById('formType').innerHTML = '第二次選課｜國中部';
    document.getElementById('section-'+ (JSelRange+1) +'-tab').classList.add('active');
    document.getElementById('section'+ (JSelRange+1) ).classList.add('active', 'show');
    for (var i = 0; i < 15; i++) {
        if (i >= JSelRange && i < totalSections) continue;
        document.getElementById('section-' + (i+1) + '-tab').remove();
    }
} else if(uformtype == 'h1') {
    document.title = '第一次選課｜高中部';
    document.getElementById('formType').innerHTML = '第一次選課｜高中部';
    document.getElementById('section-1-tab').classList.add('active');
    document.getElementById('section1').classList.add('active', 'show');
    for (var i = HSelRange; i < 15; i++) {
        document.getElementById('section-' + (i+1) + '-tab').remove();
    }
}
else if(formtype == 'h2') {
    document.title = '第二次選課｜高中部';
    document.getElementById('formType').innerHTML = '第二次選課｜國中部';
    document.getElementById('section-'+ (HSelRange+1) +'-tab').classList.add('active');
    document.getElementById('section'+ (HSelRange+1) ).classList.add('active', 'show');
    for (var i = 0; i < 15; i++) {
        if (i >= HSelRange && i < totalSections) continue;
        document.getElementById('section-' + (i+1) + '-tab').remove();
    }
}

// if (userType == 'j' && currentDate != formJ2Date) {
//     document.getElementById('formType').innerHTML = '第一次選課｜國中部';
//     formtype = 'j1';
//     document.getElementById('section-1-tab').classList.add('active');
//     document.getElementById('section1').classList.add('active', 'show');
//     for (var i = JSelRange; i < 15; i++) {
//         console.log('section-' + (i+1) + '-tab');
//         document.getElementById('section-' + (i+1) + '-tab').remove();
//     }
// } else if (userType == 'j' && currentDate == formJ2Date) {
//     document.getElementById('formType').innerHTML = '第二次選課｜國中部';
//     formtype = 'j2';
//     document.getElementById('section-'+ (JSelRange+1) +'-tab').classList.add('active');
//     document.getElementById('section'+ (JSelRange+1) ).classList.add('active', 'show');
//     for (var i = 0; i < JSelRange ; i++) {
//         console.log('section-' + (i+1) + '-tab');
//         document.getElementById('section-' + (i+1) + '-tab').remove();
//     }
//     for (var i = totalSections; i < 15; i++) {
//         console.log('section-' + (i+1) + '-tab');
//         document.getElementById('section-' + (i+1) + '-tab').remove();
//     }
// } else if(userType == 'h' && currentDate != formH2Date) {
//     document.getElementById('formType').innerHTML = '第一次選課｜高中部';
//     formtype = 'h1';
//     document.getElementById('section-1-tab').classList.add('active');
//     document.getElementById('section1').classList.add('active', 'show');
//     for (var i = HSelRange; i < 15; i++) {
//         console.log('section-' + (i+1) + '-tab');
//         document.getElementById('section-' + (i+1) + '-tab').remove();
//     }
// }
// else if(userType == 'h' && currentDate == formH2Date) {
//     document.getElementById('formType').innerHTML = '第二次選課｜高中部';
//     formtype = 'h2';
// }

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

