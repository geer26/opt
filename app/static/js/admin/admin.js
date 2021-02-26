
const app = Vue.createApp({
    delimiters: ["{@", "@}"],

	data() {
		return {
			users: admin_data['users']
		}
	},

	methods: {
		handleSelectionChanged(payload) {
			if ( payload == null ) {
				console.log("Nincs kijelölve semmi");
			} else {
				console.log("Kiválasztott felhasználó: " + payload.username);
			}
	    },

	    handleDeleteRecord(payload) {
            //if ok send via ws
            data = {event: 2251, id: payload.id};
            send_message(data, namespace='admin');
            loadstart();
	    },

	    showAddUser() {
	        $('#adduser_modal').show();
	        $('#username').val('');
	        $('#description').val('');
	        $('#contact').val('');
	        $('#password1').val('');
	        $('#password2').val('');
	        $('#is_superuser').prop( "checked", false );
	        inputkeypress();
	    }
	}

	});


app.component("table-component", TableComponent);


const vm = app.mount("#tab-users")


function inputkeypress(){
    $('#error').hide();
    $('#adduser').removeClass('credits_error');
};


function adm_post_adduser(){

    //get values
    var username = $('#username').val();
	var description = $('#description').val();
	var contact = $('#contact').val();
	var pw1 = $('#password1').val();
	var pw2 = $('#password2').val();
	var is_superuser = $('#is_superuser').is(":checked");

    //check if the required are filled
    if (!username || !pw1 || !pw2){
        $('#error').text('Hiányos kötelező mezők!');
        $('#error').show();
        $('#adduser').addClass('credits_error');
        $('#password1').val('');
	    $('#password2').val('');
        return;
    }

    //check password complexity
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
        $('#error').text('A jelszó túl gyenge!');
        $('#error').show();
        $('#adduser').addClass('credits_error');
        $('#password1').val('');
	    $('#password2').val('');
        return;
    }


    //check pw1 and pw2 equality
    if (pw1 != pw2){
        $('#error').text('A jelszavak nem egyeznek!');
        $('#error').show();
        $('#adduser').addClass('credits_error');
        $('#password1').val('');
	    $('#password2').val('');
        return;
    }

    //if ok send via ws
    data = {event: 2201, username: username, description: description, contact: contact, password: pw1, is_superuser: is_superuser};
    send_message(data, namespace='admin');
    loadstart();
};


function hide_adduser_modal(){
    $('#adduser_modal').show();
    $('#username').val('');
	$('#description').val('');
	$('#contact').val('');
	$('#password1').val('');
	$('#password2').val('');
	$('#is_superuser').prop( "checked", false );
	$('#adduser_modal').hide();
}


//Websockets admin event dispatcher
socket.on('admin', function(data){

    switch (data['event']){

        //accept adduser status
        case 1201:{
            loadend();

            if (data['status'] == 0){
                var new_users = JSON.parse(data['new_users']);
                while (admin_data.users.length > 0) {
                    admin_data.users.pop();
                }
                new_users.forEach(item => admin_data.users.push(item));
                hide_adduser_modal();
            }

            else if (data['status'] == 1){
                //user exists
                $('#error').text('Válasszon másik felhasználónevet!');
                $('#error').show();
                $('#adduser').addClass('credits_error');
                $('#password1').val('');
	            $('#password2').val('');
            }

            else if (data['status'] == 2){
                //weak password
                $('#error').text('A jelszó túl gyenge!');
                $('#error').show();
                $('#adduser').addClass('credits_error');
                $('#password1').val('');
	            $('#password2').val('');
            }

        }
        break;

        case 1251:{
            loadend();
            var new_users = JSON.parse(data['new_users']);
            while (admin_data.users.length > 0) {
                admin_data.users.pop();
            }
            new_users.forEach(item => admin_data.users.push(item));
        }
        break;
    }

});
