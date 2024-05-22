import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/buildings',
    component: () => import('layouts/BuildingsLayout.vue'),
  },
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') },
      {
        path: '/test/:id',
        component: () => import('src/pages/TestPage.vue'),
      },
      {
        path: '/model/:id',
        component: () => import('src/pages/ModelPage.vue'),
      },
      {
        path: '/submit',
        component: () => import('src/pages/ContactUsPage.vue'),
      },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
