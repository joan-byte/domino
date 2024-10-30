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
        <div class="bg-silver h-16 w-80 flex flex-col justify-center items-center text-white">
          <div>Partidas Ganadas: {{ mostrarPodium ? (podium[1]?.PG || '0') : '-' }}</div>
          <div>Puntos Totales: {{ mostrarPodium ? (podium[1]?.PP || '0') : '-' }}</div>
        </div>
      </div>
      
      <!-- Primer lugar -->
      <div class="flex flex-col items-center">
        <div class="bg-gray-200 p-4 rounded-t-lg w-80">
          <p class="text-center font-bold">🏆 Campeón</p>
          <p class="text-center text-2xl font-bold" :class="mostrarPodium ? 'text-gray-900' : 'text-gray-400'">
            {{ mostrarPodium ? (podium[0]?.nombre_pareja || 'N/A') : 'Pendiente' }}
          </p>
        </div>
        <div class="bg-gold h-24 w-80 flex flex-col justify-center items-center text-white">
          <div>Partidas Ganadas: {{ mostrarPodium ? (podium[0]?.PG || '0') : '-' }}</div>
          <div>Puntos Totales: {{ mostrarPodium ? (podium[0]?.PP || '0') : '-' }}</div>
        </div>
      </div>
      
      <!-- Tercer lugar -->
      <div class="flex flex-col items-center">
        <div class="bg-gray-200 p-4 rounded-t-lg w-80">
          <p class="text-center font-bold">3° Lugar</p>
          <p class="text-center text-lg font-medium" :class="mostrarPodium ? 'text-gray-700' : 'text-gray-400'">
            {{ mostrarPodium ? (podium[2]?.nombre_pareja || 'N/A') : 'Pendiente' }}
          </p>
        </div>
        <div class="bg-bronze h-12 w-80 flex flex-col justify-center items-center text-white">
          <div class="text-sm">Partidas Ganadas: {{ mostrarPodium ? (podium[2]?.PG || '0') : '-' }}</div>
          <div class="text-sm">Puntos Totales: {{ mostrarPodium ? (podium[2]?.PP || '0') : '-' }}</div>
        </div>
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
            <th class="px-4 py-2">Partidas Ganadas</th>
            <th class="px-4 py-2">Puntos Totales</th>
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
import { ref, onMounted, computed, onUnmounted, watch } from 'vue';
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
        // Primero intentamos obtener el ranking final
        const responseFinal = await axios.get(`http://localhost:8000/api/campeonatos/${campeonatoId.value}/ranking-final`);
        
        if (responseFinal.data && responseFinal.data.length > 0) {
          console.log('Ranking final encontrado:', responseFinal.data);
          ranking.value = responseFinal.data;
          mostrarPodium.value = true;
        } else if (route.query.mostrar === 'true') {
          // Si no hay ranking final pero venimos del cierre de campeonato,
          // obtenemos el ranking actual y cerramos el campeonato
          console.log('Cerrando campeonato...');
          const currentRanking = await axios.get(`http://localhost:8000/api/campeonatos/${campeonatoId.value}/ranking`);
          
          // Guardar el ranking actual
          ranking.value = currentRanking.data;
          mostrarPodium.value = true;

          // Cerrar el campeonato
          await axios.post(`http://localhost:8000/api/campeonatos/${campeonatoId.value}/cerrar-campeonato`);
          console.log('Campeonato cerrado exitosamente');
        } else {
          console.log('No hay ranking final y no es cierre de campeonato');
          ranking.value = [];
          mostrarPodium.value = false;
        }
      } catch (e) {
        console.error('Error al obtener el ranking:', e);
        error.value = 'Error al cargar el ranking';
        mostrarPodium.value = false;
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

    // Observar cambios en la query del route
    watch(() => route.query.mostrar, (newValue) => {
      if (newValue === 'true') {
        console.log('Query mostrar cambió a true, actualizando ranking...');
        fetchRanking();
      }
    });

    onMounted(async () => {
      console.log('Componente montado, obteniendo ranking inicial...');
      await fetchRanking();
      
      if (mostrarPodium.value) {
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

