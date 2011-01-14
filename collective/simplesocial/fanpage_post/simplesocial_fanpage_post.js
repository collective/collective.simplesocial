(function($){
  $(function() {
    if (!(SimpleSocial.settings.page_id && SimpleSocial.settings.post_to_page_available)) return;
      
    var docac = $('.documentActions ul');
    if (!docac.length) {
        docac = $('<ul></ul>').appendTo('.documentActions');
    }
    
    $('<li><a href="#">Post to Fan Page</a></li>')
        .click(function(e) {
            e.preventDefault();
            $.getJSON(window.location.href + '/@@simplesocial_attachment', null, function(attachment) {
                 SimpleSocial.queue.push(function () {
                     FB.getLoginStatus(function(response) {
                         if (response.session) {
                             SimpleSocial.publishToPage(attachment);
                         } else {
                             FB.login(function (response) {
                                 SimpleSocial.publishToPage(attachment);
                             });
                         }
                     });
                 });
            });
        })
        .appendTo(docac);
  });
})(jQuery);
