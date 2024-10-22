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
          <th class="py-2 px-4 border-b text-center">Posición</th>
          <th class="py-2 px-4 border-b text-center">ID Pareja</th>
          <th class="py-2 px-4 border-b text-left">Nombre Pareja</th>
          <th class="py-2 px-4 border-b text-center">Mesa Asignada</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(pareja, index) in parejasMesas" :key="pareja.pareja_id" class="hover:bg-gray-50">
          <td class="py-2 px-4 border-b text-center">{{ index + 1 }}</td>
          <td class="py-2 px-4 border-b text-center font-bold">{{ pareja.pareja_id }}</td>
          <td class="py-2 px-4 border-b">{{ pareja.nombre_pareja }}</td>
          <td class="py-2 px-4 border-b text-center font-bold text-green-600">
            {{ pareja.mesa_asignada }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';

export default {
  name: 'MesasAsignadas',  // Cambiado de 'Mesas' a 'MesasAsignadas'
  setup() {
    const parejasMesas = ref([]);
    const isLoading = ref(true);
    const error = ref(null);
    const partidaActual = ref(localStorage.getItem('partida_actual') || '1');
    const campeonatoId = ref(localStorage.getItem('campeonato_id'));

    const fetchParejasMesas = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/campeonatos/${campeonatoId.value}/parejas-mesas`);
        parejasMesas.value = response.data;
      } catch (e) {
        console.error('Error al obtener parejas y mesas', e);
        error.value = 'Error al cargar parejas y mesas. Por favor, intente de nuevo.';
      } finally {
        isLoading.value = false;
      }
    };

    onMounted(() => {
      fetchParejasMesas();
    });

    return {
      parejasMesas,
      isLoading,
      error,
      partidaActual
    };
  }
}
</script>

