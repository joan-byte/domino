<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Bienvenido</h1>
    <h2 class="text-xl font-semibold mb-2">Campeonatos Registrados</h2>
    <div v-if="isLoading">Cargando...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="campeonato in campeonatos" :key="campeonato.id" 
           class="campeonato-card">
        <h3 class="text-lg font-semibold mb-2">{{ campeonato.nombre }}</h3>
        <p class="text-sm text-gray-600 mb-1">Fecha de inicio: {{ formatDate(campeonato.fecha_inicio) }}</p>
        <p class="text-sm text-gray-600 mb-1">Duración: {{ campeonato.dias_duracion }} días</p>
        <p class="text-sm text-gray-600">Número de partidas: {{ campeonato.numero_partidas }}</p>
        <p class="text-sm text-gray-600">Grupo: {{ campeonato.grupo_b ? 'B' : 'A' }}</p>
        <div class="mt-4 flex justify-between">
          <button @click="modificarCampeonato(campeonato)" class="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded">
            Modificar
          </button>
          <button @click="seleccionarOSalirCampeonato(campeonato)" :class="buttonClass(campeonato)">
            {{ buttonText(campeonato) }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import '@/assets/CampeonatoCard.css';

const api = axios.create({
  baseURL: 'http://localhost:8000'
});

export default {
  name: 'HomeView',
  props: {
    seleccionandoCampeonato: {
      type: Boolean,
      default: false
    }
  },
  emits: ['campeonato-seleccionado'],
  setup(props, { emit }) {
    const campeonatos = ref([]);
    const isLoading = ref(false);
    const error = ref(null);
    const router = useRouter();
    const campeonatoSeleccionadoId = ref(localStorage.getItem('campeonato_id') || null);

    const fetchCampeonatos = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/campeonatos');
        campeonatos.value = response.data;
      } catch (e) {
        console.error('Error al obtener los campeonatos', e);
        error.value = 'Error al cargar los campeonatos. Por favor, intente de nuevo.';
      }
    };

    const formatDate = (dateString) => {
      if (!dateString) return 'No especificada';
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('es-ES', options);
    };

    const modificarCampeonato = (campeonato) => {
      router.push({ name: 'Campeonatos', params: { id: campeonato.id } });
    };

    const seleccionarOSalirCampeonato = async (campeonato) => {
      if (campeonatoSeleccionadoId.value !== campeonato.id.toString()) {
        // Seleccionar campeonato
        try {
          const campeonatoResponse = await api.get(`/api/campeonatos/${campeonato.id}`);
          const campeonatoData = campeonatoResponse.data;

          localStorage.setItem('campeonato_id', campeonatoData.id.toString());
          localStorage.setItem('campeonato_nombre', campeonatoData.nombre);
          localStorage.setItem('campeonato_partidas', campeonatoData.numero_partidas.toString());
          localStorage.setItem('campeonato_grupo', campeonatoData.grupo_b ? 'B' : 'A');

          // Usar el campo partida_actual del campeonato
          if (campeonatoData.partida_actual > 0) {
            localStorage.setItem('partida_actual', campeonatoData.partida_actual.toString());
            localStorage.setItem('inscripcionAbierta', 'false');
            localStorage.setItem('sorteoRealizado', 'true');
          } else {
            localStorage.removeItem('partida_actual');
            localStorage.setItem('inscripcionAbierta', 'true');
            localStorage.setItem('sorteoRealizado', 'false');
          }

          campeonatoSeleccionadoId.value = campeonatoData.id.toString();
          emit('campeonato-seleccionado', true);
        } catch (error) {
          console.error('Error al cargar los datos del campeonato', error);
          alert('Error al cargar los datos del campeonato. Por favor, intente de nuevo.');
        }
      } else {
        // Salir del campeonato
        localStorage.clear();
        campeonatoSeleccionadoId.value = null;
        emit('campeonato-seleccionado', false);
      }
      router.push('/');
    };

    const buttonText = (campeonato) => {
      return campeonatoSeleccionadoId.value === campeonato.id.toString() ? 'Salir del campeonato' : 'Seleccionar';
    };

    const buttonClass = (campeonato) => {
      return campeonatoSeleccionadoId.value === campeonato.id.toString()
        ? 'bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded'
        : 'bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded';
    };

    onMounted(() => {
      fetchCampeonatos();
    });

    watch(() => localStorage.getItem('campeonato_id'), (newValue) => {
      campeonatoSeleccionadoId.value = newValue || null;
    }, { immediate: true });

    return {
      campeonatos,
      isLoading,
      error,
      formatDate,
      modificarCampeonato,
      seleccionarOSalirCampeonato,
      campeonatoSeleccionadoId,
      buttonText,
      buttonClass
    };
  }
}
</script>

