

const adminActions = ActionRouter.create({
	debug: false,
	actions: {
		del_user(record) {
		    /*
			let index = vm.konyvek.findIndex(konyv => record.id == konyv.id)
			vm.konyvek.splice(index, 1);
			*/
			send_message({event:2251, id: record.id}, namespace='admin');
            loadstart();
			console.log('DEL USER!');
		}
	}
})


const app = Vue.createApp({
    delimiters: ["{@", "@}"],

	data() {
		return {
			users: admin_data['users'],
			//TODO add all table!
			actionRouter: adminActions
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
	},

	components: {
		advancedTable: AdvancedTable
	}

	});


const vm = app.mount("#tab-users")


var log;


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


function backup_db_all(){
    console.log('BACKUP ENTIRE DB!');
    loadstart();
    send_message({event: 2851}, namespace='admin');
};


function restore_db_all(){
    console.log('RESTORE ENTIRE DB!')
    loadstart();
    send_message({event: 2871}, namespace='admin');
};


function reset_db(){
    console.log('RESET DB!')
    loadstart();
    send_message({event: 2899}, namespace='admin');
};


function change_pwd(){
    console.log('INIT PASSWORD CHANGE!')
    loadstart();
    send_message({event: 2889}, namespace='admin');
};


function showlogcontent(){
    $('#log_content').show();
    $('#hide_log').show();
    $('#refresh_log').show();
    $('#show_log').hide();
    refreshlog();
};


function hidelogcontent(){
    $('#log_content').hide();
    $('#hide_log').hide();
    $('#refresh_log').hide();
    $('#show_log').show();
};


//request for refreshed log file content
function refreshlog(){
    loadstart();
    send_message({event: 2801}, namespace='admin');
};


function refreshlogtable(json){
    $("#tablebody").empty();
    json.forEach(entry => {

        var row = "<tr> <td>"+
        entry['type'].toString()+
        "</td> <td>"+
        entry['datetime'].toString()+
        "</td> <td>"+
        entry['event'].toString()+
        "</td> <td>"+
        entry['executor'].toString()+
        "</td> </tr>";

        $("#tablebody").append(row);

    });
};


//Websockets admin event dispatcher
socket.on('admin', function(data){

    switch (data['event']){

        //accept adduser status
        case 1201:{
            loadend();

            if (data['status'] == 0){
                var new_users = JSON.parse(data['new_users']);
                //2021.02.27. hajnali 09:44 javaslat!
                vm.users = new_users;
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

            else if (data['status'] == 3){
                //to much su
                $('#error').text('Nem lehet több admint regisztrálni!');
                $('#error').show();
                $('#adduser').addClass('credits_error');
                $('#password1').val('');
	            $('#password2').val('');
            }

        }
        break;

        //accept deluser status
        case 1251:{
            loadend();
            var new_users = JSON.parse(data['new_users']);
            //2021.02.27. hajnali 09:44 javaslat!
            vm.users = new_users;
            while (admin_data.users.length > 0) {
                admin_data.users.pop();
            }
            new_users.forEach(item => admin_data.users.push(item));
        }
        break;

        //accept backup entire db status
        case 1851:{
            loadend();
            if (data['status'] == 0){
                console.log('ENTIRE DB SAVED!');
            }
        }
        break;

        //accept refreshed log content as json
        case 1801:{
            loadend();
            console.log('INCOMING LOG UPDATE!');
            refreshlogtable(JSON.parse(data['data']));
        }
        break;

        //accept restore entire db status
        case 1871:{
            loadend();
            if (data['status'] == 0){
                console.log('ENTIRE DB RESTORED!');
                //TODO refresh all vm data!
            }
        }
        break;

        //accept password change status report
        case 1889:{
            loadend();
            if (data['status'] == 0){
                console.log('PASSWORD CHANGED!');
            }
        }
        break;

        //accept reset_db status
        case 1899:{
            loadend();
            if (data['status'] == 0){
                console.log('ENTIRE DB RESET!');
                //TODO refresh all vm data!
            }
        }
        break;

    }

});
