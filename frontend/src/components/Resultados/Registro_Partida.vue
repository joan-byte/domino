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
              @click="irARegistroResultado(mesa)"
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
import { ref, onMounted, computed, watch } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  name: 'RegistroPartida',
  setup() {
    const router = useRouter();
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
        const mesasData = response.data;
        
        // Verificar si cada mesa tiene resultados
        for (let mesa of mesasData) {
          try {
            const resultadoCheck = await axios.get(`http://localhost:8000/api/resultados/mesa-tiene-resultados/${mesa.id}/${partidaActual.value}`);
            mesa.resultado_registrado = resultadoCheck.data.tiene_resultados;
          } catch (e) {
            console.error(`Error al verificar resultados para mesa ${mesa.id}:`, e);
            mesa.resultado_registrado = false;
          }
        }
        
        mesas.value = mesasData;
      } catch (e) {
        console.error('Error al obtener las mesas', e);
        error.value = 'Error al cargar las mesas. Por favor, intente de nuevo.';
      } finally {
        isLoading.value = false;
      }
    };

    const registrarResultado = async (mesa) => {
      try {
        // Validación de datos
        if (!mesa.pareja1_id || !partidaActual.value) {
          throw new Error('Datos incompletos para registrar el resultado');
        }

        const resultado = {
          campeonato_id: parseInt(localStorage.getItem('campeonato_id')),
          pareja1: {
            P: parseInt(partidaActual.value),
            M: mesa.id,
            id_pareja: mesa.pareja1_id,
            RP: 0, // Estos valores deberían ser ingresados por el usuario
            GB: "A",
            PG: 0,
            PP: 0
          }
        };

        if (mesa.pareja2_id) {
          resultado.pareja2 = {
            P: parseInt(partidaActual.value),
            M: mesa.id,
            id_pareja: mesa.pareja2_id,
            RP: 0, // Estos valores deberían ser ingresados por el usuario
            GB: "A",
            PG: 0,
            PP: 0
          };
        }

        console.log('Enviando resultado:', resultado);
        const response = await axios.post('http://localhost:8000/api/resultados/create', resultado);
        console.log('Respuesta del servidor:', response.data);

        if (response.status === 200 || response.status === 201) {
          mesa.resultado_registrado = true;
          alert('Resultado registrado con éxito');
        } else {
          throw new Error('Error al registrar el resultado');
        }
      } catch (e) {
        console.error('Error al registrar el resultado', e);
        alert(`Error al registrar el resultado: ${e.message}. Por favor, intente de nuevo.`);
      }
    };

    const modificarResultado = async (mesa) => {
      try {
        console.log(`Verificando resultados para mesa ${mesa.id} y partida ${partidaActual.value}`);
        const response = await axios.get(`http://localhost:8000/api/resultados/mesa-tiene-resultados/${mesa.id}/${partidaActual.value}`);
        const tieneResultados = response.data.tiene_resultados;
        console.log(`Tiene resultados: ${tieneResultados}`, response.data);
        
        if (!tieneResultados) {
          alert('No hay resultados para modificar. Por favor, registre un nuevo resultado.');
          return;
        }
        
        router.push({
          name: 'RegistroResultados',
          params: { 
            id: mesa.id.toString()
          },
          query: {
            partida: partidaActual.value.toString(),
            pareja1_id: mesa.pareja1_id ? mesa.pareja1_id.toString() : 'null',
            pareja2_id: mesa.pareja2_id ? mesa.pareja2_id.toString() : 'null',
            modificar: 'true',
            tieneResultados: 'true'
          }
        });
      } catch (error) {
        console.error('Error al verificar resultados:', error);
        if (error.response) {
          console.error('Respuesta del servidor:', error.response.data);
        }
        alert('Error al verificar resultados. Por favor, intente de nuevo.');
      }
    };

    const irARegistroResultado = (mesa) => {
      router.push({
        name: 'RegistroResultados',
        params: { 
          id: mesa.id.toString()
        },
        query: {
          partida: partidaActual.value.toString(),
          pareja1_id: mesa.pareja1_id ? mesa.pareja1_id.toString() : 'null',
          pareja2_id: mesa.pareja2_id ? mesa.pareja2_id.toString() : 'null'
        }
      });
    };

    watch(() => router.currentRoute.value, (newRoute) => {
      if (newRoute.name === 'RegistroPartida') {
        // Actualizar el estado de las mesas
        fetchMesas();
      }
    });

    onMounted(() => {
      fetchMesas();
    });

    return {
      mesasOrdenadas,
      isLoading,
      error,
      partidaActual,
      registrarResultado,
      modificarResultado,
      irARegistroResultado
    };
  }
}
</script>
