const app = Vue.createApp({
	data() {
		return {
			boxVisible: true
		}
	},

	methods: {
		handleClick() {
			this.boxVisible = !this.boxVisible;
		}
	}
});

app.component("about", {
	props: ["visible"],

	template: `
	<transition name="slide">
		<div v-if="visible" style="width: 200px; height: 200px; background-color: red"></div>
	</transition>
	`
});

app.mount("#app");
