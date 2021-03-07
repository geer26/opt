const UsersTab = {
	delimiters: [ "{@", "@}"],
	components: {
		advancedTable: AdvancedTable
	},

// TEMPLATE
	template: `
	<div class="app-tab" id="users-tab">
		<h1>felhasználók kezelése</h1>
		<section>
			<a class="button" @click="newUser"><i class="fa fa-user-plus"></i> új felhasználó</a>
		</section>

		<section>
			<advanced-table
				:fields="[ {name: 'id', title: 'ID', alignment: 'left', sortable: false, width: '4ch'},
						   {name: 'username', title: 'felhasználónév', alignment: 'left', sortable: true, width: '18ch'},
						   {name: 'contact', title: 'kontakt', alignment: 'left', sortable: false},
						   {name: 'added', title: 'regisztráció', alignment: 'left', sortable: true, width: '10ch'}
				 		]"
				:records="usersEnhanced"
				:page="0"
				:records-per-page="3"	
				:record-menu="[ {title: 'Felhasználó törlése', icon: 'fa-trash-alt', action: 'del_user'},
								{title: 'Felhasználó adatainak a módosítása', icon: 'fa-user-edit', action: 'edit_user'}
							 ]"
				empty-text="nincsenek felhasználók"
				>
			</advanced-table>
		</section>
	</div>
	`,



// DATA	
	data() {
		return {
			selectedUser: null
		}
	},



// COMPUTED
	computed: {
		usersEnhanced() {
			return this.users;
		}
	},



// PROPS
	props: ["users"],



// METÓDUSOK
	methods: {
		// Új felhasználó hozzáadása
		newUser() {
			console.log("Új felhasználó hozzáadása");
		}
	}

};
