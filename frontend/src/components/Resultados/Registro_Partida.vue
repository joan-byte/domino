<template>
  <div class="container mx-auto p-4">
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">Registro de Partidas</h1>
      <div class="text-xl font-semibold">
        Partida {{ partidaActual }}
      </div>
    </div>
    <div v-if="isLoading">Cargando mesas y parejas...</div>
    <div v-else-if="error">{{ error }}</div>
    <table v-else class="min-w-full bg-white border border-gray-300">
      <thead>
        <tr class="bg-gray-100">
          <th class="py-2 px-4 border-b text-center">Mesa</th>
          <th class="py-2 px-4 border-b text-center">Pareja 1 (ID)</th>
          <th class="py-2 px-4 border-b text-center">Pareja 2 (ID)</th>
          <th class="py-2 px-4 border-b text-center">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="mesa in mesasOrdenadas" :key="mesa.id" class="hover:bg-gray-50">
          <td class="py-2 px-4 border-b text-center font-bold">{{ mesa.id }}</td>
          <td class="py-2 px-4 border-b text-center">{{ mesa.pareja1_id }}</td>
          <td class="py-2 px-4 border-b text-center">{{ mesa.pareja2_id || 'N/A' }}</td>
          <td class="py-2 px-4 border-b text-center">
            <button 
              @click="registrarResultado(mesa)"
              :disabled="mesa.resultado_registrado"
              :class="[
                'px-2 py-1 rounded mr-2',
                mesa.resultado_registrado 
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed' 
                  : 'bg-green-500 text-white hover:bg-green-600'
              ]"
            >
              Registrar
            </button>
            <button 
              @click="modificarResultado(mesa)"
              :disabled="!mesa.resultado_registrado"
              :class="[
                'px-2 py-1 rounded',
                !mesa.resultado_registrado 
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed' 
                  : 'bg-blue-500 text-white hover:bg-blue-600'
              ]"
            >
              Modificar
            </button>
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
  name: 'RegistroPartida',
  setup() {
    const mesas = ref([]);
    const isLoading = ref(true);
    const error = ref(null);
    const partidaActual = ref(localStorage.getItem('partida_actual') || '1');

    const mesasOrdenadas = computed(() => {
      return [...mesas.value].sort((a, b) => a.id - b.id);
    });

    const fetchMesas = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/mesas-registro');
        mesas.value = response.data.map(mesa => ({
          ...mesa,
          resultado_registrado: false // Inicializamos esta propiedad
        }));
      } catch (e) {
        console.error('Error al obtener las mesas', e);
        error.value = 'Error al cargar las mesas. Por favor, intente de nuevo.';
      } finally {
        isLoading.value = false;
      }
    };

    const registrarResultado = (mesa) => {
      // Aquí iría la lógica para registrar el resultado
      console.log('Registrar resultado para mesa:', mesa.id);
      // Después de registrar el resultado:
      mesa.resultado_registrado = true;
    };

    const modificarResultado = (mesa) => {
      // Aquí iría la lógica para modificar el resultado
      console.log('Modificar resultado para mesa:', mesa.id);
    };

    onMounted(() => {
      fetchMesas();
    });

    return {
      mesasOrdenadas,
      isLoading,
      error,
      partidaActual,
      registrarResultado,
      modificarResultado
    };
  }
}
</script>
