// FontAwesome ikon, állítható színnel és betűmérettel
const Fa = {
	template: `
	<i class="fas" :class="'fa-'+icon" :style="{fontSize: (size + 'rem'), color: color}"></i>
	`,

	props: {
		size: {
			type: [String,Number]
		},

		icon: {
			type: String,
			default: "dice"
		},

		color: {
			type: String
		}
	}
};
