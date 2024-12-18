<template>
  <div class="container mx-auto p-4 bg-gray-100 rounded-lg shadow-md">
    <h1 class="text-3xl font-bold mb-4">Partida {{ partidaActual }} - Mesa {{ mesaNumero }} - GB {{ grupoB }}</h1>
    
    <div v-if="!isModificando" class="mb-4 bg-blue-100 border-l-4 border-blue-500 text-blue-700 p-4" role="alert">
      <p class="font-bold">Nuevo registro</p>
      <p>No hay resultados previos para esta mesa y partida. Por favor, ingrese los nuevos resultados.</p>
    </div>

    <div v-for="(pareja, index) in [pareja1, pareja2]" :key="index" class="mb-4 bg-white p-4 rounded-lg shadow">
      <div class="flex items-center justify-between">
        <h2 class="text-2xl font-semibold">Pareja {{ pareja.id_pareja }}</h2>
        <p class="text-2xl font-semibold">{{ pareja.nombre }}</p>
        <div class="flex items-center space-x-4">
          <div v-if="pareja.RP > 0 || isModificando">
            <span class="font-bold">PG:</span>
            <input 
              v-model="pareja.PG"
              :id="`pg-pareja-${index}`"
              :name="`pg-pareja-${index}`"
              type="number"
              min="0"
              max="1"
              readonly
              class="w-24 px-2 py-1 border rounded"
            >
          </div>
          <div v-if="pareja.RP > 0 || isModificando">
            <span class="font-bold">PP:</span>
            <input 
              v-model="pareja.PP"
              :id="`pp-pareja-${index}`"
              :name="`pp-pareja-${index}`"
              type="number"
              readonly
              class="w-24 px-2 py-1 border rounded"
            >
          </div>
          <div>
            <span class="font-bold">RP:</span>
            <input 
              v-model.number="pareja.RP"
              :id="`rp-pareja-${index}`"
              :name="`rp-pareja-${index}`"
              type="number"
              min="0"
              max="300"
              required
              @input="validarRP(pareja)"
              class="w-24 px-2 py-1 border rounded"
            >
          </div>
        </div>
      </div>
    </div>

    <div class="flex justify-center space-x-4 mt-6">
      <button 
        @click="guardarResultados"
        class="px-6 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 text-lg font-semibold"
      >
        {{ isModificando ? 'Modificar Resultados' : 'Guardar Resultados' }}
      </button>
      <button 
        v-if="isModificando"
        @click="cancelarModificacion"
        class="px-6 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 text-lg font-semibold"
      >
        Cancelar
      </button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

