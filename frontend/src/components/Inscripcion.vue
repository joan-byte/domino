<template>
  <div class="container mx-auto p-4 flex flex-col items-center">
    <h1 class="text-2xl font-bold mb-4">Inscripción de Parejas</h1>
    <h2 class="text-xl mb-4">Campeonato: {{ campeonatoNombre }}</h2>
    <div v-if="!inscripcionAbierta" class="text-red-500 font-bold mb-4">
      La inscripción está cerrada
    </div>
    <div class="w-2/3 bg-white p-6 rounded-lg shadow-md mb-6">
      <h1 class="text-2xl font-bold mb-4">Inscripción de Parejas</h1>
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label for="nombrePareja" class="block text-sm font-bold text-gray-700">Nombre de la Pareja:</label>
            <input
              type="text"
              id="nombrePareja"
              name="nombrePareja"
              :value="nombrePareja"
              readonly
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            />
          </div>
          <div>
            <label for="club" class="block text-sm font-bold text-gray-700">Club (opcional):</label>
            <input
              type="text"
              id="club"
              name="club"
              v-model="formData.club"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            />
          </div>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label for="jugador1Nombre" class="block text-sm font-bold text-gray-700">Jugador 1</label>
            <div class="grid grid-cols-2 gap-2 mt-1">
              <div>
                <label for="jugador1Nombre" class="sr-only">Nombre del Jugador 1</label>
                <input
                  type="text"
                  id="jugador1Nombre"
                  name="jugador1Nombre"
                  v-model="formData.jugador1.nombre"
                  placeholder="Nombre"
                  required
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                />
              </div>
              <div>
                <label for="jugador1Apellido" class="sr-only">Apellido del Jugador 1</label>
                <input
                  type="text"
                  id="jugador1Apellido"
                  name="jugador1Apellido"
                  v-model="formData.jugador1.apellido"
                  placeholder="Apellido"
                  required
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                />
              </div>
            </div>
          </div>
          <div>
            <label for="jugador2Nombre" class="block text-sm font-bold text-gray-700">Jugador 2</label>
            <div class="grid grid-cols-2 gap-2 mt-1">
              <div>
                <label for="jugador2Nombre" class="sr-only">Nombre del Jugador 2</label>
                <input
                  type="text"
                  id="jugador2Nombre"
                  name="jugador2Nombre"
                  v-model="formData.jugador2.nombre"
                  placeholder="Nombre"
                  required
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                />
              </div>
              <div>
                <label for="jugador2Apellido" class="sr-only">Apellido del Jugador 2</label>
                <input
                  type="text"
                  id="jugador2Apellido"
                  name="jugador2Apellido"
                  v-model="formData.jugador2.apellido"
                  placeholder="Apellido"
                  required
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                />
              </div>
            </div>
          </div>
        </div>

        <div v-if="isEditing" class="flex items-center">
          <label for="activa" class="flex items-center cursor-pointer">
            <input
              type="checkbox"
              id="activa"
              name="activa"
              v-model="formData.activa"
              class="rounded border-gray-300 text-indigo-600 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            />
            <span class="ml-2 text-sm font-bold text-gray-700">Activa</span>
          </label>
        </div>

        <div class="flex justify-center space-x-4">
          <button 
            v-if="!isEditing" 
            type="submit" 
            :disabled="!inscripcionAbierta"
            class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Inscribir Pareja
          </button>
          <button 
            v-else 
            type="submit" 
            :disabled="!inscripcionAbierta"
            class="px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Modificar Pareja
          </button>
          <button 
            type="button" 
            @click="handleCancel" 
            :disabled="!inscripcionAbierta"
            class="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Cancelar
          </button>
          <button 
            v-if="isEditing"
            type="button" 
            @click="handleDelete" 
            :disabled="!inscripcionAbierta"
            class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Eliminar
          </button>
        </div>
      </form>
    </div>
    <div class="w-full bg-white p-6 rounded-lg shadow-md overflow-x-auto mt-6">
      <h2 class="text-xl font-bold mb-4 text-center">Lista de Parejas Inscritas</h2>
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
          <tr 
            v-for="pareja in parejas" 
            :key="pareja.id" 
            @click="seleccionarPareja(pareja)"
            :class="{
              'hover:bg-gray-50 cursor-pointer': inscripcionAbierta,
              'bg-gray-100': pareja.id === parejaSeleccionada?.id && inscripcionAbierta
            }"
          >
            <td class="py-2 px-4 border-b">{{ pareja.id }}</td>
            <td class="py-2 px-4 border-b">{{ pareja.nombre }}</td>
            <td class="py-2 px-4 border-b">{{ pareja.club }}</td>
            <td class="py-2 px-4 border-b text-center">
              <input 
                type="checkbox" 
                :id="`pareja-${pareja.id}`"
                :name="`pareja-${pareja.id}`"
                :checked="pareja.activa" 
                :disabled="true"
                class="form-checkbox h-5 w-5 text-blue-600 cursor-not-allowed"
              >
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

