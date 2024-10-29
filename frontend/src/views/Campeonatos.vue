<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4 text-center">Gestión de Campeonatos</h1>
    <div class="flex justify-center">
      <div class="w-full md:w-1/3">
        <form @submit.prevent="handleSubmit" class="space-y-4 bg-white p-6 rounded-lg shadow-md">
          <div>
            <label for="nombre" class="block text-sm font-medium text-gray-700">Nombre:</label>
            <input
              type="text"
              id="nombre"
              v-model="formData.nombre"
              required
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            />
          </div>
          <div>
            <label for="fecha_inicio" class="block text-sm font-medium text-gray-700">Fecha de inicio:</label>
            <input
              type="date"
              id="fecha_inicio"
              v-model="formData.fecha_inicio"
              required
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            />
          </div>
          <div>
            <label for="dias_duracion" class="block text-sm font-medium text-gray-700">Duración (días):</label>
            <input
              type="number"
              id="dias_duracion"
              v-model="formData.dias_duracion"
              required
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            />
          </div>
          <div>
            <label for="numero_partidas" class="block text-sm font-medium text-gray-700">Número de partidas:</label>
            <input
              type="number"
              id="numero_partidas"
              v-model="formData.numero_partidas"
              required
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            />
          </div>
          <div class="flex items-center">
            <input
              type="checkbox"
              id="grupo_b"
              v-model="formData.grupo_b"
              class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label for="grupo_b" class="ml-2 block text-sm text-gray-900">
              Grupo {{ formData.grupo_b ? 'B' : 'A' }}
            </label>
          </div>
          <div class="flex space-x-2 justify-end">
            <button v-if="isEditing" type="submit" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
              Modificar
            </button>
            <button v-else type="submit" class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600">
              Guardar
            </button>
            <button v-if="isEditing" @click="handleDelete" type="button" class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600">
              Eliminar
            </button>
            <button @click="handleCancel" type="button" class="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400">
              Cancelar
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000'
});

export default {
  name: 'CampeonatosView',
  setup(props, { emit }) {
    const formData = ref({
      nombre: '',
      fecha_inicio: '',
      dias_duracion: '',
      numero_partidas: '',
      grupo_b: false,
    });
    const isEditing = ref(false);
    const route = useRoute();
    const router = useRouter();

    const fetchCampeonato = async (id) => {
      console.log('ID del campeonato a buscar:', id);
      try {
        console.log(`Intentando obtener el campeonato con ID: ${id}`);
        const response = await api.get(`/api/campeonatos/${id}`);
        console.log('Respuesta del servidor:', response.data);
        formData.value = {
          nombre: response.data.nombre,
          fecha_inicio: response.data.fecha_inicio.split('T')[0],
          dias_duracion: response.data.dias_duracion,
          numero_partidas: response.data.numero_partidas,
          grupo_b: response.data.grupo_b,
        };
        isEditing.value = true;
      } catch (error) {
        console.error('Error al cargar el campeonato', error);
        if (error.response) {
          console.log('Estado de la respuesta:', error.response.status);
          console.log('Datos de la respuesta:', error.response.data);
          if (error.response.status === 404) {
            alert(`El campeonato con ID ${id} no existe en el servidor.`);
          } else {
            alert(`Error del servidor: ${error.response.status} - ${error.response.data.detail || 'Error desconocido'}`);
          }
        } else if (error.request) {
          console.log('No se recibió respuesta del servidor');
          alert('No se pudo conectar con el servidor. Por favor, verifica tu conexión a internet y que el servidor esté en funcionamiento.');
        } else {
          console.log('Error al configurar la solicitud:', error.message);
          alert(`Error al procesar la solicitud: ${error.message}`);
        }
        isEditing.value = false;
        router.push('/');
      }
    };

    const handleSubmit = async () => {
      // Definir campeonatoData fuera del try-catch
      const campeonatoData = {
        ...formData.value,
        grupo_b: Boolean(formData.value.grupo_b),
        dias_duracion: parseInt(formData.value.dias_duracion),
        numero_partidas: parseInt(formData.value.numero_partidas)
      };

      try {
        let response;
        if (isEditing.value) {
          response = await api.put(`/api/campeonatos/${route.params.id}`, campeonatoData);
          console.log('Respuesta de actualización:', response.data);
          alert('Campeonato actualizado con éxito');
        } else {
          response = await api.post('/api/campeonatos/', campeonatoData);
          console.log('Respuesta de creación:', response.data);
          alert('Campeonato creado con éxito');
        }
        router.push('/');
      } catch (error) {
        console.error('Error al guardar el campeonato', error);
        if (error.response) {
          console.log('Datos enviados:', campeonatoData);
          console.log('Error response:', error.response.data);
          alert(`Error del servidor: ${error.response.status} - ${error.response.data.detail || 'Error desconocido'}`);
        } else if (error.request) {
          alert('No se pudo conectar con el servidor. Por favor, verifica tu conexión a internet.');
        } else {
          alert(`Error al procesar la solicitud: ${error.message}`);
        }
      }
    };

    const handleDelete = async () => {
      if (confirm('¿Estás seguro de que quieres eliminar este campeonato?')) {
        try {
          await api.delete(`/api/campeonatos/${route.params.id}`);
          alert('Campeonato eliminado con éxito');
          router.push('/');
        } catch (error) {
          console.error('Error al eliminar el campeonato', error);
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

    const handleCancel = () => {
      formData.value = {
        nombre: '',
        fecha_inicio: '',
        dias_duracion: '',
        numero_partidas: '',
        grupo_b: false,
      };
      isEditing.value = false;
      router.push('/');
    };

    const seleccionarCampeonato = async (id) => {
      try {
        const response = await api.get(`/api/campeonatos/${id}`);
        const campeonatoData = response.data;
        
        // Guardar los datos del campeonato en localStorage
        localStorage.setItem('campeonato_id', campeonatoData.id);
        localStorage.setItem('campeonato_nombre', campeonatoData.nombre);
        
        // Emitir el evento cuando se selecciona un campeonato
        emit('campeonato-seleccionado', true);
        
        // Redirigir a la página de inicio o a donde sea apropiado
        router.push('/');
      } catch (error) {
        console.error('Error al seleccionar el campeonato', error);
        alert('Error al seleccionar el campeonato. Por favor, intente de nuevo.');
      }
    };

    onMounted(() => {
      const id = route.params.id;
      if (id) {
        fetchCampeonato(id);
      } else {
        isEditing.value = false;
        formData.value = {
          nombre: '',
          fecha_inicio: '',
          dias_duracion: '',
          numero_partidas: '',
          grupo_b: false,
        };
      }
    });

    watch(() => route.params.id, (newId) => {
      if (newId) {
        fetchCampeonato(newId);
      } else {
        isEditing.value = false;
        formData.value = {
          nombre: '',
          fecha_inicio: '',
          dias_duracion: '',
          numero_partidas: '',
          grupo_b: false,
        };
      }
    });

    return {
      formData,
      isEditing,
      handleSubmit,
      handleDelete,
      handleCancel,
      seleccionarCampeonato
    };
  },
};
</script>

