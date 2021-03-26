<template>
<div class="app-tab">
	<div class="tab-header">
		<span class="status" :style="{visibility: isLoading ? 'visible' : 'hidden'}">
			<img src="img/loader.gif"/>
		</span>
		<span class="tab-title">
			{{ tab.title }}&#160;&#160;<font-awesome-icon :icon="tab.icon" size="2x"/>
		</span>
	</div>

	<div class="tab-content">
	</div>
</div>
</template>


<script>
export default {
	name: "AppTab",

	data() {
		return {
			
		}
	},

	props: ["tab", "tabData", "isLoading"]
}
</script>


<style>
.app-tab .tab-header {
	display: flex;
	flex-flow: row nowrap;
	justify-content: space-between;
	align-items: center;
	font-size: 1rem;
	font-weight: bold;
	font-style: italic;
	color: var(--backgroundColor);
	margin-bottom: 2rem;
	text-transform: lowercase;
}
.app-tab .tab-content {
	position: relative;
}
.app-tab .blank {
	background-color: var(--foregroundColor);
	opacity: 0.3;
	position: absolute;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
}
</style>