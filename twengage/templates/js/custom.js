// Table Initialization
$(document).ready(function() {
    var defaultURL = $('#defaultURL').attr('href');

    $('#accounts-table').DataTable({
        "lengthMenu": [[150, 200, -1], [150, 200, "All"]],
        "language": {
            "search": "Filter results:",
            "lengthMenu": "Show Entries _MENU_"
          }
    });

    $('.activeStatus').each(function(index ,instance){
        var isActive = $(this).parent().siblings('td:eq(7)').html();
        $(this).prop('checked', isActive == "True");

    });
    $('.activeStatus').change(function(){
        var userActive = $(this).parent().siblings('td:eq(7)');

        if($(this).prop("checked")) {
            userActive.html("True");
            var updateURL = defaultURL + 'userActiveChange/' + $(this).attr('id') + '/True/';
           $.ajax({url: updateURL, success: function(result){
            }});
        }
        else {
            userActive.html("False");
            var updateURL = defaultURL + 'userActiveChange/' + $(this).attr('id') + '/False/';

             $.ajax({url: updateURL, success: function(result){
            }});

        }
    });
    $('#checkall').change(function(){
       $('.activeStatus').prop('checked', $(this).prop('checked'));
       $('.activeStatus').each(function(index ,instance){
            var userActive = $(this).parent().siblings('td:eq(7)');
            if($(this).prop("checked")) {
                userActive.html("True");
                var updateURL = defaultURL + 'userActiveChange/' + $(this).attr('id') + '/True/';
               $.ajax({url: updateURL, success: function(result){
                }});
            }
            else {
                userActive.html("False");
                var updateURL = defaultURL + 'userActiveChange/' + $(this).attr('id') + '/False/';

                 $.ajax({url: updateURL, success: function(result){
                }});
            }

       });
    });
    calculateGrowth();
});

function open_all_stats(){
    $('.username').each(function(i,j){
        username = $(j).text();
        console.log(username);
        url = "http://127.0.0.1:8000/stats/" + username + "/";
        window.open(url, '_blank'); 
        // window.focus();
    })

}


function calculateGrowth(){
    $("#yesterday").append($('#accounts-table .followers').eq(-1).text() - $('#accounts-table .followers').eq(-2).text());
    $("#total").append($('#accounts-table .followers').eq(-1).text() - $('#accounts-table .followers').eq(0).text());
    
}