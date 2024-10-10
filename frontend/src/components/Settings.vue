<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Configuración del Campeonato</h1>
    <form @submit.prevent="handleSubmit" class="space-y-4">
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
        <label for="fechaInicio" class="block text-sm font-medium text-gray-700">Fecha de inicio:</label>
        <input
          type="date"
          id="fechaInicio"
          v-model="formData.fechaInicio"
          required
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
        />
      </div>
      <div>
        <label for="fechaFin" class="block text-sm font-medium text-gray-700">Fecha de fin:</label>
        <input
          type="date"
          id="fechaFin"
          v-model="formData.fechaFin"
          required
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
        />
      </div>
      <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
        Guardar Configuración
      </button>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  name: 'CampeonatoSettings',
  setup() {
    const formData = ref({
      nombre: '',
      fechaInicio: '',
      fechaFin: '',
    });

    const handleSubmit = () => {
      // Aquí manejarías la lógica para guardar la configuración del campeonato
      console.log('Configuración del campeonato a guardar:', formData.value);
      // Aquí podrías hacer una llamada a la API para guardar los datos
    };

    return {
      formData,
      handleSubmit,
    };
  },
};
</script>
