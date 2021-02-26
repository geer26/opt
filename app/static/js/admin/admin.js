//console.log(admin_data);

const testdata = [
			{id: 1, author: "Shanice Wilkes", title: "Sleeping Fairy", genre: "sci-fi"},
			{id: 2, author: "Laaibah Lane", title: "The Captured Hustler", genre: "crimi"},
			{id: 3, author: "Humaira Kinney", title: "Weeping of Shadow", genre: "drama"},
			{id: 4, author: "Kira Barnett", title: "The Spark's Girl", genre: "crimi"},
			{id: 5, author: "Habiba Sears", title: "The Silk of the Person", genre: "history"},
			{id: 6, author: "Jenna Conroy", title: "Husband in the Stone", genre: "history"},
			{id: 7, author: "Elsa Donald", title: "What Dreams", genre: "sci-fi"},
			{id: 8, author: "Zahid Baker", title: "The Bold Fire", genre: "crimi"},
			{id: 9, author: "Emily-Rose Ortiz", title: "Word of Destiny", genre: "sci-fi"},
			{id: 10, author: "Esme-Rose Benton", title: "The Star's Secret", genre: "sci-fi"},
			{id: 11, author: "Harper-Rose Stanton", title: "The Years of the Sky", genre: "crimi"},
			{id: 12, author: "Abdur-Rahman Bell", title: "Time in the Storm", genre: "history"},
			{id: 13, author: "Kiki Peel", title: "Slithering Wings", genre: "history"},
			{id: 14, author: "Paisley Hope", title: "The Red Emerald", genre: "drama"},
			{id: 15, author: "Aqsa Talbot", title: "Serpent of Danger", genre: "drama"},
			{id: 16, author: "Dione Robertson", title: "The Secret's Return", genre: "history"},
			{id: 17, author: "Kaan Frame", title: "The Soul of the Voyagers", genre: "drama"},
			{id: 18, author: "Blessing Harrington", title: "Boyfriend in the Wizards", genre: "sci-fi"},
			{id: 19, author: "Lemar Edge", title: "Luscious Gift", genre: "romantic"},
			{id: 20, author: "Portia Daniels", title: "The Splintered Sword", genre: "crimi"}
		];


const app = Vue.createApp({
    delimiters: ["{@", "@}"],

	data() {
		return {
			konyvek: testdata,
			users: admin_data['users']
		}
	},

	methods: {
		handleSelectionChanged(payload) {
			if ( payload == null ) {
				console.log("Nincs kijelölve semmi");
			} else {
				console.log("Kiválasztott felhasználó: " + payload.title);
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
    console.log('DATA SENT');
    data = {event: 2201 ,username: username, description: description, contact: contact, password: pw1, is_superuser: is_superuser};
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
                admin_data['users'] = data['new_users'];
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
    }

});
