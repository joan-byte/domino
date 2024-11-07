<template>
  <div class="container mx-auto p-4">
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">Parejas Inscritas</h1>
      <div class="flex space-x-4">
        <button 
          @click="toggleSorteo" 
          :class="[
            'px-4 py-2 rounded text-white',
            sorteoRealizado 
              ? 'bg-blue-500 hover:bg-blue-600' 
              : 'bg-red-500 hover:bg-red-600'
          ]"
        >
          {{ sorteoRealizado ? 'Volver Atrás' : 'Sorteo Inicial' }}
        </button>
        <button 
          @click="toggleInscripcion" 
          class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          :disabled="sorteoRealizado"
          :class="{'opacity-50 cursor-not-allowed': sorteoRealizado}"
        >
          {{ inscripcionAbierta ? 'Cerrar Inscripción' : 'Abrir Inscripción' }}
        </button>
      </div>
    </div>
    <div v-if="isLoading">Cargando parejas...</div>
    <div v-else-if="error">{{ error }}</div>
    <table v-else class="min-w-full bg-white border border-gray-300">
      <thead>
        <tr class="bg-gray-100">
          <th class="py-2 px-4 border-b text-left">ID</th>
          <th class="py-2 px-4 border-b text-left">Nombre</th>
          <th class="py-2 px-4 border-b text-left">Club</th>
          <th class="py-2 px-4 border-b text-center">Activa</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="pareja in parejas" :key="pareja.id" class="hover:bg-gray-50">
          <td class="py-2 px-4 border-b">{{ pareja.id }}</td>
          <td class="py-2 px-4 border-b">{{ pareja.nombre }}</td>
          <td class="py-2 px-4 border-b">{{ pareja.club || '-' }}</td>
          <td class="py-2 px-4 border-b text-center">
            <input 
              type="checkbox" 
              :id="`pareja-${pareja.id}`"
              :name="`pareja-${pareja.id}`"
              :checked="pareja.activa" 
              @change="toggleActiva(pareja)"
              class="form-checkbox h-5 w-5 text-blue-600"
            >
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { ref, onMounted, nextTick, onUnmounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  name: 'InicioParejas',
  setup() {
    const router = useRouter();
    const parejas = ref([]);
    const campeonatos = ref([]);
    const isLoading = ref(true);
    const error = ref(null);
    const inscripcionAbierta = ref(localStorage.getItem('inscripcionAbierta') === 'true');
    const sorteoRealizado = ref(localStorage.getItem('sorteoRealizado') === 'true');
    const inscripcionCerrada = ref(false); // Esto debería ser controlado por el estado de la inscripción
    const mesas = ref([]);

    const fetchParejas = async () => {
      try {
        const campeonatoId = localStorage.getItem('campeonato_id');
        if (!campeonatoId) {
          console.error('No hay un campeonato seleccionado');
          error.value = 'No hay un campeonato seleccionado. Por favor, seleccione un campeonato primero.';
          return;
        }
        isLoading.value = true;
        const response = await axios.get(`http://localhost:8000/api/campeonatos/${campeonatoId}/parejas`);
        parejas.value = response.data;
        console.log('Parejas obtenidas:', parejas.value);
      } catch (e) {
        console.error('Error al obtener las parejas', e);
        error.value = 'Error al cargar las parejas. Por favor, intente de nuevo.';
      } finally {
        isLoading.value = false;
      }
    };

    const fetchCampeonatos = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/campeonatos');
        campeonatos.value = response.data;
      } catch (e) {
        console.error('Error al obtener los campeonatos', e);
        error.value = 'Error al cargar los campeonatos. Por favor, intente de nuevo.';
      }
    };

    const toggleInscripcion = () => {
      inscripcionAbierta.value = !inscripcionAbierta.value;
      localStorage.setItem('inscripcionAbierta', inscripcionAbierta.value);
    };

    const toggleActiva = async (pareja) => {
      try {
        const response = await axios.patch(`http://localhost:8000/api/parejas/${pareja.id}`, {
          activa: !pareja.activa
        });
        if (response.data && response.data.activa !== undefined) {
          pareja.activa = response.data.activa;
        } else {
          throw new Error('La respuesta del servidor no contiene el campo activa');
        }
      } catch (e) {
        console.error('Error al actualizar el estado de la pareja', e);
        if (e.response && e.response.data) {
          console.error('Detalles del error:', e.response.data);
          alert(`Error al actualizar el estado de la pareja: ${JSON.stringify(e.response.data)}`);
        } else {
          alert('Error al actualizar el estado de la pareja. Por favor, intente de nuevo.');
        }
        // Revertir el cambio en la interfaz de usuario
        pareja.activa = !pareja.activa;
      }
    };

    const toggleSorteo = async () => {
      if (sorteoRealizado.value) {
        // Volver atrás
        try {
          await axios.delete('http://localhost:8000/api/partidas/sorteo-inicial');
          sorteoRealizado.value = false;
          mesas.value = [];
          inscripcionAbierta.value = true;
          localStorage.setItem('sorteoRealizado', 'false');
          localStorage.setItem('inscripcionAbierta', 'true');
          localStorage.removeItem('partida_actual');
          await fetchParejas();
        } catch (error) {
          console.error('Error al eliminar el sorteo:', error);
          alert('Error al eliminar el sorteo. Por favor, intente de nuevo.');
        }
      } else {
        // Realizar sorteo
        try {
          const response = await axios.post('http://localhost:8000/api/partidas/sorteo-inicial');
          mesas.value = response.data;
          sorteoRealizado.value = true;
          inscripcionAbierta.value = false;
          localStorage.setItem('sorteoRealizado', 'true');
          localStorage.setItem('inscripcionAbierta', 'false');
          localStorage.setItem('partida_actual', '1');
          await nextTick();
          router.push('/Partidas/Mesas');
        } catch (error) {
          console.error('Error al realizar el sorteo:', error);
          alert('Error al realizar el sorteo. Por favor, intente de nuevo.');
        }
      }
    };

    // Añade esta función para actualizar los datos periódicamente
    const startPeriodicUpdate = () => {
      const updateInterval = setInterval(fetchParejas, 30000); // Actualiza cada 30 segundos
      return () => clearInterval(updateInterval);
    };

    onMounted(() => {
      fetchParejas();
      const stopPeriodicUpdate = startPeriodicUpdate();
      onUnmounted(stopPeriodicUpdate);
    });

    return {
      parejas,
      campeonatos,
      isLoading,
      error,
      toggleActiva,
      inscripcionAbierta,
      toggleInscripcion,
      mesas,
      sorteoRealizado,
      toggleSorteo,
      inscripcionCerrada,
      fetchCampeonatos  // Añade esta línea
    };
  }
}
</script>

