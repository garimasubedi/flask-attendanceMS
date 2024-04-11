
(function () {
    $.AutoAttendanceManageObj = function () {

        var AutoAttendanceManage = {

            init: function () {
                AutoAttendanceManage.InitUIEvents();
            },

            InitUIEvents: function () {
                $("#start_stream").click(function () {
                    let $this = $(this);
                    $.confirm({
                        title: 'Confirm!',
                        content: 'Are you sure want to take attendance?',
                        type: 'yellow',
                        typeAnimated: true,
                        buttons: {
                            yes: {
                                text: 'Yes',
                                btnClass: 'btn-success',
                                action: function () {
                                    $("#video_feed").attr("src", video_feed_url);
                                    $this.hide();
                                    $("#stop_stream").show();
                                }
                            },
                            close: {
                                text: 'Cancel',
                                btnClass: 'btn-danger',
                                action: function () {

                                }
                            }
                        }
                    });

                });

                $("#stop_stream").click(function () {

                    let $this = $(this);
                    $.confirm({
                        title: 'Confirm!',
                        content: 'Are you sure want to stop take attendance?',
                        type: 'red',
                        typeAnimated: true,
                        buttons: {
                            yes: {
                                text: 'Yes',
                                btnClass: 'btn-success',
                                action: function () {
                                    $("#video_feed").attr("src", no_video_url);
                                    AutoAttendanceManage.GetStudent();
                                    AutoAttendanceManage.ToggleForms('list');
                                }
                            },
                            close: {
                                text: 'Cancel',
                                btnClass: 'btn-danger',
                                action: function () {

                                }
                            }
                        }
                    });
                });
                $('#btnCancel').off('click').on('click',function(){
                    $("#start_stream").show();
                    $("#stop_stream").hide();
                    AutoAttendanceManage.ToggleForms();
                });
                $('#btnSubmit').off('click').on('click',function(){
                    $.confirm({
                        title: 'Confirm!',
                        content: 'Are you sure want to submit attendance?',
                        buttons: {
                            confirm: function () {
                                AutoAttendanceManage.SubmitAttendance();
                            }
                        }
                    });
                   

                });
            },
            SubmitAttendance: function () {
                var batch_id = $('#slcBatch option:selected').val();
                var course_id = $('#slcCourse option:selected').val();
                var subject_id = $('#slcSubject option:selected').val();
                var attendance_date = $('#slcAttendanceDate').val();
                let students = []
                $('.student-cb').each(function (index, item) {
                    let $this = $(this);
                    let id = $this.attr('data-id');
                    let status = $this.prop('checked') ? 1 : 0;
                    let obj = { id: id, status: status }
                    students.push(obj);

                });
                let data = {
                    batch_id: batch_id,
                    course_id: course_id,
                    subject_id: subject_id,
                    attendance_date: attendance_date,
                    studentdata: students
                };
                $.ajax({
                    url: '/automatic_attendance/submitattendance',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify(data),
                    success: AutoAttendanceManage.SubmitAttendanceResponse,
                    error: function (xhr, status, error) {
                        console.error('Error:', error);
                    }
                });
            },
            SubmitAttendanceResponse: function (data) {
                if (data != null) {
                    if (data.statuscode == 1 || data.statuscode == 2) {

                        $.confirm({
                            title: 'Awesome!',
                            content: data.message,
                            autoClose: 'cancel|15000',
                            columnClass: 'medium',
                            buttons: {
                                gotoattendancesheet: {
                                    text: 'Go to attendance sheet',
                                    btnClass: 'btn-success',
                                    action: function () {
                                        window.location.href = `/attendance/${data.data}/list`;
                                    }
                                },
                                cancel: {
                                    btnClass: 'btn-danger',
                                    action: function () {
                                        window.location.href = `/attendance/takeattendance`;
                                    }
                                },
                            }
                        });
                    } else {

                    }
                }
            },

            GetStudent: function () {
                $.ajax({
                    url: '/automatic_attendance/stop_taking_attendance',
                    type: 'GET',
                    data: {},
                    success: AutoAttendanceManage.GetStudentResponse,
                    error: function (xhr, status, error) {
                        console.error('Error:', error);
                    }
                });
            },
            GetStudentResponse: function (data) {
                if (data != null) {
                    console.log(data)
                    let students = data.students;
                    let batchs = data.batch;
                    let courses = data.course;
                    let date = data.date;
                    let subjects = data.subject;
                    if (batchs.length > 0) {
                        let html = '';
                        $.each(batchs, function (index, item) {
                            html += `<option value="${item.id}" selected>${item.batch_year}-${item.batch_name}</option>`;

                        });
                        $('#slcBatch').html(html).prop('disabled', true);
                    }
                    if (courses.length > 0) {
                        let html = '';
                        $.each(courses, function (index, item) {
                            html += `<option value="${item.id}" selected>${item.course_name}</option>`;

                        });
                        $('#slcCourse').html(html).prop('disabled', true);
                    }
                    if (subjects.length > 0) {
                        let html = '';
                        $.each(subjects, function (index, item) {
                            html += `<option value="${item.id}" selected>${item.subject_name}</option>`;

                        });
                        $('#slcSubject').html(html).prop('disabled', true);
                    }
                    $('#slcAttendanceDate').val(date);
                    if (students.length > 0) {
                        let html = '';
                        $.each(students, function (index, item) {
                            let snapshot = '/static/img/images.png';
                            let checked = '';
                            if (item.status == 'present') {
                                snapshot = `/automatic_attendance/images/${item.id}/${item.confidence}`;
                                checked = 'checked';
                            }

                            html += ` <tr>
                                            <td>${item.id}</td>
                                            <td><img src="${snapshot}" height=80 width=80 alt="..." class="img-thumbnail" heigh></td>
                                            <td>${item.first_name} ${item.last_name}</td>
                                            <td>${item.status}</td>
                                            <td>${item.confidence}%</td>
                                            <td>
                                            <div class="form-group">
                                                <div class="form-check">
                                                <input class="form-check-input student-cb" data-id="${item.id}" type="checkbox" value="" id="cbPresent-${item.id}" ${checked}>
                                                <label class="form-check-label" for="cbPresent-${item.id}">
                                                    Present?
                                                </label>
                                                </div>
                                            </div>
                                            </td>
                                        </tr>`
                        });
                        $('#div_student_list').html(html);
                    }
                }
            },

            ToggleForms: function (type = 'preview') {
                $('.camera-preview').hide();
                $('.attendance-list').hide();
                switch (type) {
                    case 'preview': $('.camera-preview').show(); break;
                    case 'list': $('.attendance-list').show(); break;
                    default: break;
                }
            },
        }
        AutoAttendanceManage.init();
    }

    $.fn.AutoAttendanceManageFn = function () {
        $.AutoAttendanceManageObj();
    }
}(jQuery))