// A fő app létrehozása és inicializálás
// ----------------------------------------------------------------------------------
const app = Vue.createApp(App);
// Komponensek globális regisztrálása
app.component("fa", Fa);
app.component("app-tab", AppTab);
app.component("tab-users", TabUsers);
app.component("tab-settings", TabSettings);

// Gloobális eventBus hozzáadása, amelyen keresztül kommunikál az
// ActionRouter-rel - ez a 'mitt' library-n keresztül történik
app.config.globalProperties.eventBus = mitt();

// App csatolása az app-container-hez
const vmApp = app.mount("#app");
// ----------------------------------------------------------------------------------



// Adatok hozzáadása (az app data propertyjéhez)
// ----------------------------------------------------------------------------------
// vmApp.data = admin_data;
vmApp.data = admin_data;
// ----------------------------------------------------------------------------------



// Alapvető eseményfigyelők:
// ----------------------------------------------------------------------------------
// Itt figyelünk egy action eseményt, amely arra utal, hogy a program
// valamely komponense valamilyen akciót kezdeményez (pl. rögzítés adatbázisba,
// adatok lekérdezése, stb.)
vmApp.eventBus.on("action", evt => { actionRouter.call(evt.action, evt.payload) });
// Egy függvény, ami lerövidíti a cuccot
function $action(action, payload) {
	vmApp.eventBus.emit("action", {action: action, payload: payload});
}
// Az egyes függvények a 'status' eseményt hívhatják meg (ezt figyelhetik az egyges
// komponensek), a küldött payload szerkezete:
// {
//   status_code: 0, 
//   message: "opcionális üzenet"
// }
// vmApp.eventBus.emit("status", { status_code: 0, message: "Minden rendben!"})
// Egy lehetséges rövidítés, ami így használható
// $$(code, message)
function $status(status_code, message) {
	vmApp.eventBus.emit("status", {satus_code: status_code, message: message}); 
}
// Adatok frissítése
// A 'data' property-ben azok az adatok jönnek át, amik változtak
// pl. {
//       users: [newdata]
//     }
function $data_change(data) {
	vmApp.eventBus.emit("data-change", data);
}
// ----------------------------------------------------------------------------------

