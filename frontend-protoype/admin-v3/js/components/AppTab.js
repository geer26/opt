/*
*/
const AppTab = {
	delimiters: ["{@", "@}"],

	template: `
	<div class="app-tab">
		<div class="tab-header">
			<span class="status" :style="{visibility: loader ? 'visible' : 'hidden'}">
				<img src="img/loader.gif"/>
			</span>
			<span class="tab-title">
				{@ tab.title @}&#160;&#160;&#160;<fa :icon="tab.icon" size="2"/>
			</span>
		</div>
		<div class="tab-content">
			asdfa
		</div>
	</div>
	`,

	data() {
		return {
			loader: false
		}
	},

	props: ["tab", "tabData"]
};
