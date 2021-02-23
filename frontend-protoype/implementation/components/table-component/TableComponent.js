const TableComponent = {
	delimiters: ["{@", "@}"],

	template:
	`
	<div class="table-component">
		<table>
			<thead>
				<tr>
					<th v-for="field in fields" v-bind:style="{width: field.stretch ? '100%' : ''}">{@ field.title @}</th>
				</tr>
			</thead>
			<tbody>
				<tr v-for="record in selectedRecords" 
					v-bind:class="selected != null ? (selected.id == record.id ? 'selected' : '') : ''"
					v-on:click="selectRecord(record.id)">
					<td v-for="field in fields" v-bind:style="{textAlign: field.alignment}">{@ record[field.name] @}</td>
				</tr>
			</tbody>
		</table>
		<div class="table-component-pager">
			<a @click="changePage('first')"><i class="fa fa-angle-double-left"></i></a> 		
			<a @click="changePage('dec')"><i class="fa fa-angle-left"></i></a> 
			<span>{@ (currentPage + 1) + "/" + (1+Math.floor(records.length/currentCount)) @}</span>
			<a @click="changePage('inc')"><i class="fa fa-angle-right"></i></a> 
			<a @click="changePage('last')"><i class="fa fa-angle-double-right"></i></a>
		</div>
	</div>
	`,

	data() {
		return {
			currentPage: 0,
			currentCount: 25,

			selected: null
		}
	},

	props: {
		fields: {
			type: Array,
			required: true
		},
		records: {
			type: Array,
			required: true
		},
		page: {
			type: Number,
			default: 0
		},
		count: {
			type: Number,
			default: 25
		}
	},

	// Itt átadjuk a propertyk értékét a megfelelő belső változónak,
	// ha elkészült a komponens
	created() {
		this.currentPage = this.page;
		this.currentCount = this.count;
	},

	methods: {
		// A lapozást megvalósító függvény
		changePage: function(command) {
			switch(command) {
				case "inc":
					this.currentPage = Math.min(this.currentPage + 1, Math.floor(this.records.length / this.currentCount));
					break;
				case "dec":
					this.currentPage = Math.max(0, this.currentPage - 1)
					break;
				case "first":
					this.currentPage = 0;
					break;
				case "last":
					this.currentPage = Math.floor(this.records.length / this.currentCount);
					break;
			}
		},

		selectRecord(id) {
			if (this.selected != null && id == this.selected.id) {
				this.selected = null;
			} else {
				this.selected = this.records.find(record => { return record.id === id} );
			}

			// Tüzelünk egy eseményt, amely arról szól, hogy megváltozott a kijelölés
			// FIGYELEM! az lehet null is!
			// Az esemény payloadja maga a kiválasztott rekord
			this.$emit("selectionChanged", this.selected);
		}
	},

	emits: ["selectionChanged"],

	computed: {
		selectedRecords() {
			var start = this.currentCount * this.currentPage;
			return this.records.slice(start, start + this.currentCount);
		}
	}
};