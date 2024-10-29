import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/components/Home.vue'
import RegistroPartida from '@/components/Resultados/Registro_Partida.vue'
import Podium from '@/components/Resultados/Podium.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/resultados/registro',
    name: 'RegistroPartida',
    component: RegistroPartida
  },
  {
    path: '/resultados/podium',
    name: 'Podium',
    component: Podium
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 