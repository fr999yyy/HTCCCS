
document.addEventListener('DOMContentLoaded', function() {
    const stdId = '{{ student.std_id }}';  // Assuming std_id is available in the template context
    fetch(`/get_courses/?std_id=${stdId}`)
        .then(response => response.json())
        .then(data => {
            const sectionsWithCourses = data.sections_with_courses;
            const sectionTab = document.getElementById('sectionTab');
            const sectionTabContent = document.getElementById('section-tabContent');

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

                section.courses.forEach(course => {
                    const listItem = document.createElement('li');
                    listItem.className = 'list-group-item';

                    const div = document.createElement('div');
                    div.className = 'd-flex align-items-center';

                    const select = document.createElement('select');
                    select.className = 'form-select form-select-sm text-center';
                    select.style.width = 'auto';
                    const option = document.createElement('option');
                    option.selected = true;
                    option.textContent = '選擇志願';
                    select.appendChild(option);
                    for (let i = 1; i <= section.num_courses.length; i++) {
                        const option = document.createElement('option');
                        option.value = i;
                        option.textContent = i;
                        select.appendChild(option);
                    }
                    div.appendChild(select);

                    const courseName = document.createElement('div');
                    courseName.className = 'lead fw-bold mx-2';
                    courseName.textContent = course.course_name;
                    div.appendChild(courseName);

                    const button = document.createElement('button');
                    button.className = 'btn btn-secondary ms-auto me-3';
                    button.type = 'button';
                    button.setAttribute('data-bs-toggle', 'collapse');
                    button.setAttribute('data-bs-target', `#collapse${course.course_id}`);
                    button.setAttribute('aria-expanded', 'false');
                    button.setAttribute('aria-controls', `collapse${course.course_id}`);
                    button.textContent = '詳細資訊';
                    div.appendChild(button);

                    listItem.appendChild(div);

                    const collapse = document.createElement('div');
                    collapse.className = 'collapse';
                    collapse.id = `collapse${course.course_id}`;

                    const cardBody = document.createElement('div');
                    cardBody.className = 'bg-light bg-gradient card card-body border-0 d-flex flex-row align-items-start justify-content-between mt-1';

                    const courseInfo = document.createElement('div');
                    courseInfo.className = 'info';
                    courseInfo.textContent = course.course_info;
                    cardBody.appendChild(courseInfo);

                    const teacherImages = document.createElement('div');
                    teacherImages.className = 'ms-4 text-end';
                    teacherImages.style.width = '180px';
                    course.teachers.forEach(teacher => {
                        const img = document.createElement('img');
                        img.src = `media/pfp/${teacher}.jpg`;
                        img.className = 'rounded-circle profile mx-3';
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
});
