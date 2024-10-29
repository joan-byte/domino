<template>
  <div class="container mx-auto p-4">
    <h1 class="text-3xl font-bold text-center mb-8">Podium del Campeonato</h1>
    
    <!-- Podium Section siempre visible pero sin datos -->
    <div class="flex justify-center items-end mb-12 space-x-8">
      <!-- Segundo lugar -->
      <div class="flex flex-col items-center">
        <div class="bg-gray-200 p-4 rounded-t-lg w-80">
          <p class="text-center font-bold">2° Lugar</p>
          <p class="text-center text-xl font-semibold" :class="mostrarPodium ? 'text-gray-800' : 'text-gray-400'">
            {{ mostrarPodium ? (podium[1]?.nombre_pareja || 'N/A') : 'Pendiente' }}
          </p>
        </div>
        <div class="bg-silver h-16 w-80"></div>
      </div>
      
      <!-- Primer lugar -->
      <div class="flex flex-col items-center">
        <div class="bg-gray-200 p-4 rounded-t-lg w-80">
          <p class="text-center font-bold">🏆 Campeón</p>
          <p class="text-center text-2xl font-bold" :class="mostrarPodium ? 'text-gray-900' : 'text-gray-400'">
            {{ mostrarPodium ? (podium[0]?.nombre_pareja || 'N/A') : 'Pendiente' }}
          </p>
        </div>
        <div class="bg-gold h-24 w-80"></div>
      </div>
      
      <!-- Tercer lugar -->
      <div class="flex flex-col items-center">
        <div class="bg-gray-200 p-4 rounded-t-lg w-80">
          <p class="text-center font-bold">3° Lugar</p>
          <p class="text-center text-lg font-medium" :class="mostrarPodium ? 'text-gray-700' : 'text-gray-400'">
            {{ mostrarPodium ? (podium[2]?.nombre_pareja || 'N/A') : 'Pendiente' }}
          </p>
        </div>
        <div class="bg-bronze h-12 w-80"></div>
      </div>
    </div>

    <!-- Ranking List -->
    <div class="mt-8">
      <h2 class="text-2xl font-bold mb-4">Ranking Final</h2>
      <table class="min-w-full bg-white">
        <thead>
          <tr>
            <th class="px-4 py-2">Posición</th>
            <th class="px-4 py-2">Pareja</th>
            <th class="px-4 py-2">PG</th>
            <th class="px-4 py-2">PP</th>
          </tr>
        </thead>
        <tbody>
          <!-- Solo mostrar datos si mostrarPodium es true -->
          <tr v-if="!mostrarPodium">
            <td colspan="4" class="px-4 py-8 text-center text-gray-500">
              El ranking se mostrará cuando finalice el campeonato
            </td>
          </tr>
          <tr v-else v-for="pareja in parejasVisibles" :key="pareja.pareja_id">
            <td class="px-4 py-2 text-center">{{ pareja.posicion }}</td>
            <td class="px-4 py-2">{{ pareja.nombre_pareja }}</td>
            <td class="px-4 py-2 text-center">{{ pareja.PG }}</td>
            <td class="px-4 py-2 text-center">{{ pareja.PP }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed, onUnmounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

export default {
  name: 'PodiumView',
  setup() {
    const route = useRoute();
    const ranking = ref([]);
    const startIndex = ref(3);
    const isLoading = ref(true);
    const error = ref(null);
    const campeonatoId = ref(localStorage.getItem('campeonato_id'));
    const mostrarPodium = ref(false);

    const podium = computed(() => ranking.value.slice(0, 3));
    
    const parejasVisibles = computed(() => {
      return ranking.value
        .slice(startIndex.value, startIndex.value + 15)
        .map((pareja, index) => ({
          ...pareja,
          posicion: startIndex.value + index + 1
        }));
    });

    const fetchRanking = async () => {
      try {
        isLoading.value = true;
        const response = await axios.get(`http://localhost:8000/api/campeonatos/${campeonatoId.value}/ranking`);
        ranking.value = response.data;
      } catch (e) {
        console.error('Error al obtener el ranking', e);
        error.value = 'Error al cargar el ranking';
      } finally {
        isLoading.value = false;
      }
    };

    const actualizarParejasMostradas = () => {
      startIndex.value += 15;
      if (startIndex.value >= ranking.value.length) {
        startIndex.value = 3;
      }
    };

    let intervalId;

    onMounted(() => {
      // Solo mostrar y cargar datos si viene desde el botón de cierre
      mostrarPodium.value = route.query.mostrar === 'true';
      if (mostrarPodium.value) {
        fetchRanking();
        intervalId = setInterval(actualizarParejasMostradas, 10000);
      }
    });

    onUnmounted(() => {
      if (intervalId) clearInterval(intervalId);
    });

    return {
      podium,
      parejasVisibles,
      isLoading,
      error,
      mostrarPodium
    };
  }
};
</script>

<style scoped>
.bg-gold {
  background-color: #1E40AF;
}
.bg-silver {
  background-color: #3B82F6;
}
.bg-bronze {
  background-color: #93C5FD;
}
</style>

