// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable();
  $('#studet_dataTable').DataTable();
  $('#studet_dataTable1').DataTable({searching: false, paging: false, info: false});
  //$('#studet_attendance_datatable').DataTable({searching: false,paging: false, info: false,});
  
});
