<template>
  <div class="container mx-auto p-4 bg-gray-100 rounded-lg shadow-md">
    <h1 class="text-3xl font-bold mb-4">Partida {{ partidaActual }} - Mesa {{ mesaId }} - GB A</h1>
    
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
    const partidaActual = ref(route.query.partida);
    const isModificando = ref(route.query.modificar === 'true');
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
      if (pareja2.value.id_pareja === null) {
        pareja1.value.RP = 150;
        pareja1.value.PG = 1;
        pareja1.value.PP = 150;
      } else {
        if (pareja1.value.RP > pareja2.value.RP) {
          pareja1.value.PG = 1;
          pareja2.value.PG = 0;
        } else if (pareja1.value.RP < pareja2.value.RP) {
          pareja1.value.PG = 0;
          pareja2.value.PG = 1;
        } else {
          pareja1.value.PG = 0;
          pareja2.value.PG = 0;
        }

        pareja1.value.PP = pareja1.value.RP - pareja2.value.RP;
        pareja2.value.PP = pareja2.value.RP - pareja1.value.RP;
      }
    };

    const guardarResultados = async () => {
      try {
        const campeonatoId = localStorage.getItem('campeonato_id');
        if (!campeonatoId) {
          throw new Error('ID del campeonato no encontrado');
        }

        const payload = {
          campeonato_id: parseInt(campeonatoId),
          pareja1: {
            P: parseInt(partidaActual.value),
            M: parseInt(mesaId.value),
            id_pareja: parseInt(pareja1.value.id_pareja),
            GB: 'A',
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
            GB: 'A',
            PG: pareja2.value.PG,
            PP: pareja2.value.PP,
            RP: pareja2.value.RP
          };
        }

        console.log('Payload enviado:', payload);
        let response;
        if (isModificando.value) {
          response = await axios.post(`http://localhost:8000/api/resultados/update/${mesaId.value}/${partidaActual.value}`, payload);
        } else {
          response = await axios.post('http://localhost:8000/api/resultados/create', payload);
        }
        console.log('Respuesta del servidor:', response.data);

        if (response.data.message === "Resultados actualizados exitosamente" || response.data.message === "Resultados creados exitosamente") {
          alert(response.data.message);
          await actualizarRanking();
          router.push('/resultados/registro_partida');
        } else {
          throw new Error('Respuesta inesperada del servidor');
        }
      } catch (e) {
        console.error('Error al guardar los resultados:', e);
        alert('Error al guardar los resultados. Por favor, intente de nuevo.');
      }
    };

    const validarRP = (pareja) => {
      const valor = pareja.RP;
      if (valor < 0) {
        alert("El resultado no puede ser negativo");
        pareja.RP = 0;
      } else if (valor > 300) {
        alert("El resultado debe ser como máximo 300");
        pareja.RP = 300;
      } else if (!Number.isInteger(valor)) {
        alert("El resultado debe ser un número entero");
        pareja.RP = Math.round(valor);
      }
      calcularResultados();
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

        pareja1.value = { ...pareja1Response.data, RP: 0, PG: 0, PP: 0, id_pareja: id1 };
        
        if (pareja2Response) {
          pareja2.value = { ...pareja2Response.data, RP: 0, PG: 0, PP: 0, id_pareja: id2 };
        } else {
          pareja2.value = { nombre: 'Sin pareja', id_pareja: null, RP: 0, PG: 0, PP: 0 };
        }

        if (isModificando.value && tieneResultados) {
          console.log(`Obteniendo resultados para mesa ${mesaId.value} y partida ${partidaActual.value}`);
          try {
            const resultadosResponse = await axios.get(`http://localhost:8000/api/resultados/${mesaId.value}/${partidaActual.value}`);
            const resultados = resultadosResponse.data;
            console.log('Resultados obtenidos:', resultados);
            
            if (resultados.pareja1) {
              pareja1.value = { ...pareja1.value, ...resultados.pareja1 };
            }
            if (resultados.pareja2) {
              pareja2.value = { ...pareja2.value, ...resultados.pareja2 };
            } else {
              pareja2.value = { nombre: 'Sin pareja', id_pareja: null, RP: 0, PG: 0, PP: 0 };
            }
          } catch (error) {
            console.error('Error al obtener resultados:', error);
            if (error.response && error.response.status === 404) {
              console.log('No se encontraron resultados para esta mesa y partida');
              alert('No se encontraron resultados para modificar. Se iniciará un nuevo registro.');
              isModificando.value = false;
            } else {
              throw error;
            }
          }
        }

        calcularResultados();
      } catch (e) {
        console.error('Error al cargar los datos de las parejas', e);
        alert('Error al cargar los datos de las parejas. Por favor, intente de nuevo.');
        router.push('/resultados/registro_partida');
      }
    });

    return {
      mesaId,
      partidaActual,
      pareja1,
      pareja2,
      calcularResultados,
      guardarResultados,
      validarRP,
      isModificando,
      cancelarModificacion,
      actualizarRanking
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

































