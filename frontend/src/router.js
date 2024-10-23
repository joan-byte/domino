import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/Home.vue';
import Campeonatos from '@/views/Campeonatos.vue';
import Inscripcion from '@/components/Inscripcion.vue';
import Inicio from '@/components/Partidas/Inicio.vue';
import Mesas from '@/components/Partidas/Mesas.vue';
import CierrePartida from '@/components/Resultados/CierrePartida.vue';
import RegistroPartida from '@/components/Resultados/Registro_Partida.vue';
import RegistroResultados from '@/components/Resultados/Resultados.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/campeonatos/:id?',
    name: 'Campeonatos',
    component: Campeonatos
  },
  {
    path: '/inscripcion',
    name: 'Inscripcion',
    component: Inscripcion
  },
  {
    path: '/Partidas/Inicio',
    name: 'Inicio',
    component: Inicio
  },
  {
    path: '/Partidas/Ranking',
    name: 'Ranking',
    component: () => import('@/components/Partidas/Ranking.vue')
  },
  {
    path: '/Partidas/Mesas',
    name: 'Mesas',
    component: Mesas
  },
  {
    path: '/Resultados/CierrePartida',
    name: 'CierrePartida',
    component: CierrePartida
  },
  {
    path: '/resultados/:id',
    name: 'RegistroResultados',
    component: RegistroResultados
  },
  {
    path: '/Resultados/Registro_Partida',
    name: 'RegistroPartida',
    component: RegistroPartida
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
