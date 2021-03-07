const AppTab = {
	delimiters: ["{@", "@}"],

	template: `
	<section class="app-content">
		<div class="app-tab">
			<div class="tab-header" style="display: flex; flex-flow: row nowrap; justify-content: space-between;">
				<span class="status">
					<span :style="{visibility: status ? 'visible' : 'hidden'}">STATUS</span>
				</span>
				<h1><fa icon="users" size="2"/> felhasználók kezelése</h1>
			</div>
			<component :is="tab" v-bind="{tabData: tabData}"/>
		</div>
	</section>	
	`,

	data() {
		return {
			status: true
		}
	},

	props: ["tab", "tabData"],

	methods: {
		showStatus() { this.status = true; },
		hideStatus() { this.status = false; }
	},

	mounted() {
		// Ha a szerver-folyamat befejeződött, akkor eltüntetjük a státuszt
		this.$root.on("status-received", this.hideStatus);
	}
};
