// Ez a függvény a menüket kezeli = 
// a megadott menuitem-hez rendelt függvényt
// futtatja le.
// Ezek a hozzárendelések az admin vagy a user 
// saját js-ében lesznek megadva, akárcsak
// a függvények
function menuItemClicked(evt) {
	// Aktuális cuccok
	var route = menuRoutes[evt.target.id];
	var newTab = document.getElementById(route.tab_id);

	// Előző cuccok
	var activeGomb = document.querySelector(".menuitem.active");
	var activeRoute = null;
	if (activeGomb != null)
		activeRoute = menuRoutes[activeGomb.id];
	var activeTab = null;
	if (activeRoute)
		activeTab = document.getElementById(activeRoute.tab_id);

	// Ha ugyanarra a gombra kattintottunk, akkor nincs mit csinálni
	if (activeRoute != null && route === activeRoute) {
		// Itt egyszerűen kilépünk, nincs emmi további tennivaló
		return;
	}

	// Ha van aktivált menügomb, akkor azt deaktiválja, és
	// eltünteti a megfelelő tabot is, egyben lefuttatja
	// a bezáráshoz rendelt függvényt
	if (activeRoute != null) {
		activeGomb.classList.remove("active");
		activeTab.classList.remove("visible");
		if (activeRoute.on_hide)
			activeRoute.on_hide();
	}


	// A kiválasztott gombot és tabot aktiválja, ha szükséges, de csak egy 
	// kis késleltetéssel
	if (route.activate) {
		evt.target.classList.add("active");
		newTab.classList.add("visible");
	}

	// A dedikált függvény meghívása
	route.fun();
}

// Itt pedig minden 'menuitem' elemhez hozzáadjuk a
// megfelelő eseményfigyelőt
document.querySelectorAll(".menuitem").forEach(menuitem => {
	menuitem.childNodes.forEach(child => child.style.pointerEvents = "none");
	menuitem.addEventListener("click", menuItemClicked);
});


// Minden app-tab-hoz hozzáadunk egy preloadert...
document.querySelectorAll(".app-tab").forEach(tab => {
	var preloader = document.createElement("div")
	preloader.classList.add("preloader");
	tab.appendChild(preloader);
});

