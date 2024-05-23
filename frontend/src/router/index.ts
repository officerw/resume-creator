import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import TemplateEditor from '@/views/TemplateEditor.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/editor',
      name: 'editor',
      component: TemplateEditor
    }
  ]
})

export default router
