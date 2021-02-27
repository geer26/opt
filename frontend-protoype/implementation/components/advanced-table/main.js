// Teszt-adatok
const testdata = [
	{id: 1, author: "Shanice Wilkes", title: "Sleeping Fairy", genre: "sci-fi"},
	{id: 2, author: "Laaibah Lane", title: "The Captured Hustler", genre: "crimi"},
	{id: 3, author: "Humaira Kinney", title: "Weeping of Shadow", genre: "drama"},
	{id: 4, author: "Kira Barnett", title: "The Spark's Girl", genre: "crimi"},
];		


const myActions = ActionRouter.create({
	debug: false,
	actions: {
		torles(record) {
			let index = vm.konyvek.findIndex(konyv => record.id == konyv.id)
			vm.konyvek.splice(index, 1);
		}
	}
})


// App létrehozása és csatolása
const app = Vue.createApp({
	delimiters: ["{@", "@}"],

	data() {
		return {
			konyvek: testdata,
			actionRouter: myActions
		}
	},

	methods: {
		handleSelectionChanged(payload) {
		}
	},

	components: {
		advancedTable: AdvancedTable
	},

	computed: {
		konyvekEnhanced() {
			var konyvek2 = JSON.parse(JSON.stringify(this.konyvek));
			konyvek2.forEach(item => {
				var icon = "";
				switch( item.genre) {
					case "drama": icon = "<i class='fa fa-trash-alt'></i> "; break;
					case "sci-fi": icon = "<i class='fa fa-ambulance'></i> "; break;
					case "crimi": icon = "<i class='fa fa-check'></i> "; break;
					case "history": icon = "<i class='fa fa-book'></i> "; break;
				}
				item.genreIcon = icon;
			});
			return konyvek2
		}
	}

});
const vm = app.mount("#app")



