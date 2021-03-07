/*
SECTION.app-navbar
 |--IMG.logo
 |--DIV.user-info
 |   |--H1.username
 |   |--DIV.small-menu
 |       |--A.button,button-icon   (kilépés)
 |       |--SPAN.icon-button-wrapper
 |           |--A.button,button-icon    (beállítások)
 |--DIV.big-menu
     |--DIV.icon-button-wrapper  (n darab)
         |--A.button,button-icon
COMPONENT (app-tab)
*/
const App = {
	delimiters: ["{@", "@}"],

	template: `
	<section class="app-navbar">
		<img class="logo" src="http://picsum.photos/100/70">
		<div class="user-info">
			<h1 class="username">username</h1>
			<div class="small-menu">
				<a class="button button-icon"
				   title="Kilépés"
				   @click="startLogout()">
				   <fa icon="power-off"/>
				</a>
				<span class="icon-button-wrapper" :class="(currentTab != null && currentTab.tab) == 'tab-settings' ? 'selected' : ''">
					<a class="button button-icon"
				   	   title="Beállítások"
				   	   @click="currentTab = {title: 'Beállítások', tab: 'tab-settings', icon: 'cogs'}">
				   	   <fa icon="cogs"/>
					</a>
				</span>
			</div>
		</div>
		<div class="big-menu">
			<div v-for="item in tabs" class="icon-button-wrapper" :class="(currentTab != null && currentTab.tab) == item.tab ? 'selected' : ''">
				<a class="button button-icon"
			   	   :title="item.title"
			   	   @click="currentTab = item">
			   	   <fa :icon="item.icon" size="2"></fa>
			   	   <span>{@ item.label @}</span>
				</a>
			</div>
		</div>
	</section>
	<section v-if="currentTab != null" class="app-content">
		<component is="app-tab" v-bind="{tab: currentTab, tabData: data}"></component>
	</section>
	`,

	data() {
		return {
			// A programon belüli tab-ok adatai - a menühöz és fejléchez is
			tabs: [
				{title: "Felhasználok kezelése", icon: "users", label: "felhasználók", tab: "tab-users"}
			],
			// Aktuális tab
			currentTab: null,
			// A program által használt összes adat!
			data: "Hello"
		}
	},

	methods: {
		startLogout() {
			// Kijelentkezés kezdeményezése
			if (confirm("Biztosna kijelentkezel az alkalmazásból?"))
				this.$root.eventBus.emit("action", {action: "logout"})
		}
	}
};