export default {
  name: 'InscripcionParejas',
  setup() {
    const formData = ref({
      jugador1: { nombre: '', apellido: '' },
      jugador2: { nombre: '', apellido: '' },
      club: '',
      activa: true
    });
    const parejas = ref([]);
    const nombrePareja = computed(() => {
      return `${formData.value.jugador1.nombre} ${formData.value.jugador1.apellido} y ${formData.value.jugador2.nombre} ${formData.value.jugador2.apellido}`;
    });
    const route = useRoute();
    const router = useRouter();
    const isEditing = ref(false);
    const parejaSeleccionada = ref(null);
    const campeonatoNombre = ref(localStorage.getItem('campeonato_nombre') || 'No seleccionado');
    const isLoading = ref(false);
    const error = ref(null);
    const campeonatoId = ref(localStorage.getItem('campeonato_id'));
    const inscripcionAbierta = ref(true);

    const seleccionarPareja = (pareja) => {
      if (!inscripcionAbierta.value) return;
      parejaSeleccionada.value = pareja;
      formData.value = {
        jugador1: { 
          nombre: pareja.nombre.split(' y ')[0].split(' ')[0], 
          apellido: pareja.nombre.split(' y ')[0].split(' ').slice(1).join(' ')
        },
        jugador2: { 
          nombre: pareja.nombre.split(' y ')[1].split(' ')[0], 
          apellido: pareja.nombre.split(' y ')[1].split(' ').slice(1).join(' ')
        },
        club: pareja.club,
        activa: pareja.activa
      };
      isEditing.value = true;
    };

    const fetchParejas = async () => {
      isLoading.value = true;
      error.value = null;
      try {
        if (!campeonatoId.value) {
          throw new Error('ID del campeonato no definido');
        }
        const response = await axios.get(`http://localhost:8000/api/campeonatos/${campeonatoId.value}/parejas`);
        parejas.value = response.data;
      } catch (e) {
        console.error('Error al obtener las parejas', e);
        error.value = 'Error al cargar las parejas. Por favor, intente de nuevo.';
      } finally {
        isLoading.value = false;
      }
    };

    const handleSubmit = async () => {
      try {
        const payload = {
          jugador1: formData.value.jugador1,
          jugador2: formData.value.jugador2,
          club: formData.value.club,
          activa: formData.value.activa,
          campeonato_id: parseInt(localStorage.getItem('campeonato_id'))
        };

        if (isEditing.value) {
          const response = await axios.put(`http://localhost:8000/api/parejas/${parejaSeleccionada.value.id}`, payload);
          console.log('Respuesta del servidor:', response.data);
          alert('Pareja actualizada con éxito');
        } else {
          await axios.post('http://localhost:8000/api/parejas', payload);
          alert('Pareja inscrita con éxito');
        }
        resetForm();
        await fetchParejas();
      } catch (error) {
        console.error('Error al procesar la pareja', error);
        if (error.response) {
          console.error('Datos de la respuesta de error:', error.response.data);
          if (error.response.status === 422) {
            const errorDetail = error.response.data.detail;
            if (typeof errorDetail === 'string') {
              alert(`Error: ${errorDetail}`);
            } else if (Array.isArray(errorDetail)) {
              const errorMessages = errorDetail.map(err => `${err.loc.join('.')} - ${err.msg}`).join('\n');
              alert(`Errores de validación:\n${errorMessages}`);
            } else {
              alert(`Error de validación: ${JSON.stringify(errorDetail)}`);
            }
          } else {
            alert(`Error del servidor: ${error.response.status} - ${JSON.stringify(error.response.data)}`);
          }
        } else if (error.request) {
          alert('No se pudo conectar con el servidor. Por favor, verifica tu conexión a internet.');
        } else {
          alert(`Error al procesar la solicitud: ${error.message}`);
        }
      }
    };

    const handleCancel = () => {
      resetForm();
      if (isEditing.value) {
        router.push('/inscripcion');
      }
    };

    const handleDelete = async () => {
      if (confirm('¿Estás seguro de que quieres eliminar esta pareja?')) {
        try {
          await axios.delete(`http://localhost:8000/api/parejas/${parejaSeleccionada.value.id}`);
          alert('Pareja eliminada con éxito');
          resetForm();
          await fetchParejas();
        } catch (error) {
          console.error('Error al eliminar la pareja', error);
          if (error.response) {
            alert(`Error del servidor: ${error.response.status} - ${error.response.data.detail || 'Error desconocido'}`);
          } else if (error.request) {
            alert('No se pudo conectar con el servidor. Por favor, verifica tu conexión a internet.');
          } else {
            alert(`Error al procesar la solicitud: ${error.message}`);
          }
        }
      }
    };

    const resetForm = () => {
      formData.value = {
        jugador1: { nombre: '', apellido: '' },
        jugador2: { nombre: '', apellido: '' },
        club: '',
        activa: true
      };
      isEditing.value = false;
      parejaSeleccionada.value = null;
    };

    const toggleActiva = async (pareja) => {
      try {
        const response = await axios.patch(`http://localhost:8000/api/parejas/${pareja.id}`, {
          activa: !pareja.activa
        });
        pareja.activa = response.data.activa;
      } catch (error) {
        console.error('Error al actualizar el estado de la pareja', error);
        alert('Error al actualizar el estado de la pareja. Por favor, intente de nuevo.');
      }
    };

    onMounted(() => {
      fetchParejas();
      if (route.params.id) {
        isEditing.value = true;
        // Aquí deberías cargar los datos de la pareja seleccionada
        // y asignarlos a formData.value
      }
      const inscripcionEstado = localStorage.getItem('inscripcionAbierta');
      if (inscripcionEstado !== null) {
        inscripcionAbierta.value = inscripcionEstado === 'true';
      }
    });

    watch(() => route.params.id, (newId) => {
      isEditing.value = !!newId;
      if (newId) {
        // Cargar los datos de la pareja seleccionada
      } else {
        resetForm();
      }
    });

    return {
      formData,
      nombrePareja,
      parejas,
      handleSubmit,
      handleCancel,
      handleDelete,
      isEditing,
      seleccionarPareja,
      parejaSeleccionada,
      campeonatoNombre,
      isLoading,
      error,
      toggleActiva,
      inscripcionAbierta
    };
  }
}
</script>