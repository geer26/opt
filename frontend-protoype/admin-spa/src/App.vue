<template>
  <font-awesome-icon icon="user-secret" size="2x"/>
</template>


<script>
import {library} from '@fortawesome/fontawesome-svg-core'
import {faUserSecret} from '@fortawesome/free-solid-svg-icons'
import io from 'socket.io-client'
import mitt from 'mitt'

library.add(faUserSecret);

export default {
  name: 'App',

  data() {
    return {
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
    // Admin adatok lekérdezése
    this.socket.emit("admin", "Valami üzenet");
  }

}
</script>


<style>
</style>
