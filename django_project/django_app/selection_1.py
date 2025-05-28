def process_selection_results(request): # 處理志願結果
    if request.method == 'POST':
        processing_stage = request.POST['processing_stage']
        # 從按鈕判斷處理第一階或第二階選課
        if processing_stage == '1':
            sections = Section.objects.filter(section_id__lte=AdminSetting.objects.get(setting_name='J1stRange').configuration) # 1~6
        elif processing_stage == '2': 
            sections = Section.objects.filter(section_id__gt=AdminSetting.objects.get(setting_name='J1stRange').configuration) # 7~12
        for section in sections:
            print(f"Processing section {section.section_id}")
            assigned_students = set()
        for section in sections:
            print(f"Processing section {section.section_id}")
            assigned_students = set()  # 追蹤已經被分配的學生
            unassigned_students = set(Selection.objects.filter(section=section).values_list('std_id', flat=True))            
            vacancy = {}  # 追蹤每個課程的缺額

            courses_in_section = list(Course.objects.filter(section_id=section.section_id))
            special_courses_in_section = list(SpecialCourse.objects.filter(section_id=section.section_id))
            all_courses_in_section = courses_in_section + special_courses_in_section

            # 優先排序連堂的第二堂課
            all_courses_in_section.sort(key=lambda x: (x.course_type != 'NA', x.course_type != 'H', x.course_id))

            # 光仁學生先全部指定到手語課
            SL_courses = [c for c in all_courses_in_section if '手語課' in c.course_name]
            sl_selections = []
            for course in SL_courses: 
                for gr_student in Student.objects.filter(std_tag='gr'):
                    if gr_student.std_id in assigned_students:
                        print(f"Student {gr_student.std_id} already assigned, skipping.")
                        continue
                    sl_selections.append(SelectionResult(
                        std=gr_student,
                        content_type=ContentType.objects.get_for_model(course),
                        object_id=course.course_id,
                        section=section,
                        form_type='NA'
                    ))
                    assigned_students.add(gr_student.std_id)
                    unassigned_students.remove(gr_student.std_id)
            SelectionResult.objects.bulk_create(sl_selections)

            # 優先處理連堂的第二堂課
            na_selections = []
            for course in all_courses_in_section:
                if course.course_type == 'NA':
                    previous_course_id = course.course_id - 1
                    previous_course = Course.objects.get(course_id=previous_course_id)
                    previous_selections = previous_course.selection_results.all()

                    for selection in previous_selections:
                        if selection.std.std_id in unassigned_students:
                            na_selections.append(SelectionResult(
                                std=selection.std,
                                content_type=ContentType.objects.get_for_model(course),
                                object_id=course.course_id,
                                section=section,
                                form_type=selection.form_type
                            ))
                            assigned_students.add(selection.std.std_id)
                            unassigned_students.remove(selection.std.std_id)
            SelectionResult.objects.bulk_create(na_selections)

            # 處理完連堂後處理高中限定課程
            for priority in range(1, 6): 
                for course in [c for c in all_courses_in_section if c.course_type == 'H']:
                    if course.course_id not in vacancy:
                        vacancy[course.course_id] = course.std_limit
                    selections = Selection.objects.filter(
                        section=section,
                        course_id=course.course_id,
                        priority=priority
                    )

                    available_selections = [s for s in selections if s.std.std_id in unassigned_students]

                    if len(available_selections) <= vacancy[course.course_id]:
                        h_selections = []
                        for selection in available_selections:
                            if selection.std.std_id in assigned_students:
                                print(f"Student {selection.std.std_id} already assigned, skipping.")
                                continue
                            h_selections.append(SelectionResult(
                                std=selection.std,
                                content_type=ContentType.objects.get_for_model(course),
                                object_id=course.course_id,
                                section=section,
                                form_type=selection.form_type
                            ))
                            assigned_students.add(selection.std.std_id)
                            unassigned_students.remove(selection.std.std_id)
                            vacancy[course.course_id] -= 1
                        SelectionResult.objects.bulk_create(h_selections)
                    else:
                        selected_students = random.sample(available_selections, vacancy[course.course_id])
                        h_selections = []
                        for selection in selected_students:
                            if selection.std.std_id in assigned_students:
                                print(f"Student {selection.std.std_id} already assigned, skipping.")
                                continue
                            h_selections.append(SelectionResult(
                                std=selection.std,
                                content_type=ContentType.objects.get_for_model(course),
                                object_id=course.course_id,
                                section=section,
                                form_type=selection.form_type
                            ))
                            assigned_students.add(selection.std.std_id)
                            unassigned_students.remove(selection.std.std_id)
                        SelectionResult.objects.bulk_create(h_selections)
                        vacancy[course.course_id] = 0
                
            while unassigned_students:
                student = random.choice(list(unassigned_students))
                if not Selection.objects.filter(section=section, std_id=student).exists():
                    unassigned_students.remove(student)
                    continue
                for priority in range(1, 6): 
                    selection = Selection.objects.filter(std=student, priority=priority, section=section).first()
                    if selection:
                        course_id = selection.course_id
                        try:
                            course = Course.objects.get(course_id=course_id)
                        except Course.DoesNotExist:
                            course = SpecialCourse.objects.get(course_id=course_id)
                        if '手語課' in course.course_name and '二' in course.course_name and priority in [3, 4, 5, 6]:
                            continue
                        if course_id not in vacancy:
                            vacancy[course_id] = course.std_limit
                        if vacancy[course_id] > 0:
                            if student in assigned_students:
                                print(f"Student {student} already assigned, skipping.")
                                continue
                            SelectionResult.objects.create(
                                std=selection.std,
                                content_type=ContentType.objects.get_for_model(course),
                                object_id=course_id,
                                section=section,
                                form_type=selection.form_type
                            )
                            assigned_students.add(student)
                            vacancy[course_id] -= 1
                            unassigned_students.remove(student)
                            break

            # Debugging: Check for unassigned students
            all_students = set(Selection.objects.filter(section=section).values_list('std_id', flat=True))
            unassigned_students = all_students - assigned_students
            if unassigned_students:
                print(f"Unassigned students in section {section.section_id}: {unassigned_students}")
            
        messages.success(request, '選課結果已處理完成')
        return redirect('result')
    return redirect('result')