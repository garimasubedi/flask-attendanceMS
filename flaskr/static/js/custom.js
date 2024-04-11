$(document).ready(function() {
    let AttendanceID = 0;
    let $validator = $('#form1').validate({
        errorElement: 'div', // Change the error element to a div
        errorClass: 'invalid-feedback', // Bootstrap 4 class for styling error messages
        debug: true,
        rules: {
            slcBatch: { selectcheck: true },
            slcCourse: { selectcheck: true },
            slcSubject: { selectcheck: true },
            slcAttendanceDate: { required: true},


        },
        messages: {
            slcBatch: { selectcheck: "* required" },
            slcCourse: { selectcheck: "* required" },
            slcSubject: { selectcheck: "* required" },
            slcAttendanceDate: { required: "* required" },


        }
    });
    jQuery.validator.addMethod('selectcheck', function (value,e) {
        return (value != '0' && value.length > 0);
    }, "*");

    $('#btnSearch').off('click').on('click',function(){
        if($validator.form()){
            check_attendande()
        }
    });
    $('#slcCourse').off('change').on('change',function(){
        get_subject_ddl();
    });
   
    $('#btnSubmit').off('click').on('click',function(){
        $.confirm({
            title: 'Confirm!',
            content: 'Are you sure want to submit attendance?',
            buttons: {
                confirm: function () {
                    submit_attendance()
                }
            }
        });
    });
    $('#btnCancel').off('click').on('click',function(){
        
        reset_search_form();
    });
    $('#btnPrint').off('click').on('click',function(){
        printDivByID('print-window-table');
    });
    $('#btnSendMail').off('click').on('click',function(){
        let $this = $(this);
        let teacher_mail = 'ashesh@yopmail.com';//$this.attr('data-mail');
        $.confirm({
            title: 'Confirm!',
            content: '' +
                    '<form action="" class="formName" id="sendMailFrom">' +
                    '<div class="form-group">' +
                    '<label>Mail address</label>' +
                    `<input type="email" placeholder="john.doe@gmail.com" id="txtTeacherMail" class="custom-select form-control" value="${teacher_mail}" required />` +
                    '</div>' +
                    '</form>',
            autoClose: 'cancel',
            columnClass: 'medium',
            buttons: {
                sendmail:{
                    text: 'Send Mail',
                    btnClass: 'btn-success',
                    action: function () {
                        let $mailValidator = $('#sendMailFrom').validate({
                            errorElement: 'div', // Change the error element to a div
                            errorClass: 'invalid-feedback', // Bootstrap 4 class for styling error messages
                            debug: true,
                            rules: {
                                slcAttendanceDate: { required: true,mail:true},
                            },
                            messages: {
                                slcAttendanceDate: { required: "* required" },
                            }
                        });
                       
                        if(!$mailValidator.form()){
                            return false;
                        }
                        send_mail();
                        
                    }
                },
                cancel: {
                    btnClass: 'btn-danger',
                    action: function () {
                        
                    }
                },
            }
        });
    });
    function send_mail(){
        $('.ta-loaderwrapper').show();
        var mail = $('#txtTeacherMail').val();
        var attendance_id = $('#btnSendMail').attr('data-id');
        let data = {
            mail:mail,
            attendance_id:attendance_id
        }
        $.ajax({
            url: '/attendance/send-mail',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: send_mail_response,
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    }
    function send_mail_response(data){
        console.log(data);
        if(data != null){
            $('.ta-loaderwrapper').hide();
            if(data.statuscode == 1){
                $.confirm({
                    title: 'Mail Sent!',
                    content: data.message,
                    type: 'green',
                    typeAnimated: true,
                    buttons: {
                        close: function () {
                        }
                    }
                });
            }else{
                $.confirm({
                    title: 'Encountered an error!',
                    content: 'Something went downhill, this may be serious',
                    type: 'red',
                    typeAnimated: true,
                    buttons: {
                        tryAgain: {
                            text: 'Try again',
                            btnClass: 'btn-red',
                            action: function(){
                                $('#btnSendMail').trigger('click');
                            }
                        },
                        close: function () {
                        }
                    }
                });
            }
            
        }
       
    }
    function reset_search_form(){
        $('#slcBatch').val('0');
        $('#slcCourse').val('0');
        $('#slcSubject').val('0');
        $('#slcAttendanceDate').val('');
        $('.tbl-student-list').hide();
        disable_search(false);

    }
    function submit_attendance(){
        var batch_id = $('#slcBatch option:selected').val();
        var course_id = $('#slcCourse option:selected').val();
        var subject_id = $('#slcSubject option:selected').val();
        var attendance_date = $('#slcAttendanceDate').val();
        let students = []
        $('.student-cb').each(function(index,item){
            let $this = $(this);
            let id = $this.attr('data-id');
            let status = $this.prop('checked')?1:0;
            let obj = {id:id,status:status}
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
            url: '/attendance/submitattendance',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: submit_attendance_response,
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });

    }
    function submit_attendance_response(data){
        if (data != null){
            if(data.statuscode == 1 || data.statuscode == 2){
            
                $.confirm({
                    title: 'Awesome!',
                    content: data.message,
                    autoClose: 'cancel|15000',
                    columnClass: 'medium',
                    buttons: {
                        gotoattendancesheet:{
                            text: 'Go to attendance sheet',
                            btnClass: 'btn-success',
                            action: function () {
                                window.location.href = `/attendance/${data.data}/list`;
                            }
                        },
                        cancel: {
                            btnClass: 'btn-danger',
                            action: function () {
                                reset_search_form()
                            }
                        },
                    }
                });
            }else{

            }
        }

    }
     function get_subject_ddl(){
        var course_id = $('#slcCourse option:selected').val();
        $.ajax({
            url: '/attendance/get_subject_ddl',
            type: 'GET',
            data: {
                course_id: course_id
            },
            success: get_subject_ddl_response,
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    }
    function get_subject_ddl_response(data){
        console.log(data);
        if(data != null){
            let html = '<option value="0" selected>Choose subject...</option>';
           $.each(data,function(index,item){
            html += `<option value="${item.id}">${item.subject_name}</option>`;

           });
           $('#slcSubject').html(html);
        }
       
    }
    function get_students(){
        var batch_id = $('#slcBatch option:selected').val();
        var course_id = $('#slcCourse option:selected').val();
        var subject_id = $('#slcSubject option:selected').val();
        var attendance_date = $('#slcAttendanceDate').val();
        $.ajax({
            url: '/attendance/getstudents',
            type: 'GET',
            data: {
                batch_id: batch_id,
                course_id: course_id,
                subject_id: subject_id,
                attendance_date: attendance_date,
            },
            success: get_students_response,
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    }
    function get_students_response(data){
        console.log(data);
        if(data != null){
            let html = '';
           $.each(data,function(index,item){
            html += `<tr>
                    <td>${item.id}</td>
                    <td>${item.first_name} ${item.last_name}</td>
                    <td>
                    <div class="form-group">
                        <div class="form-check">
                        <input class="form-check-input student-cb" data-id="${item.id}" type="checkbox" value="" id="cbPresent-${item.id}" ${(item.status==1)?'checked':''}>
                        <label class="form-check-label" for="cbPresent-${item.id}">
                            Present?
                        </label>
                        </div>
                    </div>
                    </td>

                    </tr>`;

           });
           $('#div_student_list').html(html);
           
            $('.tbl-student-list').show();
         
           $('#staticBackdrop').modal('hide');
        }
       
    }
    function disable_search(flag = true){
         $('#slcBatch').prop('disabled',flag?'disabled':flag);
         $('#slcCourse').prop('disabled',flag?'disabled':flag);
         $('#slcSubject').prop('disabled',flag?'disabled':flag);
         $('#slcAttendanceDate').prop('disabled',flag);
         $('#btnSearch').prop('disabled',flag);
    }
    function check_attendande(){
        var batch_id = $('#slcBatch option:selected').val();
        var course_id = $('#slcCourse option:selected').val();
        var subject_id = $('#slcSubject option:selected').val();
        var attendance_date = $('#slcAttendanceDate').val();
        $.ajax({
            url: '/attendance/checkattendance',
            type: 'GET',
            data: {
                batch_id: batch_id,
                course_id: course_id,
                subject_id: subject_id,
                attendance_date: attendance_date,
            },
            success: check_attendande_response,
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    }
    function check_attendande_response(data){
        if(data != null){
            disable_search();
            console.log(data)
            if(data.statuscode == 1){
                $.confirm({
                    title: 'Confirm!',
                    content: data.message,
                    autoClose: 'cancel',
                    columnClass: 'medium',
                    buttons: {
                        takeattendance:{
                            text: 'Yes',
                            btnClass: 'btn-success',
                            action: function () {
                                $.confirm({
                                    title: 'Confirm!',
                                    content: 'Choose attendance taking method!',
                                    autoClose: 'cancel',
                                    columnClass: 'medium',
                                    buttons: {
                                        manual:{
                                            text: 'Manual',
                                            btnClass: 'btn-success',
                                            action: function () {
                
                                                get_students();
                                            }
                                        },
                                        automatic:{
                                            text: 'Automatic',
                                            btnClass: 'btn-success',
                                            action: function () {
                
                                                take_automatic_attendance();
                                            }
                                        },
                                        cancel: {
                                            btnClass: 'btn-danger',
                                            action: function () {
                                                reset_search_form();
                                            }
                                        },
                                    }
                                });
                            }
                        },
                        cancel: {
                            btnClass: 'btn-danger',
                            action: function () {
                                reset_search_form();
                            }
                        },
                    }
                });
            }else{
                $.confirm({
                    title: 'Confirm!',
                    content: data.message,
                    autoClose: 'cancel',
                    columnClass: 'medium',
                    buttons: {
                        takeattendance:{
                            text: 'Yes, get students anyway!',
                            btnClass: 'btn-warning',
                            action: function () {

                                get_students();
                            }
                        },
                        cancel: {
                            btnClass: 'btn-danger',
                            action: function () {
                                reset_search_form();
                            }
                        },
                    }
                });
            }
            
        }
       
    }
    function take_automatic_attendance(){
        window.location.href = `/automatic_attendance/1/1/1/take_attendance`;
    }
    function printDivByID(DivIdToPrint) {

        var divToPrint = document.getElementById(DivIdToPrint);
    
        var newWin = window.open('', 'Print-Window');
    
        newWin.document.open();
    
        newWin.document.write(`
            <!doctype html>
            <html lang="en">

            <head>


                <meta charset="utf-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                <meta name="description" content="">
                <meta name="author" content="">

                <title>Attendance System</title>

                <!-- Custom fonts for this template -->
                <link href="/static/vendor/fontawesome-free/css/all.min.css" rel="stylesheet"
                    type="text/css">
                <link
                    href="https://fonts.googleapis.com/css?family=Nunito:200,200i,300,300i,400,400i,600,600i,700,700i,800,800i,900,900i"
                    rel="stylesheet">

                <!-- Custom styles for this template -->
                <link href="/static/css/sb-admin-2.min.css" rel="stylesheet">
                <link href="/static/css/jquery-confirm.css" rel="stylesheet">

                <!-- Custom styles for this page -->
                <link href="/static/vendor/datatables/dataTables.bootstrap4.min.css" rel="stylesheet">



            </head>

            <body onload='window.print()'>` + divToPrint.innerHTML + `
                    
                </body>
                
                </html>
        `);
    
        newWin.document.close();
    
        setTimeout(function () { newWin.close(); }, 10);
    
    }
  });