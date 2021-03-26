import {createApp} from 'vue'
import App from './App.vue'
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'
import Btn from './components/Btn.vue'


let app = createApp(App);
// Komponensek globális regisztrálása - ezek minden App alá
// tartozó komponensen belül elérhetőek lesznek
app.component("font-awesome-icon", FontAwesomeIcon);
app.component("btn", Btn);


// App csatolása a DOM-hoz
let mapp = app.mount('#app');
