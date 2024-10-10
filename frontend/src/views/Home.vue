<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Bienvenido</h1>
    <h2 class="text-xl font-semibold mb-2">Campeonatos Registrados</h2>
    <div v-if="isLoading">Cargando...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="campeonato in campeonatos" :key="campeonato.id" 
           @click="handleCampeonatoClick(campeonato)"
           :class="['campeonato-card', { 'campeonato-card-selected': campeonato.id.toString() === campeonatoSeleccionadoId }]">
        <h3 class="text-lg font-semibold mb-2">{{ campeonato.nombre }}</h3>
        <p class="text-sm text-gray-600 mb-1">Fecha de inicio: {{ formatDate(campeonato.fecha_inicio) }}</p>
        <p class="text-sm text-gray-600 mb-1">Duración: {{ campeonato.dias_duracion }} días</p>
        <p class="text-sm text-gray-600">Número de partidas: {{ campeonato.numero_partidas }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, computed } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import '@/assets/CampeonatoCard.css';

const api = axios.create({
  baseURL: 'http://localhost:8000'
});

export default {
  name: 'HomeView',
  props: ['seleccionandoCampeonato'],
  emits: ['campeonato-seleccionado'],
  setup(props, { emit }) {
    const campeonatos = ref([]);
    const isLoading = ref(false);
    const error = ref(null);
    const router = useRouter();
    const campeonatoSeleccionadoId = ref(localStorage.getItem('campeonato_id') || null);

    const hayCampeonatoSeleccionado = computed(() => {
      return !!localStorage.getItem('campeonato_id');
    });

    const fetchCampeonatos = async () => {
      isLoading.value = true;
      error.value = null;
      try {
        const response = await api.get('/api/campeonatos/');
        campeonatos.value = response.data;
      } catch (err) {
        console.error('Error al cargar los campeonatos:', err);
        if (err.response) {
          error.value = `Error del servidor: ${err.response.status} - ${err.response.data.detail || 'Error desconocido'}`;
        } else if (err.request) {
          error.value = 'No se pudo conectar con el servidor. Por favor, verifica tu conexión a internet.';
        } else {
          error.value = `Error al procesar la solicitud: ${err.message}`;
        }
      } finally {
        isLoading.value = false;
      }
    };

    const formatDate = (dateString) => {
      if (!dateString) return 'No especificada';
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('es-ES', options);
    };

    const handleCampeonatoClick = (campeonato) => {
      if (props.seleccionandoCampeonato) {
        localStorage.setItem('campeonato_id', campeonato.id.toString());
        localStorage.setItem('campeonato_nombre', campeonato.nombre);
        localStorage.setItem('campeonato_partidas', campeonato.numero_partidas.toString());
        campeonatoSeleccionadoId.value = campeonato.id.toString();
        emit('campeonato-seleccionado', true);
      } else {
        router.push({ name: 'Campeonatos', params: { id: campeonato.id } });
      }
    };

    const updateSelectedCampeonato = () => {
      campeonatoSeleccionadoId.value = localStorage.getItem('campeonato_id') || null;
    };

    onMounted(() => {
      fetchCampeonatos();
      updateSelectedCampeonato();
    });

    watch(() => localStorage.getItem('campeonato_id'), (newValue) => {
      campeonatoSeleccionadoId.value = newValue || null;
    }, { immediate: true });

    // Observar cambios en la ruta
    watch(() => router.currentRoute.value.fullPath, () => {
      updateSelectedCampeonato();
    });

    return {
      campeonatos,
      isLoading,
      error,
      formatDate,
      handleCampeonatoClick,
      campeonatoSeleccionadoId,
      hayCampeonatoSeleccionado
    };
  }
}
</script>
