<template>
  <div id="app">
    <NavBar 
      :campeonato-seleccionado="campeonatoSeleccionado"
    />
    <router-view 
      @campeonato-seleccionado="handleCampeonatoSeleccionado"
    ></router-view>
  </div>
</template>

<script>
import { ref, watch } from 'vue';
import NavBar from '@/components/NavBar.vue'

export default {
  name: 'App',
  components: {
    NavBar
  },
  setup() {
    const campeonatoSeleccionado = ref(!!localStorage.getItem('campeonato_id'));

    const handleCampeonatoSeleccionado = (seleccionado) => {
      campeonatoSeleccionado.value = seleccionado;
    };

    watch(() => localStorage.getItem('campeonato_id'), (newValue) => {
      campeonatoSeleccionado.value = !!newValue;
    });

    return {
      campeonatoSeleccionado,
      handleCampeonatoSeleccionado
    };
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
