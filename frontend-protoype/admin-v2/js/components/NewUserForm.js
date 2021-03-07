// Új felhasználó adatainak beivetlére szolgáló űrlap
/*
FORM.form-basic
*/

const NewUserForm = {
	delimiters: ["{@", "@}"],

	template: `
	<form class="form-basic" @input="this.$emit('changed')">
		<div>Felhasználónév: <input name="username" type="text" v-model="formData.username"/></div>
		<div>Leírás: <input name="description" type="text" v-model="formData.description"/></div>
		<div>Kontakt: <input name="contact" type="text" v-model="formData.contact"/></div>
		<div>Jelszó: <input name="password" type="password" v-model="formData.password"/></div>
		<div>Jelszó újra: <input name="password_again" type="password" v-model="formData.password_again"/></div>
	</form>
	`,

	data() {
		return {
			formData: {
				username: "",
				description: "",
				contact: "",
				password: "",
				password_again: ""
			}
		}
	},

	props: ["data"],

	methods: {
		get() {
			return this.formData;
		},

		set(data) {
			this.formData = {
				username: data.username,
				description: data.description,
				contact: data.contact,
				password: data.password,
				password_again: data.password
			};
		},

		// Űrlap adatainak kitörlése
		reset() {
			this.formData = {
				userame: "",
				description: "",
				contact: "",
				password: "",
				password_again: ""
			}
		},

		validate() {
			// Jelszavak összehasonlítása, stb.
			return true;
		}
	}


};
