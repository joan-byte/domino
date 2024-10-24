<template>
  <div class="container mx-auto p-4">
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">Parejas y Mesas Asignadas</h1>
      <div class="text-xl font-semibold">
        Partida {{ partidaActual }}
      </div>
    </div>
    <div v-if="isLoading">Cargando parejas y mesas...</div>
    <div v-else-if="error">{{ error }}</div>
    <table v-else class="min-w-full bg-white border border-gray-300">
      <thead>
        <tr class="bg-gray-100">
          <th class="py-2 px-4 border-b text-center">ID Pareja</th>
          <th class="py-2 px-4 border-b text-left">Nombre Pareja</th>
          <th class="py-2 px-4 border-b text-center">Club</th>
          <th class="py-2 px-4 border-b text-center">Mesa Asignada</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="pareja in parejasVisibles" :key="pareja.id" class="hover:bg-gray-50">
          <td class="py-2 px-4 border-b text-center font-bold">{{ pareja.id }}</td>
          <td class="py-2 px-4 border-b">{{ pareja.nombre }}</td>
          <td class="py-2 px-4 border-b text-center">{{ pareja.club || 'N/A' }}</td>
          <td class="py-2 px-4 border-b text-center font-bold text-green-600">
            {{ pareja.mesa }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import axios from 'axios';

export default {
  name: 'MesasAsignadas',
  setup() {
    const parejas = ref([]);
    const isLoading = ref(true);
    const error = ref(null);
    const partidaActual = ref(localStorage.getItem('partida_actual') || '1');
    const campeonatoId = ref(localStorage.getItem('campeonato_id'));
    const startIndex = ref(0);
    const intervalId = ref(null);

    const parejasOrdenadas = computed(() => {
      return [...parejas.value].sort((a, b) => a.mesa - b.mesa);
    });

    const parejasVisibles = computed(() => {
      return parejasOrdenadas.value.slice(startIndex.value, startIndex.value + 20);
    });

    const fetchParejasMesas = async () => {
      try {
        isLoading.value = true;
        const response = await axios.get(`http://localhost:8000/api/mesas-asignadas/${campeonatoId.value}`);
        parejas.value = response.data;
        console.log('Parejas y mesas actualizadas:', parejas.value);
      } catch (e) {
        console.error('Error al obtener las parejas y mesas', e);
        error.value = 'Error al cargar las parejas y mesas. Por favor, intente de nuevo.';
      } finally {
        isLoading.value = false;
      }
    };

    const startAutoPagination = () => {
      intervalId.value = setInterval(() => {
        startIndex.value += 20;
        if (startIndex.value >= parejas.value.length) {
          startIndex.value = 0; // Reiniciar al inicio
        }
      }, 10000); // Cambiar cada 10 segundos
    };

    const stopAutoPagination = () => {
      if (intervalId.value) {
        clearInterval(intervalId.value);
      }
    };

    onMounted(() => {
      fetchParejasMesas();
      startAutoPagination();
    });

    onUnmounted(() => {
      stopAutoPagination();
    });

    return {
      parejasVisibles,
      isLoading,
      error,
      partidaActual
    };
  }
}
</script>
