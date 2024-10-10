<template>
  <nav class="bg-blue-500 p-4 flex justify-between items-center">
    <ul class="flex space-x-4">
      <li v-if="!campeonatoSeleccionado"><router-link to="/" class="text-white hover:text-gray-200">Inicio</router-link></li>
      <li v-if="!campeonatoSeleccionado"><router-link to="/campeonatos" class="text-white hover:text-gray-200">Campeonatos</router-link></li>
      <li v-if="campeonatoSeleccionado"><router-link to="/inscripcion" class="text-white hover:text-gray-200">Inscripción</router-link></li>
      <template v-if="campeonatoSeleccionado">
        <li v-for="(files, dir) in componentDirectories" :key="dir" class="relative">
          <div @mouseleave="closeDropdown" @mouseenter="cancelCloseDropdown">
            <span 
              @click="toggleDropdown(dir)"
              class="text-white hover:text-gray-200 cursor-pointer"
            >
              {{ dir }}
            </span>
            <ul 
              v-show="openDropdown === dir"
              class="absolute bg-white text-blue-500 mt-2 rounded shadow-lg"
            >
              <li v-for="file in files" :key="file" class="px-4 py-2 hover:bg-blue-100">
                <router-link :to="`/${dir}/${file}`">{{ file }}</router-link>
              </li>
            </ul>
          </div>
        </li>
      </template>
    </ul>
    <button 
      @click="toggleCampeonato"
      class="bg-white text-blue-500 px-4 py-2 rounded hover:bg-blue-100"
    >
      {{ campeonatoSeleccionado ? 'Salir del Campeonato' : 'Seleccionar Campeonato' }}
    </button>
  </nav>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'NavBar',
  props: ['campeonatoSeleccionado'],
  emits: ['toggle-seleccion-campeonato'],
  setup(props, { emit }) {
    const router = useRouter();
    const openDropdown = ref(null);
    let closeTimeout = null;

    const componentDirectories = {
      Partidas: ['Inicio', 'Ranking', 'Mesas'],
      Resultados: ['CierrePartida', 'Resultados', 'Registro_Partida']
    };

    const toggleDropdown = (dir) => {
      if (openDropdown.value === dir) {
        openDropdown.value = null;
      } else {
        openDropdown.value = dir;
      }
    };

    const closeDropdown = () => {
      closeTimeout = setTimeout(() => {
        openDropdown.value = null;
      }, 300); // 300ms de retraso antes de cerrar
    };

    const cancelCloseDropdown = () => {
      if (closeTimeout) {
        clearTimeout(closeTimeout);
      }
    };

    const toggleCampeonato = () => {
      if (props.campeonatoSeleccionado) {
        localStorage.removeItem('campeonato_id');
        localStorage.removeItem('campeonato_nombre');
        localStorage.removeItem('campeonato_partidas');
        emit('toggle-seleccion-campeonato', false);
        router.push('/');
      } else {
        emit('toggle-seleccion-campeonato', true);
      }
    };

    return {
      toggleCampeonato,
      componentDirectories,
      openDropdown,
      toggleDropdown,
      closeDropdown,
      cancelCloseDropdown
    };
  }
}
</script>
