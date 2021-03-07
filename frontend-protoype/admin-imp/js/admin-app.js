// EventBus


// Fő applikáció
const mainApp = Vue.createApp({
    delimiters: ["{@", "@}"],

	data() {
		return {
            adminData: admin_data,
			currentTab: null,
			disabled: true
		}
	},

	computed: {
		tabProperties() {
			switch(this.currentTab) {
				case "users-tab": 
					return {users: this.adminData.users};
					break;
			};

			return {adminData: this.adminData};
		}
	},

	components: {
		settingsTab: SettingsTab,
        messagesTab: MessagesTab,
        usersTab: UsersTab,
        modulesTab: ModulesTab,
        testbatteriesTab: TestbatteriesTab,
        reportsTab: ReportsTab,
        dbTab: DbTab

	},


	methods: {
		callLogout() { actionRouter.call("logout"); }
	}
});
const vmMain = mainApp.mount("#main-app");
