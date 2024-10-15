<template>
  <div class="container mx-auto p-4 bg-gray-100 rounded-lg shadow-md">
    <h1 class="text-3xl font-bold mb-4">Partida {{ partidaActual }} - Mesa {{ mesaId }} - GB A</h1>
    
    <div v-for="(pareja, index) in [pareja1, pareja2]" :key="index" class="mb-4 bg-white p-4 rounded-lg shadow">
      <div class="flex items-center justify-between">
        <h2 class="text-2xl font-semibold">Pareja {{ pareja.id_pareja }}</h2>
        <p class="text-2xl font-semibold">{{ pareja.nombre }}</p>
        <div class="flex items-center space-x-4">
          <div>
            <span class="font-bold">PG:</span>
            <input 
              v-model="pareja.PG"
              :id="`pg-pareja-${pareja.id_pareja}`"
              :name="`pg-pareja-${pareja.id_pareja}`"
              type="number"
              min="0"
              max="1"
              readonly
              class="w-24 px-2 py-1 border rounded"
            >
          </div>
          <div>
            <span class="font-bold">PP:</span>
            <input 
              v-model="pareja.PP"
              :id="`pp-pareja-${pareja.id_pareja}`"
              :name="`pp-pareja-${pareja.id_pareja}`"
              type="number"
              readonly
              class="w-24 px-2 py-1 border rounded"
            >
          </div>
          <div>
            <span class="font-bold">RP:</span>
            <input 
              v-model="pareja.RP"
              :id="`rp-pareja-${pareja.id_pareja}`"
              :name="`rp-pareja-${pareja.id_pareja}`"
              type="number"
              min="0"
              max="300"
              required
              @input="calcularResultados"
              class="w-24 px-2 py-1 border rounded"
            >
          </div>
        </div>
      </div>
    </div>

    <button 
      @click="guardarResultados"
      class="mx-auto mt-6 px-6 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 text-lg font-semibold"
    >
      Guardar Resultados
    </button>
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
    };

    const guardarResultados = async () => {
      try {
        const payload = {
          pareja1: {
            P: parseInt(partidaActual.value),
            M: parseInt(mesaId.value),
            id_pareja: pareja1.value.id_pareja,
            RP: parseInt(pareja1.value.RP),
            PG: parseInt(pareja1.value.PG),
            PP: parseInt(pareja1.value.PP),
            GB: "A"
          },
          pareja2: {
            P: parseInt(partidaActual.value),
            M: parseInt(mesaId.value),
            id_pareja: pareja2.value.id_pareja,
            RP: parseInt(pareja2.value.RP),
            PG: parseInt(pareja2.value.PG),
            PP: parseInt(pareja2.value.PP),
            GB: "A"
          }
        };
        await axios.post('http://localhost:8000/api/resultados', payload);
        alert('Resultados guardados con éxito');
        router.push('/resultados/registro_partida');
      } catch (e) {
        console.error('Error al guardar los resultados', e);
        alert('Error al guardar los resultados. Por favor, intente de nuevo.');
      }
    };

    onMounted(async () => {
      try {
        const id1 = route.query.pareja1_id;
        const id2 = route.query.pareja2_id;
        if (id1 && id1 !== 'null') {
          const response = await axios.get(`http://localhost:8000/api/parejas/${id1}`);
          pareja1.value.nombre = response.data.nombre;
          pareja1.value.id_pareja = id1;
        }
        if (id2 && id2 !== 'null') {
          const response = await axios.get(`http://localhost:8000/api/parejas/${id2}`);
          pareja2.value.nombre = response.data.nombre;
          pareja2.value.id_pareja = id2;
        }
        if (!id1 || id1 === 'null') {
          pareja1.value.nombre = 'Sin pareja';
          pareja1.value.id_pareja = null;
        }
        if (!id2 || id2 === 'null') {
          pareja2.value.nombre = 'Sin pareja';
          pareja2.value.id_pareja = null;
        }
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
      guardarResultados
    };
  }
}
</script>
