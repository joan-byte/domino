<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Ranking del Campeonato</h1>
    <div v-if="isLoading">Cargando ranking...</div>
    <div v-else-if="error">{{ error }}</div>
    <table v-else class="min-w-full bg-white border border-gray-300">
      <thead>
        <tr class="bg-gray-100">
          <th class="py-2 px-4 border-b">Posición</th>
          <th class="py-2 px-4 border-b">Partida</th>
          <th class="py-2 px-4 border-b">GB</th>
          <th class="py-2 px-4 border-b">PG</th>
          <th class="py-2 px-4 border-b">PP</th>
          <th class="py-2 px-4 border-b">ID Pareja</th>
          <th class="py-2 px-4 border-b">Nombre Pareja</th>
          <th class="py-2 px-4 border-b">Club</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="pareja in parejasVisibles" :key="pareja.pareja_id" class="hover:bg-gray-50">
          <td class="py-2 px-4 border-b text-center">{{ pareja.posicion }}</td>
          <td class="py-2 px-4 border-b text-center">{{ pareja.partida }}</td>
          <td class="py-2 px-4 border-b text-center">{{ pareja.GB }}</td>
          <td class="py-2 px-4 border-b text-center">{{ pareja.PG }}</td>
          <td class="py-2 px-4 border-b text-center">{{ pareja.PP }}</td>
          <td class="py-2 px-4 border-b text-center">{{ pareja.pareja_id }}</td>
          <td class="py-2 px-4 border-b">{{ pareja.nombre_pareja }}</td>
          <td class="py-2 px-4 border-b">{{ pareja.club || 'N/A' }}</td>
        </tr>
      </tbody>
    </table>
    <div class="mt-4 text-center">
      Mostrando parejas {{ startIndex + 1 }} - {{ Math.min(startIndex + 20, ranking.length) }} de {{ ranking.length }}
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue';
import axios from 'axios';

export default {
  name: 'RankingCampeonato',
  setup() {
    const ranking = ref([]);
    const isLoading = ref(true);
    const error = ref(null);
    const startIndex = ref(0);

    const parejasVisibles = computed(() => {
      return ranking.value.slice(startIndex.value, startIndex.value + 20);
    });

    const fetchRanking = async () => {
      try {
        isLoading.value = true;
        const campeonatoId = localStorage.getItem('campeonato_id');
        if (!campeonatoId) {
          throw new Error('No hay un campeonato seleccionado');
        }
        const response = await axios.get(`http://localhost:8000/api/campeonatos/${campeonatoId}/ranking`);
        ranking.value = response.data;
        error.value = null;
      } catch (e) {
        console.error('Error al obtener el ranking:', e);
        error.value = 'Error al cargar el ranking. Por favor, intente de nuevo.';
      } finally {
        isLoading.value = false;
      }
    };

    const actualizarParejasMostradas = () => {
      startIndex.value += 20;
      if (startIndex.value >= ranking.value.length) {
        startIndex.value = 0;
      }
      fetchRanking();
    };

    let intervalId;

    onMounted(() => {
      fetchRanking();
      intervalId = setInterval(actualizarParejasMostradas, 10000); // Actualiza cada 10 segundos
    });

    onUnmounted(() => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    });

    watch(ranking, (newRanking) => {
      if (startIndex.value >= newRanking.length) {
        startIndex.value = 0;
      }
    });

    return {
      ranking,
      isLoading,
      error,
      startIndex,
      parejasVisibles
    };
  }
};
</script>
