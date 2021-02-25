console.log(admin_data);

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
	    }
	}

	});


app.component("table-component", TableComponent);


const vm = app.mount("#tab-users")