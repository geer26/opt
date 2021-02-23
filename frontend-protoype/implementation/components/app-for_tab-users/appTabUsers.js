// A tab-users app létrehozása
const appUsers = Vue.createApp({
	delimiters: ["{@", "@}"],

	data() {
		return {
			users: admin_data.users
		}
	},

	computed: {
		usersEnhanced() {
			var e = this.users;
			e.forEach(record => {
				record.role = record.is_superuser ? 'admin' : 'user'
			});
			return e;
		}
	}
});


appUsers.component("table-component", TableComponent);

const vmUsers = appUsers.mount("#tab-users");
