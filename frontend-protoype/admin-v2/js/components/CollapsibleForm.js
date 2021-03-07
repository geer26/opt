/*
DIV.collapsible-form
 |--DIV.form-header
 |   |A.button
 |--DIV.form-container
     |--DIV.form-content
     |--DIV.form-footer
         |--A.button,button-solid
         |--A.button,button-text
         |--A.button,button-text
*/
const CollapsibleForm = {
	delimiters: ["{@", "@}"],

	template: `
	<div class="collapsible-form">
		<div class="form-header">
			<a class="button" @click="flipForm()">
				<fa :icon="icon"/>
				{@ title @}
				<fa :icon="open ? 'caret-down' : 'caret-right'"/></a>
		</div>
		<div v-if="open" class="form-container">
			<div class="form-content">
				<component :is="form" v-bind="{data: data, ref: 'innerForm'}"/>
			</div>
			<div class="form-footer">
				<a class="button button-solid" @click="saveForm"><fa icon="check"/> mentés</a>
				<a class="button button-text" @click="cancelForm">mégse</a>
				<a class="button button-text" @click="resetForm">tartalom törlése</a>
			</div>
		</div>
	</div>
	`,

	data() {
		return {
			open: false
		}
	},	

	props: ["icon", "title", "data", "form"],

	methods: {
		flipForm() {
			this.open = !this.open;
		},

		resetForm() {
			// Űrlap türlése
			this.$refs.innerForm.reset();
		},
		cancelForm() {
			// Űrlap törlése
			this.$refs.innerForm.reset();
			// Bezárás
			this.open = false;
		},
		saveForm() {
			this.$emit("save-form", this.$refs.innerForm.get());
		}
	}
};
