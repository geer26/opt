function adm_post_adduser(){

    var username = $('#username').val();
    var description = $('#description').val();
    var contact = $('#contact').val();
    var pw1 = $('#password1').val();
    var pw2 = $('#password2').val();
    var is_superuser = $('#is_superuser').is(':checked');
    var data_to_check = {event:2201, username:username, pw1:pw1, description:description, contact:contact, is_superuser:is_superuser};

    //perform initial checks

    //check all neccessary filled
    if(!username || !pw1 || !pw2){
        $('#credits').addClass('credits_error');
        $('#error').text('Hiányos kötelező mezők!!');
        $('#error').show();
        return;
    };

    //check password policy
    //regex values
    var reg_strlo = /[abcdefghijklmnopqrstuvwxyz]+/;
    var reg_strhi = /[ABCDEFGHIJKLMNOPQRSTUVWXYZ]+/;
    var reg_num = /[0-9]+/;
    var reg_strspec = /[!@#$%^&*?_~]+/;

    if(
            pw1.length < 8 ||
            !reg_strlo.test(pw1) ||
            !reg_strhi.test(pw1) ||
            !reg_num.test(pw1) ||
            !reg_strspec.test(pw1)
        ){
            $('#credits').addClass('credits_error');
            $('#error').text('A jelszó nem elég erős!');
            $('#error').show();
            $('#password1').val('');
            $('#password2').val('');
            return;
        };

    //compare the two passwords
    if (pw1 != pw2){
        $('#credits').addClass('credits_error');
        $('#error').text('A két jelszó nem egyezik!');
        $('#error').show();
        $('#password1').val('');
        $('#password2').val('');
        return;
    };

    //if everything is ok, send a test
    loadstart();
    send_message(data_to_check, 'admin');

};


function del_user(userid){
    loadstart();
    send_message({event: 2251, userid: parseInt(userid)}, 'admin');
};


//admin websocket event dispatcher
socket.on('admin', function(data){

    switch (data['event']){

         //accept creditentials status
         case 1201:{
                loadend();
                if (data['status'] == 1){
                    $('#credits').addClass('credits_error');
                    $('#error').text('A felhasználónév már létezik!');
                    $('#error').show();
                    $('#password1').val('');
                    $('#password2').val('');
                }
                if (data['status'] == 2){
                    $('#credits').addClass('credits_error');
                    $('#error').text('A jelszó nem elég erős!');
                    $('#error').show();
                    $('#password1').val('');
                    $('#password2').val('');
                }
                if (data['status'] == 0){
                    $('#username').val('');
                    $('#description').val('');
                    $('#contact').val('');
                    $('#password1').val('');
                    $('#password2').val('');
                    $('#is_superuser').prop( "checked", false );
                    $('#adduser_modal').hide();
                    //refresh page!
                }
            };
            break;

         case 1251:{
            loadend();
            if (data['status'] == 0){
                //refresh page!
            }
            };
            break;

    }

});