export default {
  name: 'RegistroResultados',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const mesaId = ref(route.params.id);
    const mesaNumero = ref(0);
    const grupoB = ref('A');
    const partidaActual = ref(route.query.partida);
    const isModificando = ref(route.query.modificar === 'true');
    const campeonatoId = ref(localStorage.getItem('campeonato_id'));
    const pareja1 = ref({
      id_pareja: route.query.pareja1_id,
      nombre: '',
      RP: 0,
      PG: 0,
      PP: 0
    });
    const pareja2 = ref({
      id_pareja: route.query.pareja2_id,
      nombre: '',
      RP: 0,
      PG: 0,
      PP: 0
    });

    const calcularResultados = () => {
      // Si ambos RP son 0, no calcular nada (caso inicial)
      if (pareja1.value.RP === 0 && pareja2.value.RP === 0) {
        // Caso especial: última mesa con una sola pareja
        if (pareja2.value.id_pareja === null) {
          pareja1.value.RP = 150;
          pareja1.value.PG = 1;
          pareja1.value.PP = 150;
          
          // Establecer valores para pareja2 (aunque no exista)
          pareja2.value.RP = 0;
          pareja2.value.PG = 0;
          pareja2.value.PP = -150;
          return;
        }
        return;
      }

      if (pareja2.value.id_pareja === null) {
        // Caso de mesa con una sola pareja
        pareja1.value.RP = 150;
        pareja1.value.PG = 1;
        pareja1.value.PP = 150;
        
        // Establecer valores para pareja2 (aunque no exista)
        pareja2.value.RP = 0;
        pareja2.value.PG = 0;
        pareja2.value.PP = -150;
      } else {
        // Lógica normal para dos parejas
        if (pareja1.value.RP > pareja2.value.RP) {
          pareja1.value.PG = 1;
          pareja2.value.PG = 0;
        } else if (pareja1.value.RP < pareja2.value.RP) {
          pareja1.value.PG = 0;
          pareja2.value.PG = 1;
        } else {
          pareja2.value.RP = pareja1.value.RP - 1;
          pareja1.value.PG = 1;
          pareja2.value.PG = 0;
        }

        pareja1.value.PP = pareja1.value.RP - pareja2.value.RP;
        pareja2.value.PP = pareja2.value.RP - pareja1.value.RP;
      }
    };

    const guardarResultados = async () => {
      try {
        // Validar que ambos RP no sean 0 al mismo tiempo
        if (pareja1.value.RP === 0 && pareja2.value.RP === 0) {
          alert("Debe ingresar los resultados parciales (RP) antes de guardar");
          return;
        }

        // Validar que los RP sean diferentes
        if (pareja2.value.id_pareja !== null && pareja1.value.RP === pareja2.value.RP) {
          alert("No se pueden guardar los resultados: Los RP deben ser diferentes entre las parejas");
          return;
        }

        const campeonatoId = localStorage.getItem('campeonato_id');
        if (!campeonatoId) {
          throw new Error('ID del campeonato no encontrado');
        }

        // Validar que todos los campos necesarios estén presentes
        if (!partidaActual.value || !mesaId.value || !pareja1.value.id_pareja) {
          throw new Error('Faltan datos requeridos para guardar los resultados');
        }

        const payload = {
          campeonato_id: parseInt(campeonatoId),
          pareja1: {
            P: parseInt(partidaActual.value),
            M: parseInt(mesaId.value),
            id_pareja: parseInt(pareja1.value.id_pareja),
            GB: grupoB.value || 'A',
            PG: pareja1.value.PG,
            PP: pareja1.value.PP,
            RP: pareja1.value.RP
          }
        };

        if (pareja2.value.id_pareja !== null) {
          payload.pareja2 = {
            P: parseInt(partidaActual.value),
            M: parseInt(mesaId.value),
            id_pareja: parseInt(pareja2.value.id_pareja),
            GB: grupoB.value || 'A',
            PG: pareja2.value.PG,
            PP: pareja2.value.PP,
            RP: pareja2.value.RP
          };
        }

        console.log('Payload enviado:', payload);
        let response;
        
        try {
          if (isModificando.value) {
            response = await axios.post(
              `http://localhost:8000/api/resultados/update/${mesaId.value}/${partidaActual.value}`, 
              payload
            );
          } else {
            response = await axios.post('http://localhost:8000/api/resultados/create', payload);
          }
          
          console.log('Respuesta del servidor:', response.data);

          if (response.data && (response.data.message || response.data.pareja1)) {
            alert(response.data.message || 'Resultados guardados exitosamente');
            await actualizarRanking();
            router.push('/resultados/registro_partida');
          } else {
            throw new Error('Respuesta inesperada del servidor');
          }
        } catch (axiosError) {
          console.error('Error en la petición:', axiosError);
          if (axiosError.response?.data?.detail) {
            throw new Error(axiosError.response.data.detail);
          } else {
            throw new Error('Error al comunicarse con el servidor');
          }
        }
      } catch (e) {
        console.error('Error al guardar los resultados:', e);
        alert(`Error al guardar los resultados: ${e.message}`);
      }
    };

    const validarRP = (pareja) => {
      const valor = pareja.RP;
      
      if (valor < 0) {
        alert("El resultado no puede ser negativo");
        pareja.RP = 0;
        return false;
      } 
      
      if (valor > 300) {
        alert("El resultado debe ser como máximo 300");
        pareja.RP = 300;
        return false;
      } 
      
      if (!Number.isInteger(valor)) {
        alert("El resultado debe ser un número entero");
        pareja.RP = Math.round(valor);
        return false;
      }
      
      if (pareja2.value.id_pareja !== null && pareja1.value.RP === pareja2.value.RP) {
        alert("Los resultados parciales (RP) no pueden ser iguales entre las parejas");
        pareja.RP = 0;
        return false;
      }

      calcularResultados();
      return true;
    };

    const cancelarModificacion = () => {
      router.push('/resultados/registro_partida');
    };

    const actualizarRanking = async () => {
      const campeonatoId = localStorage.getItem('campeonato_id');
      if (!campeonatoId) {
        console.error('No hay un campeonato seleccionado');
        return;
      }
      try {
        await axios.post(`http://localhost:8000/api/campeonatos/${campeonatoId}/actualizar-ranking`);
      } catch (e) {
        console.error('Error al actualizar el ranking', e);
      }
    };

    onMounted(async () => {
      try {
        const id1 = route.query.pareja1_id;
        const id2 = route.query.pareja2_id;
        mesaId.value = route.params.id;
        partidaActual.value = route.query.partida;
        isModificando.value = route.query.modificar === 'true';
        const tieneResultados = route.query.tieneResultados === 'true';

        if (!id1 || id1 === 'null') {
          throw new Error('ID de la primera pareja no proporcionado');
        }

        const [pareja1Response, pareja2Response] = await Promise.all([
          axios.get(`http://localhost:8000/api/parejas/${id1}`),
          id2 && id2 !== 'null' ? axios.get(`http://localhost:8000/api/parejas/${id2}`) : Promise.resolve(null)
        ]);

        // Si es un nuevo registro, inicializar con RP en 0
        if (!isModificando.value) {
          pareja1.value = { 
            ...pareja1Response.data, 
            RP: 0, 
            PG: 0, 
            PP: 0, 
            id_pareja: id1 
          };
          
          if (pareja2Response) {
            pareja2.value = { 
              ...pareja2Response.data, 
              RP: 0, 
              PG: 0, 
              PP: 0, 
              id_pareja: id2 
            };
          } else {
            pareja2.value = { 
              nombre: 'Sin pareja', 
              id_pareja: null, 
              RP: 0, 
              PG: 0, 
              PP: 0 
            };
          }
        }

        // Si estamos modificando, cargar los resultados existentes
        if (isModificando.value && tieneResultados) {
          console.log(`Obteniendo resultados para mesa ${mesaId.value} y partida ${partidaActual.value}`);
          try {
            const resultadosResponse = await axios.get(
              `http://localhost:8000/api/resultados/${mesaId.value}/${partidaActual.value}`,
              {
                params: {
                  campeonato_id: localStorage.getItem('campeonato_id')
                }
              }
            );
            const resultados = resultadosResponse.data;
            console.log('Resultados obtenidos:', resultados);
            
            if (resultados.pareja1) {
              pareja1.value = { 
                ...pareja1Response.data,
                ...resultados.pareja1,
                id_pareja: id1 
              };
            }
            if (resultados.pareja2 && pareja2Response) {
              pareja2.value = { 
                ...pareja2Response.data,
                ...resultados.pareja2,
                id_pareja: id2 
              };
            }
          } catch (error) {
            console.error('Error al obtener resultados:', error);
            throw error;
          }
        }

        calcularResultados();

        // Obtener información de la mesa
        const mesaResponse = await axios.get(
          `http://localhost:8000/api/campeonatos/${localStorage.getItem('campeonato_id')}/mesas-partida-actual`
        );
        const mesa = mesaResponse.data.find(m => m.id === parseInt(mesaId.value));
        if (!mesa) {
          throw new Error('Mesa no encontrada');
        }
        mesaNumero.value = mesa.numero;
        grupoB.value = mesa.grupo || localStorage.getItem('campeonato_grupo');

        // Actualizar el payload con el grupo correcto
        const payload = {
          campeonato_id: parseInt(campeonatoId.value),
          pareja1: {
            P: parseInt(partidaActual.value),
            M: parseInt(mesaId.value),
            id_pareja: parseInt(pareja1.value.id_pareja),
            GB: grupoB.value,  // Usar el grupo obtenido
            PG: pareja1.value.PG,
            PP: pareja1.value.PP,
            RP: pareja1.value.RP
          }
        };

        if (pareja2.value.id_pareja !== null) {
          payload.pareja2 = {
            P: parseInt(partidaActual.value),
            M: parseInt(mesaId.value),
            id_pareja: parseInt(pareja2.value.id_pareja),
            GB: grupoB.value,  // Usar el grupo obtenido
            PG: pareja2.value.PG,
            PP: pareja2.value.PP,
            RP: pareja2.value.RP
          };
        }

        // ... resto del código existente ...
      } catch (e) {
        console.error('Error al cargar los datos', e);
        alert('Error al cargar los datos. Por favor, intente de nuevo.');
        router.push('/resultados/registro_partida');
      }
    });

    return {
      mesaId,
      mesaNumero,
      grupoB,
      partidaActual,
      pareja1,
      pareja2,
      calcularResultados,
      guardarResultados,
      validarRP,
      isModificando,
      cancelarModificacion,
      actualizarRanking,
      campeonatoId
    };
  }
}
</script>










INSERT INTO resultados (
    id,
    P,
    M,
    id_pareja,
    GB,
    PG,
    PP,
    RP,
    campeonato_id
  )
VALUES (
         
s,
    P:integer,
    M:integer,
    id_pareja:integer,
    'GB:character varying',
    PG:integer,
    PP:integer,
    RP:integer,
    campeonato_id:integer
  );


































