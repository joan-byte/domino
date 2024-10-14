<template>
  <div class="container mx-auto p-4">
    <h1 class="text-3xl font-bold mb-4">Partida {{ partidaActual }} - Mesa {{ mesaId }} - GB A</h1>
    
    <div v-for="(pareja, index) in [pareja1, pareja2]" :key="index" class="mb-6">
      <h2 class="text-2xl font-semibold mb-2">Pareja {{ pareja.id_pareja }}</h2>
      <p class="text-xl mb-4 text-center">{{ pareja.nombre }}</p>
      <div class="flex justify-between mb-2">
        <div>
          <span class="font-bold">PG:</span> {{ pareja.PG }}
        </div>
        <div>
          <span class="font-bold">PP:</span> {{ pareja.PP }}
        </div>
      </div>
      <div>
        <label :for="`rp-pareja${index + 1}`" class="block text-sm font-medium text-gray-700">
          RP Pareja {{ index + 1 }}
        </label>
        <input 
          :id="`rp-pareja${index + 1}`"
          v-model="pareja.RP"
          type="number"
          min="0"
          max="300"
          required
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
        >
      </div>
    </div>

    <button 
      @click="guardarResultados"
      class="w-full px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 mt-4"
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

    const guardarResultados = async () => {
      try {
        const payload = {
          pareja1: {
            P: parseInt(partidaActual.value),
            M: parseInt(mesaId.value),
            id_pareja: pareja1.value.id_pareja,
            RP: parseInt(pareja1.value.RP),
            GB: "A"
          },
          pareja2: {
            P: parseInt(partidaActual.value),
            M: parseInt(mesaId.value),
            id_pareja: pareja2.value.id_pareja,
            RP: parseInt(pareja2.value.RP),
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
      guardarResultados
    };
  }
}
</script>

