import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import HkviewVue from '@/components/Hkview.vue'
import AppLayOutVue from '@/components/layouts/AppLayOut.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: AppLayOutVue,
    },
    {
      path: '/HKview',
      name: 'HKview',
      component:HkviewVue
    }
  ]
})

export default router
