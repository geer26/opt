// Egy űrlap opcionális kezelőgombokkal
/*
DIV.inline-form
 |--DIV.form-content
 |   |--COMPONENT (maga az űrlap)
 |--DIV.form-footer
     |--A.button,button-solid
     |--A.button,button-text
     |--A.button,button-text
*/
const InlineForm = {
	delimiters: ["{@", "@}"],

	template: `
	<div class="inline-form">
		<div class="form-content">
			<component :is="form" v-bind="{data: data, ref: 'innerForm'}"/>
		</div>
		<div class="form-footer">
			<a v-if="save != undefined" class="button button-solid" @click="saveForm()"><fa icon="check"/> mentés</a>
			<a v-if="cancel != undefined" class="button button-text" @click="cancelForm()">mégse</a>
			<a v-if="reset != undefined" class="button button-text" @click="resetForm()">tartalom törlése</a>
		</div>
	</div>
	`,

	data() {
		return {
		}
	},

	props: ["form", "data", "save", "cancel", "reset"],

	methods: {
		saveForm() {
			this.$emit("save-form", this.$refs.innerForm.get());
		},

		cancelForm() {
			this.$refs.innerForm.reset();
			this.$emit("cancel-form");
		},

		resetForm() {
			// Nullázzuk az űrlapot
			this.$refs.innerForm.reset();
			this.$emit("reset-form");
		}
	}
};

