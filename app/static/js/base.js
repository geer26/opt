socket = io();


$(document).ready(function(){

    $('body').on('mousemove', function(e){
        var w = $('#loadanim').width();
        var h = $('#loadanim').height();
        $('#loadanim').offset({ top: e.pageY-h/2, left: e.pageX-w/2 });
    });

});



function loadstart(){
    $('#loadanim').show();
};


//hide loader animation
function loadend(){
    $('#loadanim').hide();
}


function inputkeypress(){
    $('#error').hide();
    $('#credits').removeClass('credits_error');
};


//generic websocket event dispatcher
socket.on('generic', function(data){

    switch (data['event']){

         //accept creditentials status
         case 1109:{
                loadend();
                $('#error').show();
                $('#credits').addClass('credits_error');
                $('#password').val('');
            };
            break;

    }

});


//standardized sender function
function send_message(message, namespace='generic'){
    socket.emit(namespace,message);
};