<template>
  <div id="app">
    <NavBar 
      @toggle-seleccion-campeonato="toggleSeleccionCampeonato"
      :campeonato-seleccionado="campeonatoSeleccionado"
    />
    <router-view 
      :seleccionando-campeonato="seleccionandoCampeonato" 
      @campeonato-seleccionado="handleCampeonatoSeleccionado"
      :key="$route.fullPath"
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
    const seleccionandoCampeonato = ref(false);
    const campeonatoSeleccionado = ref(!!localStorage.getItem('campeonato_id'));

    const toggleSeleccionCampeonato = (value) => {
      seleccionandoCampeonato.value = value;
      if (!value) {
        campeonatoSeleccionado.value = false;
        localStorage.removeItem('campeonato_id');
        localStorage.removeItem('campeonato_nombre');
        localStorage.removeItem('campeonato_partidas');
      }
    };

    const handleCampeonatoSeleccionado = () => {
      seleccionandoCampeonato.value = false;
      campeonatoSeleccionado.value = true;
    };

    watch(() => localStorage.getItem('campeonato_id'), (newValue) => {
      campeonatoSeleccionado.value = !!newValue;
    });

    return {
      seleccionandoCampeonato,
      campeonatoSeleccionado,
      toggleSeleccionCampeonato,
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
