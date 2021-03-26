<comment>
Ez itt egy általános gomb-komponens, amellyel különböző felépítésű gombok készíthetők,
a következő beállítások mentén
- ikon van vagy nincs (icon="")
- ikon mérete (icon-size="")
- cimke van vagy nincs (label="")
- vertikális, vagy horizontális elrendezés (vertical  - alapértelmezett a horizontáls)
- ikon és szöveg egymáshoz való helyzete (align="start|center|end")
- cimke stílusa (bold, italic, underline, label-color="" label-size="")
- blokk-gomb stílus, háttérrel (bg="háttér színe")
- front-szín (fg="front /ikon és cimke/ színe")

A gombnak megadható egy id attribútum

A gomb letiltható ("disabled"), valamint tüzel eseményt ("click"), amelyben alapértelmezésben
átadja magát a gombot, mint objektumot.
</comment>

<template>
	<button @click="$emit('click', this)" 
		:style="buttonStyle">
		<font-awesome-icon v-if="icon != null" :icon="icon" :size="iconSize"/>
		<span :style="labelStyle" v-if="label != ''">{{label}}</span>
	</button>	
</template>


<script>
	export default {
		name: 'Btn',

		computed: {
			buttonStyle() {
				return {
					flexDirection: this.vertical ? "column" : "row",
					alignItems: (this.align == "center") ? "center" : (this.align == "start") ? "flex-start" : (this.align == "end") ? "flex-end" : "center",

					color: this.fg != null ? this.fg : "",
					background: this.bg != null ? this.bg : "none",
					paddingLeft: this.bg != null ? "1rem" : "",
					paddingRight: this.bg != null ? "1rem" : ""
				}
			},

			labelStyle() {
				return {
					fontSize: this.labelSize + "rem",
					marginLeft: this.vertical ? "" : "1ch",
					fontWeight: this.bold ? "bold" : "none",
					fontStyle: this.italic ? "italic" : "none",
					textDecoration: this.underline ? "underline" : "none",
					color: this.labelColor != null ? this.labelColor : ""
				}
			}
		},

		props: {
			icon: {
				type: String,
				required: false,
				default: null
			},
			iconSize: {
				type: String,
				required: false,
				default: "1x"
			},
			label: {
				type: String,
				required: false,
				default: ""
			},
			id: {
				type: String,
				required: false,
				default: ""
			},
			vertical: {
				type: Boolean,
				required: false,
				default: false
			},
			labelSize: {
				type: [String, Number],
				required: false,
				default: 1
			},
			align: {
				type: String,
				required: false,
				default: "center"
			},
			bold: {
				type: Boolean,
				required: false,
				default: false
			},
			italic: {
				type: Boolean,
				required: false,
				default: false
			},
			underline: {
				type: Boolean,
				required: false,
				default: false
			},
			fg: {
				type: String,
				required: false,
				default: null
			},
			bg: {
				type: String,
				required: false,
				default: null
			},
			labelColor: {
				type: String,
				required: false,
				default: null
			}
		},

		emits: ["click"]
	}
</script>


<style>

button {
	border: none;
	outline: none;
	padding: 0.3rem;	
	cursor: pointer;
	font-size: 1rem;
	transition: filter 0.3s ease;
	display: flex;
	flex-wrap: nowrap;
	border-radius: 0.7rem;
}
button:hover:not(:disabled) { filter: brightness(1.2); }
button:active:not(:disabled) { filter: brightness(1.4); }
button:disabled {
	cursor: default;
}



</style>
