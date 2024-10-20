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
          <th class="py-2 px-4 border-b text-center">Mesa Asignada</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="pareja in parejasOrdenadas" :key="pareja.id" class="hover:bg-gray-50">
          <td class="py-2 px-4 border-b text-center font-bold">{{ pareja.id }}</td>
          <td class="py-2 px-4 border-b">{{ pareja.nombre }}</td>
          <td class="py-2 px-4 border-b text-center font-bold" :class="pareja.mesa_asignada ? 'text-green-600' : 'text-red-600'">
            {{ pareja.mesa_asignada || 'Sin asignar' }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

export default {
  name: 'ParejasYMesasAsignadas',
  setup() {
    const parejas = ref([]);
    const isLoading = ref(true);
    const error = ref(null);
    const partidaActual = ref(localStorage.getItem('partida_actual') || '1');

    const parejasOrdenadas = computed(() => {
      return [...parejas.value].sort((a, b) => {
        if (a.mesa_asignada === null && b.mesa_asignada !== null) return 1;
        if (a.mesa_asignada !== null && b.mesa_asignada === null) return -1;
        if (a.mesa_asignada === b.mesa_asignada) return a.id - b.id;
        return (a.mesa_asignada || 0) - (b.mesa_asignada || 0);
      });
    });

    const fetchParejasYMesas = async () => {
      try {
        const campeonatoId = localStorage.getItem('campeonato_id');
        if (!campeonatoId) {
          throw new Error('No hay un campeonato seleccionado');
        }
        const response = await axios.get(`http://localhost:8000/api/parejas-mesas/${campeonatoId}`);
        parejas.value = response.data;
      } catch (e) {
        console.error('Error al obtener las parejas y mesas', e);
        if (e.response) {
          console.error('Respuesta del servidor:', e.response.data);
          error.value = `Error del servidor: ${e.response.status} - ${e.response.data.detail || 'Error desconocido'}`;
        } else if (e.request) {
          error.value = 'No se pudo conectar con el servidor. Por favor, verifica tu conexión a internet.';
        } else {
          error.value = `Error al cargar las parejas y mesas: ${e.message}`;
        }
      } finally {
        isLoading.value = false;
      }
    };

    onMounted(() => {
      fetchParejasYMesas();
    });

    return {
      parejas,
      isLoading,
      error,
      partidaActual,
      parejasOrdenadas
    };
  }
}
</script>
