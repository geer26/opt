socket = io();


function inputkeypress(){
    $('#error').hide();
    $('#credits').removeClass('credits_error');
};


//generic websocket event dispatcher
socket.on('generic', function(data){

    switch (data['event']){

         //accept creditentials status
         case 1109:{
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