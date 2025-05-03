
document.addEventListener('DOMContentLoaded', function() {
    const stdId = document.getElementById('stdId').textContent;  // Ensure std_id is properly escaped for JavaScript
    fetch(`/get_courses`)
        .then(response => response.json())
        .then(data => {
            const sectionsWithCourses = data.sections_with_courses;
            const sectionTab = document.getElementById('sectionTab');
            const sectionTabContent = document.getElementById('section-tabContent');
            const savedSelections = data.saved_selections;
            const test = data.test; //測試功能
            console.log('test:', test); //測試功能

            sectionsWithCourses.forEach((section, index) => {
                // Create tab button
                const button = document.createElement('button');
                button.className = 'nav-link';
                if (index === 0) button.classList.add('active');
                button.id = `section-${section.section_id}-tab`;
                button.setAttribute('data-bs-toggle', 'tab');
                button.setAttribute('data-bs-target', `#section${section.section_id}`);
                button.type = 'button';
                button.role = 'tab';
                button.textContent = section.section_display;
                // console.log(section.section_display);
                sectionTab.appendChild(button);

                // Create tab pane
                const tabPane = document.createElement('div');
                tabPane.className = 'tab-pane fade p-3';
                if (index === 0) tabPane.classList.add('show', 'active');
                tabPane.id = `section${section.section_id}`;
                tabPane.role = 'tabpanel';

                const sectionTime = document.createElement('h2');
                sectionTime.className = 'text-center mb-3';
                sectionTime.textContent = section.section_time;
                tabPane.appendChild(sectionTime);

                const listGroup = document.createElement('ul');
                listGroup.className = 'list-group';
                var n = 1; //測試功能

                section.courses.forEach(course => {
                    const listItem = document.createElement('li');
                    listItem.className = 'list-group-item';
                    const div = document.createElement('div');
                    div.className = 'd-flex align-items-center';
                    const select = document.createElement('select');
                    if (course.course_type === 'NA') {
                        course.course_name = '（連堂）' + course.course_name;
                    }
                    else if (course.course_type !== 'NA') {
                        select.className = 'form-select form-select-sm text-center';
                        select.name = 'priority';
                        select.style.width = 'auto';
                        const option = document.createElement('option');
                        option.selected = false; //測試功能
                        option.textContent = '選擇志願';

                        select.appendChild(option);
                        const testOption = document.createElement('option'); //測試功能
                        
                        console.log('test:', test); //測試功能
                        if (test === 0) {
                            testOption.selected = true; //測試功能
                        }


                        testOption.textContent = '測試'; //測試功能   
                        testOption.value = n+`-${course.course_id}-${stdId}-${section.section_id}`; //測試功能
                        // console.log(testOption.value); //測試功能
                        if (select){
                            select.appendChild(testOption); //測試功能
                        }
                        
                        n++; //測試功能
                        
                        for (let i = 1; i <= section.num_courses; i++) {
                            const option = document.createElement('option');
                            option.value = i + `-${course.course_id}-${stdId}-${section.section_id}`;
                            option.textContent = i;

                            if (savedSelections.includes(option.value)) {
                                option.selected = true;
                            }

                            select.appendChild(option);
                        }

                        div.appendChild(select);
                    }
                    

                    

                    const courseName = document.createElement('div');
                    const noCourseInfo = "相飛世？耳年童邊急六寺鳥綠燈向父貝食澡收！科足游彩王找頭孝請肖收田士西喝根見氣，星定朱具都公外反鼻時刃婆兔她着今八頭借哪；鳥員西爪得要意點師停故嗎昔花。巾至您采告門高貝完來爪書，巴爪哭青幸植吃對乾千。";
                    courseName.className = 'lead fw-bold mx-2 text-wrap';
                    courseName.style.fontSize = 'clamp(1rem, 2.5vw, 1.25rem)'; courseName.textContent = course.course_name;
                    div.appendChild(courseName);

                    const button = document.createElement('button');
                    button.className = 'btn btn-secondary ms-auto me-3';
                    button.type = 'button';
                    button.setAttribute('data-bs-toggle', 'collapse');
                    button.setAttribute('data-bs-target', `#collapse${course.course_id}`);
                    button.setAttribute('aria-expanded', 'false');
                    button.setAttribute('aria-controls', `collapse${course.course_id}`);
                    button.innerHTML = '<span class="d-none d-md-inline">詳細資訊</span><i class="d-md-none bi bi-chevron-down"></i>';
                    button.addEventListener('click', function() {
                        const icon = button.querySelector('i');
                        if (icon.classList.contains('bi-chevron-down')) {
                            icon.classList.remove('bi-chevron-down');
                            icon.classList.add('bi-chevron-up');
                        } else {
                            icon.classList.remove('bi-chevron-up');
                            icon.classList.add('bi-chevron-down');
                        }
                    });
                    div.appendChild(button);

                    listItem.appendChild(div);

                    const collapse = document.createElement('div');
                    collapse.className = 'collapse';
                    collapse.id = `collapse${course.course_id}`;

                    const cardBody = document.createElement('div');
                    cardBody.className = 'bg-light bg-gradient card card-body border-0 d-flex flex-row align-items-start justify-content-between mt-1';

                    const courseInfo = document.createElement('div');
                    courseInfo.className = 'info';
                    courseInfo.textContent = course.course_info ?? noCourseInfo;
                    cardBody.appendChild(courseInfo);

                    const teacherImages = document.createElement('div');
                    teacherImages.className = 'ms-4 text-end';
                    teacherImages.style.width = '180px';
                    course.teachers.forEach(teacher => {
                        const img = document.createElement('img');
                        img.src = `/media/DBzip/pfp/${teacher}.jpg`; // 志工頭貼
                        img.className = 'rounded-circle profile ms-1';
                        img.alt = '';
                        teacherImages.appendChild(img);
                    });
                    cardBody.appendChild(teacherImages);

                    collapse.appendChild(cardBody);
                    listItem.appendChild(collapse);

                    listGroup.appendChild(listItem);
                });

                tabPane.appendChild(listGroup);
                sectionTabContent.appendChild(tabPane);
            });
        });

        // Form validation
        const form = document.getElementById('priorityForm');
        form.addEventListener('submit', function(event) {
            const errorMessage = document.getElementById('error-message');
            const selects = document.querySelectorAll('select[name="priority"]');
            const priorities = {};
    
            for (const select of selects) {
                const value = select.value;
                // console.log(value);
                if (!value || value === '選擇志願') {
                    errorMessage.textContent = '請確認所有課程都有填寫志願！';
                    // console.log('請確認所有課程都有填寫志願！');
                    event.preventDefault();
                    return;
                }
                const [priority, course_id, std_id, section_id] = value.split('-');
                if (!priorities[section_id]) {
                    priorities[section_id] = {};
                }
                if (priorities[section_id][priority]) {
                    errorMessage.textContent = '同一節內志願序不得重複！（第'+section_id+'節）';
                    // console.log('志願序不得重複！');
                    event.preventDefault();
                    return;
                }
                priorities[section_id][priority] = true;
            }
 
            // Clear error message if validation passes
            errorMessage.textContent = '';
            

        });

});
