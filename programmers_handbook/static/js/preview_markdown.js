$(document).ready(function() {
    var timer;
    $('textarea#id_text').on('keyup', function(event) {
        clearTimeout(timer);
        timer = setTimeout(function() {
            $.post('/page_preview/', { text: $(event.target).val() }, function(data) {
                $('#preview').html(data);
            });
        }, 1 * 1000);
    }).trigger('keyup');
});
