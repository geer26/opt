import {createApp} from 'vue'
import App from './App.vue'
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'


let app = createApp(App);
// Komponensek globális regisztrálása - ezek minden App alá
// tartozó komponensen belül elérhetőek lesznek
app.component("font-awesome-icon", FontAwesomeIcon);


// App csatolása a DOM-hoz
let mapp = app.mount('#app');
