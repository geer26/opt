const AdvancedTable = {
// CONFIG
	delimiters: ["{@", "@}"],



// TEMPLATE
	template:
	`
	<div class="advanced-table" style="box-sizing: border-box">
		<table style="width: 100%; border-collapse: collapse">
			<thead>
				<tr>
					<th v-for="field in fields" v-bind:style="{width: field.stretch ? '100%' : field.width ? field.width : ''}" style="white-space: nowrap; textAlign: left; vertical-align: top; padding: 0 0.3em 0 0.3em; white-space: nowrap; overflow: hidden">
						{@ field.title @}
						<span class="sort-icon" 
							  v-if="field.sortable" 
							  v-on:click="applySort(field.name)"
							  style="margin-left: 0.1em; cursor: pointer"
							  title="Rekordok rendezése">
							<i v-if="field.name == sort.by && sort.direction == 0" class="fa fa-sort-down"></i>
							<i v-else-if="field.name == sort.by && sort.direction == 1" class="fa fa-sort-up"></i>
							<i v-else class="fa fa-sort"></i>
						</span>
					</th>
				</tr>
			</thead>
			<tbody>
				<tr v-if="records.length == 0">
					<td :colspan="fields.length"><div class="empty-content" v-html="emptyText"></div></td>
				</tr>
				<template v-for="record in selectedRecords">
				<tr 
					v-bind:class="selected != null ? (selected.id == record.id ? 'selected' : '') : ''"
					v-on:click="selectRecord(record.id)">
					<td v-for="field in fields" v-bind:style="{textAlign: field.alignment}" v-html="record[field.name]" style="vertical-align: top; padding: 0 0.3em 0 0.3em; white-space: nowrap; overflow:hidden"></td>
				</tr>
				<tr v-if="recordMenu != null && selected != null && selected.id == record.id" class="record-menu-container">
					<td :colspan="fields.length">
						<div style="width: 100%; text-align: center; padding: 0.5em 0 0.5em 0" class="record-menu">
							<a  v-for="item in recordMenu"
								v-on:click="callMenuAction(item.action, record)"
								:title="item.title"
								style="cursor: pointer; margin: 0 0.4em 0 0.4em">
								<i class="fa" 
								   :class="item.icon != null ? item.icon : ''"
								   :style="{color: item.color != null ? item.color : ''}"></i>
							</a>
						</div>
					</td>
				</tr>
				</template>
			</tbody>
		</table>
		<div v-if="numPages >= 2" class="page-selector" style="display: flex; flex-flow: row nowrap; justify-content: center">
			<a @click="changePage('first')" style="margin-right: 0.5em; cursor: pointer" title="Első oldal"><i class="fa fa-angle-double-left"></i></a> 		
			<a @click="changePage('dec')" style="margin-right: 0.5em; cursor: pointer" title="Előző oldal"><i class="fa fa-angle-left"></i></a> 
			<span class="page-display">{@ (currentPage + 1) + "/" + numPages @}</span>
			<a @click="changePage('inc')" style="margin-left: 0.5em; cursor: pointer" title="Következő oldal"><i class="fa fa-angle-right"></i></a> 
			<a @click="changePage('last')" style="margin-left: 0.5em; cursor: pointer" title="Utolsó oldal"><i class="fa fa-angle-double-right"></i></a>
		</div>
	</div>
	`,



// DATA
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



// PROPERTIES
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
		recordsPerPage: {
			type: Number,
			default: 25
		},
		recordMenu: {
			type: Array,
			default: null
		},
		actionRouter: {
			type: Object,
			default: null
		},
		emptyText: {
			type: String,
			default: null
		}
	},



// HOOKS
	created() {
		this.currentPage = this.page;
		this.currentCount = this.recordsPerPage;
	},

	beforeUpdate() {
		// Itt lecsekkoljuk, hogy az aktuális lap nem több-e, 
		// mint a maximum lehetséges
		if (this.currentPage > this.numPages-1)
			this.currentPage = Math.max(0, this.numPages-1);
	},



// WATCHES
	watch: {
		records() {
			this.resetSelection();
		}
	},



// COMPONENT METHODS
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

		// A rekordhoz tartozó menü alapján egy függvény meghívása
		callMenuAction(action, rec) {
			if (this.actionRouter) {
				this.actionRouter.call(action, rec);
			}
		},

		// Rekord megjelölése
		selectRecord(id) {
			if (this.selected != null && id == this.selected.id) {
				this.selected = null;
			} else {
				this.selected = this.records.find(record => { return record.id == id} );
			}

			// Tüzelünk egy eseményt, amely arról szól, hogy megváltozott a kijelölés
			// FIGYELEM! az lehet null is!
			// Az esemény payloadja maga a kiválasztott rekord
			this.$emit("selectionChanged", this.selected);
		},

		// A kiválasztás megszüntetése
		resetSelection() {
			this.selected = null;
			this.$emit("selectionChanged", this.selected);
		},

		// Sorbarendezés a kiválasztott szempont és irány alapján
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



// EVENTS
	emits: ["selectionChanged"],



// COMPUTED FIELDS
	computed: {
		// Egy oldalnyi rekord leszűrése
		selectedRecords() {
			// SORBARENDEZÉS
			var recs = Array.from(this.records);
			if (this.sort.by != null) {
				// Itt először sorba kell rendeznünk, ha egyáltalán van megadva erre szabály
				if (this.sort.direction == 0)				
					recs.sort((a,b) => (a[this.sort.by] > b[this.sort.by]) ? 1 : -1);
				if (this.sort.direction == 1)
					recs.sort((a,b) => (a[this.sort.by] < b[this.sort.by]) ? 1 : -1);
			}

			// KIVÁLASZTOTT REKORDOK
			var start = this.currentCount * this.currentPage;
			return recs.slice(start, start + this.currentCount);
		},

		// A szükséges oldalak száma
		numPages() {
			return Math.ceil(this.records.length / this.currentCount);
		}
	}
};