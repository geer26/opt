// Itt adjuk meg az elérhető menüpontok, és a hozzájuk
// tartozó függvények listáját
var menuRoutes = {

	menuitem_messages: {
		fun: function() {
			console.log("Showing messages");
		},
		on_data_ready: function(data) {

		},
		on_error: function(data) {

		},
		activate: true,
		tab_id: "tab-messages",
		on_hide: function() {
			console.log("Hiding messages");
		}
	},

	menuitem_users: {
		fun: function() {
			console.log("Showing users");
		},
		activate: true,
		tab_id: "tab-users",
		on_hide: function() {
			console.log("Hiding users");
		}
	},

	menuitem_modules: {
		fun: function() {
			console.log("Showing modules");
		},
		activate: true,
		tab_id: "tab-modules",
		on_hide: function() {
			console.log("Hiding modules");
		}
	},

	menuitem_reports: {
		fun: function() {
			console.log("Showing reports");
		},
		activate: true,
		tab_id: "tab-reports",
		on_hide: function() {
			console.log("Hiding reports");
		}
	},

	menuitem_db: {
	    fun: function() {
			console.log("Showing database operations");
		},
		activate: true,
		tab_id: "tab-db",
		on_hide: function() {
			console.log("Hiding database operations");
		}
	},

	menuitem_log: {
	    fun: function() {
			console.log("Showing log operations");
		},
		activate: true,
		tab_id: "tab-log",
		on_hide: function() {
			console.log("Hiding log operations");
		}
	},

	menuitem_logout: {
		fun: function() {
			location.href='/logout';
		}
	}

};
