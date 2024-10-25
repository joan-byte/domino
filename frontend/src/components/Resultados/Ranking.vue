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
        <tr v-for="(pareja, index) in ranking" :key="pareja.pareja_id" class="hover:bg-gray-50">
          <td class="py-2 px-4 border-b text-center">{{ index + 1 }}</td>
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
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';

export default {
  name: 'RankingView',
  setup() {
    const ranking = ref([]);
    const isLoading = ref(true);
    const error = ref(null);

    const fetchRanking = async () => {
      try {
        const campeonatoId = localStorage.getItem('campeonato_id');
        if (!campeonatoId) {
          throw new Error('No hay un campeonato seleccionado');
        }
        const response = await axios.get(`http://localhost:8000/api/campeonatos/${campeonatoId}/ranking`);
        ranking.value = response.data;
        isLoading.value = false;
      } catch (e) {
        console.error('Error al cargar el ranking:', e);
        error.value = 'Error al cargar el ranking. Por favor, intente de nuevo.';
        isLoading.value = false;
      }
    };

    onMounted(fetchRanking);

    return {
      ranking,
      isLoading,
      error
    };
  }
}
</script>

<style scoped>
/* Aquí irán los estilos específicos del componente */
</style>
