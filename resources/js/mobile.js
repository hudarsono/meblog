$(document).ready(function() {

  if ((screen.width<=960) && (screen.height<=640)) {

    $("img").attr("src", $("img").attr("src").replace(/([^.]*)\.(.*)/, "$1-iphone.$2"));

  }

});


function show_more(){
    $('li').show();
    $('#paging').show();
    $('li#divider').hide();
}
