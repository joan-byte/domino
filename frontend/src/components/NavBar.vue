<template>
  <nav class="bg-blue-500 p-4">
    <div class="container mx-auto px-8 flex justify-between items-center">
      <div class="ml-4">
        <router-link to="/" class="text-white hover:text-gray-200 text-xl font-bold">Home</router-link>
      </div>
      <ul class="flex space-x-6 items-center mr-4">
        <li v-if="!campeonatoSeleccionado"><router-link to="/campeonatos" class="text-white hover:text-gray-200 text-lg font-semibold">Campeonatos</router-link></li>
        <li v-if="campeonatoSeleccionado"><router-link to="/inscripcion" class="text-white hover:text-gray-200 text-lg font-semibold">Inscripción</router-link></li>
        <template v-if="campeonatoSeleccionado">
          <li v-for="(files, dir) in componentDirectories" :key="dir" class="relative">
            <div @mouseleave="closeDropdown" @mouseenter="cancelCloseDropdown">
              <span 
                @click="toggleDropdown(dir)"
                class="text-white hover:text-gray-200 cursor-pointer text-lg font-semibold"
              >
                {{ dir }}
              </span>
              <ul 
                v-show="openDropdown === dir"
                class="absolute bg-white text-blue-500 mt-2 rounded shadow-lg"
              >
                <li v-for="file in visibleFiles(dir, files)" :key="file" class="px-4 py-2 hover:bg-blue-100">
                  <router-link :to="`/${dir}/${file}`" class="text-base font-medium">{{ file }}</router-link>
                </li>
              </ul>
            </div>
          </li>
        </template>
      </ul>
    </div>
  </nav>
</template>

<script>
import { ref } from 'vue';

export default {
  name: 'NavBar',
  props: ['campeonatoSeleccionado'],
  emits: ['toggle-seleccion-campeonato'],
  setup() {
    const openDropdown = ref(null);
    let closeTimeout = null;

    const componentDirectories = {
      Partidas: ['Inicio', 'Mesas'],
      Resultados: ['CierrePartida', 'Resultados', 'Registro_Partida', 'Ranking']
    };

    const visibleFiles = (dir, files) => {
      if (dir === 'Resultados') {
        return files.filter(file => file !== 'Resultados');
      }
      return files;
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
      }, 300);
    };

    const cancelCloseDropdown = () => {
      if (closeTimeout) {
        clearTimeout(closeTimeout);
      }
    };

    return {
      componentDirectories,
      openDropdown,
      toggleDropdown,
      closeDropdown,
      cancelCloseDropdown,
      visibleFiles
    };
  }
}
</script>
