const TabUsers = {
	delimiters: ["{@", "@}"],

	components: {
		fa: Fa,
		advancedTable: AdvancedTable,
		newUserForm: NewUserForm,
		inlineForm: InlineForm
	},

	template: `
	<div class="tab-content">
		<section>
			<collapsible-form form="new-user-form" :data="{username: 'Példani'}" save cancel reset
			  @save-form="handleSave" title="Új felhasználó hozzáadása"/>
		</section>
		<section>
			<advanced-table
				:records="tabData.users"
				:fields="[
					{name: 'id', title: 'ID', alignment: 'left'},
					{name: 'username', title: 'felhasználónév', alignment: 'left'},
					{name: 'contact', title: 'elérhetőség', alignment: 'left'},
					{name: 'description', title: 'leírás', alignment: 'left'}
				]"
			></advanced-table>
		</section>
	</div>
	`,

	props: ["tabData"],

	methods: {
		handleSave(evt) {
			console.log(evt.username);
		},
		handleCancel() { console.log("CANCEL"); },
		handleReset() { console.log("RESET"); },
		handleChange() { console.log("CHANGE"); }
	}
};
