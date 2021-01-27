var t; var s; var p;

$(document).ready(function(){
    $('.radio').on('click',function(){
        t = $('input[name="radio"]:checked').val();
    });
});
$(document).ready(function(){
    $('.strat').on('click',function(){
        s = $('option:selected').attr('id')
    });
});

$(document).ready(function(){
    $('.period').on('click',function(){
        p = $('.period option:selected').attr('id')
    });
});

// Run the sim
$(document).ready(function(){
    $('.sim').on('click',function(){
        $.ajax({
            url: "/",
            type: "post",
            data: {t: t, s: s, p: p},
            success: function(response) {
                var new_html = response.html;
            },
        });
    });
});
