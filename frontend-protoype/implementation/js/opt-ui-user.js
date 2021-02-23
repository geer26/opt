// Itt adjuk meg az elérhető menüpontok, és a hozzájuk
// tartozó függvények listáját
var menuRoutes = {
	menuitem_messages: {
		fun: function() {
			console.log("Showing messages");
		},
		activate: true,
		tab_id: "tab-messages",
		on_hide: function() {
			console.log("Hiding messages");
		}
	},
	menuitem_sessions: {
		fun: function() {
			console.log("Showing sessions");
		},
		activate: true,
		tab_id: "tab-sessions",
		on_hide: function() {
			console.log("Hiding sessions");
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
	menuitem_catalog: {
		fun: function() {
			console.log("Showing catalog");
		},
		activate: true,
		tab_id: "tab-catalog",
		on_hide: function() {
			console.log("Hiding catalog");
		}
	},
	menuitem_logout: {
		fun: function() {
			console.log("Logging out");
		}
	}
};

