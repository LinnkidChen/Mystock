import { createRouter, createWebHistory } from 'vue-router'
// import HkviewVue from '@/components/HkView.vue'
import AppLayOutVue from '@/components/layouts/AppLayOut.vue';
// import IndexView from '@/views/IndexView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'index',
      component: AppLayOutVue,
      children: [
        {
          path: '',
          name: 'index',
          component: ()=> import( '@/views/IndexView.vue')
        },
        {
          path: '/HKview',
          name: 'HKview',
          component: ()=> import( '@/components/HkView.vue')
        },
        {
          path: '/:catchAll(.*)',
          name: 'NotFound',
          component: () => import( '@/views/ErrorPage.vue'),
          meta: {
            requiresAuth: false
          }}
      ]
    },    
    

    


  ]
})

export default router
