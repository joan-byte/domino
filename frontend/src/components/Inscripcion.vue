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
      <div v-else-if="error" class="text-red-500">{{ error }}</div>
      <div v-else>
        <table v-if="parejas.length > 0" class="min-w-full bg-white border border-gray-300">
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
        <div v-else class="text-center py-4 text-gray-600">
          No hay parejas inscritas en este campeonato.
        </div>
      </div>
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
    const error = ref('');
    const inscripcionAbierta = ref(true);
    const editingParejaId = ref(null);

    const seleccionarPareja = (pareja) => {
      if (!inscripcionAbierta.value || !pareja.nombre) return;
      parejaSeleccionada.value = pareja;
      const [jugador1Completo, jugador2Completo] = pareja.nombre.split(' y ');
      const jugador1 = jugador1Completo.split(' ');
      const jugador2 = jugador2Completo.split(' ');
      formData.value = {
        jugador1: { 
          nombre: jugador1[0] || '', 
          apellido: jugador1.slice(1).join(' ')
        },
        jugador2: { 
          nombre: jugador2[0] || '', 
          apellido: jugador2.slice(1).join(' ')
        },
        club: pareja.club,
        activa: pareja.activa
      };
      isEditing.value = true;
      editingParejaId.value = pareja.id;
    };

    const fetchParejas = async () => {
      try {
        const campeonatoId = localStorage.getItem('campeonato_id');
        if (!campeonatoId) {
          console.error('No hay un campeonato seleccionado');
          error.value = 'No hay un campeonato seleccionado. Por favor, seleccione un campeonato primero.';
          return;
        }
        isLoading.value = true;
        const response = await axios.get(`http://localhost:8000/api/campeonatos/${campeonatoId}/parejas`);
        parejas.value = response.data.sort((a, b) => b.id - a.id);
        console.log('Parejas obtenidas:', parejas.value);
      } catch (e) {
        console.error('Error al obtener las parejas', e);
        if (e.response?.status === 404) {
          if (e.response.data.detail === "Campeonato no encontrado") {
            error.value = 'El campeonato seleccionado no existe.';
          } else {
            parejas.value = []; // Si no hay parejas, inicializamos como array vacío
            error.value = ''; // Limpiamos cualquier error previo
          }
        } else {
          error.value = 'Error al conectar con el servidor. Por favor, intente de nuevo más tarde.';
        }
      } finally {
        isLoading.value = false;
      }
    };

    const handleSubmit = async () => {
      try {
        const campeonatoId = parseInt(localStorage.getItem('campeonato_id'));
        if (!campeonatoId) {
          throw new Error('ID del campeonato no encontrado');
        }

        const payload = {
          jugador1: {
            ...formData.value.jugador1,
            campeonato_id: campeonatoId
          },
          jugador2: {
            ...formData.value.jugador2,
            campeonato_id: campeonatoId
          },
          club: formData.value.club,
          activa: formData.value.activa,
          campeonato_id: campeonatoId
        };

        console.log('Payload a enviar:', payload);

        if (isEditing.value) {
          if (!parejaSeleccionada.value || !parejaSeleccionada.value.id) {
            console.error('Error: Intentando editar una pareja sin ID');
            alert('Error: No se puede editar la pareja. Por favor, seleccione una pareja válida.');
            return;
          }
          console.log('Editando pareja con ID:', parejaSeleccionada.value.id);
          const response = await axios.put(`http://localhost:8000/api/parejas/${parejaSeleccionada.value.id}`, payload);
          console.log('Respuesta del servidor (edición):', response.data);
          alert('Pareja actualizada con éxito');
        } else {
          const response = await axios.post('http://localhost:8000/api/parejas', payload);
          console.log('Respuesta del servidor (creación):', response.data);
          alert('Pareja inscrita con éxito');
        }

        resetForm();
        await fetchParejas();  // Actualizar la lista de parejas
      } catch (error) {
        console.error('Error al guardar la pareja:', error);
        if (error.response) {
          console.error('Datos de la respuesta de error:', error.response.data);
          alert(`Error del servidor: ${error.response.status} - ${error.response.data.detail || JSON.stringify(error.response.data)}`);
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
      editingParejaId.value = null;
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
      inscripcionAbierta,
      editingParejaId
    };
  }
}
</script>



















































