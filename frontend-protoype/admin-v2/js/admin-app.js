const mainApp = Vue.createApp({
	delimiters: ["{@", "@}"],

	components: {
		fa: Fa,
		appTab: AppTab,
		tabSettings: TabSettings,
		tabMessages: TabMessages,
		tabUsers: TabUsers,
		tabModules: TabModules,
		tabTestbatteries: TabTestbatteries,
		tabReports: TabReports,
		tabDb: TabDb
	},

	data() {
		return {
			menu: [
				{title:'Üzenetek', icon: 'envelope', label: 'üzenetek', tab: 'tab-messages'},
				{title:'Felhasználók', icon: 'users', label: 'felhasználók', tab: 'tab-users'},
				{title:'Modulok', icon: 'box-open', label: 'modulok', tab: 'tab-modules'},
				{title:'Tesztcsomagok', icon: 'clipboard-list', label: 'tesztcsomagok', tab: 'tab-testbatteries'},
				{title:'Kimutatások', icon: 'chart-bar', label: 'kimutatások', tab: 'tab-reports'},
				{title:'Adatbázis', icon: 'coins', label: 'adatbázis', tab: 'tab-db'}
			],
			currentTab: null,
			adminData: admin_data
		}
	}


});
// Globálisan komponensek regisztrálása
mainApp.component("fa", Fa);
mainApp.component("new-user-form", NewUserForm);
mainApp.component("inline-form", InlineForm);
mainApp.component("collapsible-form", CollapsibleForm);
// EventBus hozzáadása (mitt library)
mainApp.config.globalProperties.eventBus = mitt();
const vmMainApp = mainApp.mount("#main-app");
