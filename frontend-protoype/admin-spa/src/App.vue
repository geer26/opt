<template>
  <section class="app-navbar">
    <img class="logo" src="img/logo.png"/>
    <div class="user-info">
      <h1 class="username" v-if="data != null">{{ data.current_user.username }}</h1>
      <div class="small-menu">
        <btn icon="power-off" title="Kilépés" @click="startLogout()"/>
        <span class="icon-button-wrapper" :class="(currentTab != null && currentTab.tab == 'tab-settings' ? 'selected' : '')">
          <btn icon="cogs" title="Beállítások" 
            @click="currentTab = {title: 'Beállítások', tab: 'tab-settings', icon: 'cogs'}"/>
        </span>
      </div>
    </div>

    <div class="big-menu">
      <div v-for="item in tabs" class="icon-button-wrapper"
        :class="(currentTab != null && currentTab.tab == item.tab) ? 'selected' : ''">
        <btn :icon="item.icon" :title="item.title" @click="currentTab = item" icon-size="2x"
          :label="item.label" vertical/>
      </div>
    </div>
  </section>

  <section v-if="currentTab != null" class="app-content">
    <component is="app-tab" v-bind="{tab: currentTab, tabData: data}" ref="currentTab"></component>
  </section>
</template>


<script>
import {library} from '@fortawesome/fontawesome-svg-core'
import {faPowerOff, faCogs, faUsers} from '@fortawesome/free-solid-svg-icons'
import io from 'socket.io-client'
import mitt from 'mitt'
import Btn from './components/Btn.vue'

library.add(faPowerOff, faCogs, faUsers);

export default {
  name: 'App',

  data() {
    return {
      // A TAB-okhoz tartozó cuccok
      tabs: [
        {title: "Felhasználók kezelése", icon: "users", label: "felhasználók", tab: "tab-users"}
      ],
      currentTab: null,

      // Az app alapvető adatai
      data: null,


      socket: null,
      eventBus: null
    }
  },

  // Ha elkészült a komponens, akkor szépen csatlakozunk a Socket.io
  // szerverhez, majd lekérdezzük az admin-adatokat
  created() {
    // Inicializáljuk a központi esemény-kezelőt:
    this.eventBus = mitt();

  
    // Csatlakozunk a Socket.IO szerverhez
    this.socket = io("ws://localhost:5000");

    // A szerverről érkező üzenetek kezelése
    this.socket.on("admin", (data) => {
      switch(data.event) {
        case 1999: // Admin adatok megérkeztek
          this.data = JSON.parse(data.su_data);
          break;
      }
    });


    // Admin adatok lekérdezése
    this.socket.emit("admin", {event: 2999});
  },

  methods: {
    startLogout(data) {
      // Kijelentkezés kezdeményezése
      if (confirm("Biztosan kijelentkezel az alkalmazásból?")) {
        console.log("KILÉPÉS");
        // TODO: init kilépés
      }
    }
  }

}
</script>


<style>

.app-navbar {
  width: 100%;
  background-color: #A1BABA;
  display: flex;
  flex-flow: row nowrap;
  justify-content: flex-start;
  align-items: center;
}
.app-navbar img.logo { display: block; margin: 5px 0 5px 1rem; }
.app-navbar .user-info {
  align-self: stretch;
  display: flex;
  flex-flow: column nowrap;
  justify-content: flex-end;
  margin: 0;
  margin-left: 1rem;
}
.app-navbar .user-info .username { margin-bottom: 0.3rem; }
.app-navbar .user-info h1 { margin: 0; font-size: 1.2rem; }
.small-menu { 
  font-size: 1rem; 
  display: flex;
  flex-flow: row nowrap;
  justify-content: flex-start;
  align-items: flex-end;
}
.big-menu {
  align-self: flex-end;
  margin-left: 2rem;
  display: flex;
  flex-flow: row nowrap;
}
.big-menu .button-icon {
  display: flex;
  flex-flow: column nowrap;
  align-items: center;
}
.app-navbar .icon-button-wrapper {
  background-color: #A1BABA;
  border-radius: 0.5rem 0.5rem 0 0;
  transition: all 0.3s ease;
  margin: 0 0.1rem 0 0.1rem;
}
.app-navbar .icon-button-wrapper:hover { filter: brightness(1.1); }
.app-navbar .icon-button-wrapper.selected { background-color: #F3F6F6 !important; }
.app-content {
  background-color: #F3F6F6;
  padding: 0.5rem 1rem 1rem 1rem;
}

</style>
