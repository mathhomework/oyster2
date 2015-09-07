(function(){

$(document).ready(function(){
    //textFit(document.getElementById('label-wrapper'));
    //$('body').flowtype({
    //    fontRatio: 30
    //});
    //$('#label-wrapper').fitText(1.4);
    var label_text = $('.label-wrapper label').data('label');
    console.log(label_text);
    $('.label-wrapper label').typed({
        strings: [label_text],
        typeSpeed: 11
    });
    //$('#label-wrapper').fitText(1.4);
    $(window).resize(function(){
        document.body.style.overflow = "hidden";
        var window_height = $(window).height();
        var rest  = $('.top-bar').outerHeight(true) + $('label-wrapper').outerHeight(true);
        var ta_height = $('textarea').outerHeight(true);
        console.log("window hieght" + window_height);
        console.log("rest" + rest);
        console.log("tah" + ta_height);
        $('textarea').css('height', window_height-rest);
        if(window_height-rest < ta_height){
            $('textarea').css('height', window_height-rest);
        }
        //document.body.style.overflow = "";

    });
});

})();