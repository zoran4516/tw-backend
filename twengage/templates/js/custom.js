// Table Initialization
$(document).ready(function() {
    $('#accounts-table').DataTable({
        "lengthMenu": [[150, 200, -1], [150, 200, "All"]],
        "language": {
            "search": "Filter results:",
            "lengthMenu": "Show Entries _MENU_"
          }
    });
    calculateGrowth();
});

function open_all_stats(){
    $('.username').each(function(i,j){
        username = $(j).text();
        console.log(username)
        url = "http://127.0.0.1:8000/stats/" + username + "/";
        window.open(url, '_blank'); 
        // window.focus();
    })

}


function calculateGrowth(){
    $("#yesterday").append($('#accounts-table .followers').eq(-1).text() - $('#accounts-table .followers').eq(-2).text());
    $("#total").append($('#accounts-table .followers').eq(-1).text() - $('#accounts-table .followers').eq(0).text());
    
}