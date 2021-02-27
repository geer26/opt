const TableComponent = {
	delimiters: ["{@", "@}"],

	template:
	`
	<div class="table-component">
		<table>
			<thead>
				<tr>
					<th v-for="field in fields" v-bind:style="{width: field.stretch ? '100%' : ''}">
						{@ field.title @}
						<span class="sorter" 
							  v-if="field.sortable" 
							  v-on:click="applySort(field.name)">
							<i v-if="field.name == sort.by && sort.direction == 0" class="fa fa-sort-down"></i>
							<i v-else-if="field.name == sort.by && sort.direction == 1" class="fa fa-sort-up"></i>
							<i v-else class="fa fa-sort"></i>
						</span>
					</th>
				</tr>
			</thead>
			<tbody>
				<template v-for="record in selectedRecords">
				<tr 
					v-bind:class="selected != null ? (selected.id == record.id ? 'selected' : '') : ''"
					v-on:click="selectRecord(record.id)">
					<td v-for="field in fields" v-bind:style="{textAlign: field.alignment}" v-html="record[field.name]"></td>
				</tr>
				<tr v-if="menu != null && selected != null && selected.id == record.id" class="selected record-menu">
					<td :colspan="fields.length">
						<span>
							<a  v-for="item in menu"
								v-on:click="callMenuAction(item.action, record)"
								:title="item.title">
								<i class="fa" :class="item.icon != null ? item.icon : ''"></i>
							</a>
						</span>
					</td>
				</tr>
				</template>
			</tbody>
		</table>
		<div v-if="numPages >= 2" class="table-component-pager">
			<a @click="changePage('first')"><i class="fa fa-angle-double-left"></i></a> 		
			<a @click="changePage('dec')"><i class="fa fa-angle-left"></i></a> 
			<span>{@ (currentPage + 1) + "/" + numPages @}</span>
			<a @click="changePage('inc')"><i class="fa fa-angle-right"></i></a> 
			<a @click="changePage('last')"><i class="fa fa-angle-double-right"></i></a>
		</div>
	</div>
	`,

	data() {
		return {
			currentPage: 0,
			currentCount: 25,

			selected: null,
			sort: {
				by: null,
				direction: 0,
			}
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
		},
		menu: {
			type: Array,
			default: null
		}
	},

	// Itt átadjuk a propertyk értékét a megfelelő belső változónak,
	// ha elkészült a komponens
	created() {
		this.currentPage = this.page;
		this.currentCount = this.count;
	},

	beforeUpdate() {
		// Itt lecsekkoljuk, hogy az aktuális lap nem több-e, 
		// mint a maximum
		if (this.currentPage > this.numPages-1)
			this.currentPage = Math.max(0, this.numPages-1);
	},

	watch: {
		records() {
			this.resetSelection();
		}
	},

	methods: {
		// A lapozást megvalósító függvény
		changePage: function(command) {
			switch(command) {
				case "inc":
					this.currentPage = Math.min(this.currentPage+1, this.numPages-1);
					break;
				case "dec":
					this.currentPage = Math.max(0, this.currentPage - 1)
					break;
				case "first":
					this.currentPage = 0;
					break;
				case "last":
					this.currentPage = this.numPages-1;
					break;
			}
		},

		callMenuAction(action, rec) {
			window[action](rec);
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
		},

		resetSelection() {
			this.selected = null;
			this.$emit("selectionChanged", this.selected);
		},

		applySort(name) {
			if (this.sort.by == null) {
				this.sort.by = name;
				this.sort.direction = 0;
			} else if (this.sort.by == name) {
				// Ha ugyanarra klikkelünk rá, akkor forgatjuk az irányt
				this.sort.direction = (this.sort.direction + 1) % 3;
				// Ha az irány a 2, akkor nem rendezünk sorba
				if (this.sort.direction == 2) {
					this.sort.by = null;
					this.sort.direction = 0;
				}
			} else {
				this.sort.by = name;
				this.sort.direction = 0;
			}
		}
	},

	emits: ["selectionChanged"],

	computed: {
		selectedRecords() {
			// SORBARENDEZÉS
			var recs = Array.from(this.records);
			if (this.sort.by != null) {
				// Itt először sorba kell rendeznünk, ha egyáltalán van megadva erre szabály
				if (this.sort.direction == 0)				
					recs.sort((a,b) => (a[this.sort.by] > b[this.sort.by]) ? 1 : -1)
				if (this.sort.direction == 1)
					recs.sort((a,b) => (a[this.sort.by] < b[this.sort.by]) ? 1 : -1)
			}

			// KIVÁLASZTOTT REKORDOK
			var start = this.currentCount * this.currentPage;
			return recs.slice(start, start + this.currentCount);
		},

		numPages() {
			return Math.ceil(this.records.length / this.currentCount);
		}
	}
};