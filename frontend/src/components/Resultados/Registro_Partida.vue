<template>
  <div class="container mx-auto p-4">
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">Registro de Partidas</h1>
      <div class="flex items-center">
        <button 
          v-if="todasParejasRegistradas"
          @click="finalizarPartida"
          class="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded mr-4"
        >
          {{ esUltimaPartida ? 'Cierre Campeonato' : 'Finalizar Partida' }}
        </button>
        <div class="text-xl font-semibold">
          Partida {{ partidaActual }}
        </div>
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
          <td class="py-2 px-4 border-b text-center font-bold">{{ mesa.numero }}</td>
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
    const campeonatoId = ref(localStorage.getItem('campeonato_id'));
    const numeroPartidasCampeonato = ref(parseInt(localStorage.getItem('campeonato_partidas') || '0'));

    const todasParejasRegistradas = computed(() => {
      return mesas.value.every(mesa => mesa.resultado_registrado);
    });

    const mesasOrdenadas = computed(() => {
      return [...mesas.value].sort((a, b) => a.numero - b.numero);
    });

    const esUltimaPartida = computed(() => {
      return parseInt(partidaActual.value) === numeroPartidasCampeonato.value;
    });

    const fetchMesas = async () => {
      try {
        isLoading.value = true;
        const response = await axios.get(`http://localhost:8000/api/campeonatos/${campeonatoId.value}/mesas-partida-actual`);
        const mesasData = response.data;
        
        // Verificar si cada mesa tiene resultados
        for (let mesa of mesasData) {
          try {
            const resultadoCheck = await axios.get(
              `http://localhost:8000/api/resultados/mesa/${mesa.id}/partida/${partidaActual.value}/tiene-resultados`,
              {
                params: {
                  campeonato_id: campeonatoId.value
                }
              }
            );
            mesa.resultado_registrado = resultadoCheck.data.tiene_resultados;
          } catch (e) {
            console.error(`Error al verificar resultados para mesa ${mesa.id}:`, e);
            mesa.resultado_registrado = false;
          }
        }
        
        mesas.value = mesasData;
        console.log('Mesas actualizadas:', mesas.value);
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
        const response = await axios.get(
          `http://localhost:8000/api/resultados/mesa-tiene-resultados/${mesa.id}/${partidaActual.value}`, 
          {
            params: {
              campeonato_id: campeonatoId.value
            }
          }
        );
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

    const finalizarPartida = async () => {
      try {
        // Verificar si es la penúltima partida
        const partidaActualNum = parseInt(partidaActual.value);
        const totalPartidas = parseInt(localStorage.getItem('campeonato_partidas'));
        
        if (partidaActualNum + 1 === totalPartidas) {
          // Obtener el ranking actual separado por grupos
          const rankingResponse = await axios.get(
            `http://localhost:8000/api/campeonatos/${campeonatoId.value}/ranking`
          );
          const ranking = rankingResponse.data;

          // Separar parejas por grupos
          const grupoA = ranking.filter(p => p.GB === 'A');
          const grupoB = ranking.filter(p => p.GB === 'B');

          // Función para verificar si una pareja debe jugar la última partida
          const debeJugarUltimaPartida = (primera, segunda) => {
            // Si la diferencia en PG es mayor a 1, la primera pareja no juega
            if (primera.PG - segunda.PG > 1) {
              return false;
            }
            
            // Solo verificar PP si la diferencia en PG es exactamente 1
            if (primera.PG - segunda.PG === 1) {
              // Si la diferencia en PP es mayor a 300, la primera pareja no juega
              if (primera.PP - segunda.PP > 300) {
                return false;
              }
            }
            
            // Si los PG son iguales o la diferencia de PP no es suficiente, se debe jugar
            return true;
          };

          // Verificar y ajustar PG para las parejas que no deben jugar
          const ajustarParejas = async (grupo) => {
            if (grupo.length >= 2) {
              const [primera, segunda] = grupo;
              if (!debeJugarUltimaPartida(primera, segunda)) {
                // Sumar un punto adicional a la primera pareja
                await axios.post(`http://localhost:8000/api/resultados/ajustar-pg`, {
                  pareja_id: primera.pareja_id,
                  campeonato_id: campeonatoId.value,
                  nuevo_pg: primera.PG + 1
                });
                
                // Marcar la pareja para que no sea incluida en la asignación de mesas
                primera.excluir_ultima_partida = true;
              }
            }
          };

          // Ajustar parejas para ambos grupos
          await ajustarParejas(grupoA);
          await ajustarParejas(grupoB);

          // Filtrar las parejas que deben jugar la última partida
          const parejasParaUltimaPartida = ranking.filter(p => !p.excluir_ultima_partida);

          // Calcular las nuevas asignaciones solo con las parejas que deben jugar
          const nuevasAsignaciones = calcularNuevasAsignaciones(parejasParaUltimaPartida);

          // Continuar con la lógica existente usando las nuevas asignaciones
          await axios.post(`http://localhost:8000/api/campeonatos/${campeonatoId.value}/asignar-mesas`, nuevasAsignaciones);
        }

        // Continuar con la lógica existente
        const rankingResponse = await axios.get(`http://localhost:8000/api/campeonatos/${campeonatoId.value}/ranking`);
        const ranking = rankingResponse.data;

        if (esUltimaPartida.value) {
          router.push({
            path: '/resultados/podium',
            query: { mostrar: 'true' }
          });
          return;
        }

        // 2. Calcular las nuevas asignaciones de mesas
        const nuevasAsignaciones = calcularNuevasAsignaciones(ranking);

        // 3. Actualizar la partida actual en el backend
        const nuevaPartida = parseInt(partidaActual.value) + 1;
        await axios.put(`http://localhost:8000/api/campeonatos/${campeonatoId.value}/partida_actual`, {
          partida_actual: nuevaPartida
        });

        // 4. Actualizar las asignaciones de mesas en el backend
        await axios.post(`http://localhost:8000/api/campeonatos/${campeonatoId.value}/asignar-mesas`, nuevasAsignaciones);

        // 5. Actualizar el localStorage y el estado local
        localStorage.setItem('partida_actual', nuevaPartida.toString());
        partidaActual.value = nuevaPartida.toString();

        // 6. Recargar los datos de las mesas
        await fetchMesas();

        alert('Partida finalizada. Se han asignado nuevas mesas para la siguiente partida.');
      } catch (error) {
        console.error('Error al finalizar la partida:', error);
        alert('Error al finalizar la partida. Por favor, intente de nuevo.');
      }
    };

    const calcularNuevasAsignaciones = (ranking) => {
      const nuevasAsignaciones = [];
      for (let i = 0; i < ranking.length; i += 2) {
        const mesaNumero = Math.ceil((i + 1) / 2);
        nuevasAsignaciones.push({
          mesa: mesaNumero,
          pareja1_id: ranking[i].pareja_id,
          pareja2_id: ranking[i + 1] ? ranking[i + 1].pareja_id : null
        });
      }
      return nuevasAsignaciones;
    };

    onMounted(() => {
      fetchMesas();
    });

    // Agregar un watcher para partidaActual
    watch(partidaActual, () => {
      fetchMesas();
    });

    // Agregar un watcher para la ruta
    watch(() => router.currentRoute.value, (newRoute) => {
      if (newRoute.name === 'RegistroPartida') {
        fetchMesas();
      }
    });

    return {
      mesas,
      mesasOrdenadas,
      isLoading,
      error,
      partidaActual,
      todasParejasRegistradas,
      finalizarPartida,
      registrarResultado,
      modificarResultado,
      irARegistroResultado,
      esUltimaPartida,
    };
  }
}
</script>
