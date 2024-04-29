import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') },
      {
        path: '/buildings',
        component: () => import('src/pages/BuildingsPage.vue'),
      },
      {
        path: '/building/:id',
        component: () => import('src/pages/BuildingPage.vue'),
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
