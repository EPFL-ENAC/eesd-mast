<template>
  <q-layout view="lHh Lpr lFf">
    <q-header bordered class="bg-white text-grey-10">
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title class="text-weight-medium">
          MAsonry Shake-Table
        </q-toolbar-title>
      </q-toolbar>
      <q-toolbar inset style="min-height: 20px">
        <q-btn
          flat
          dense
          :label="$t('overview')"
          no-caps
          to="/"
          :class="isHome ? 'bg-grey-3' : ''"
          class="q-pt-sm q-pb-sm q-pr-md q-pl-md"
        />
        <q-btn
          flat
          dense
          :label="$t('tested_buildings')"
          no-caps
          to="/buildings"
          :class="isBuildings ? 'bg-grey-3' : ''"
          class="on-left on-right q-pt-sm q-pb-sm q-pr-md q-pl-md"
        />
        <q-btn
          flat
          dense
          :label="$t('data_submission')"
          no-caps
          to="/submit"
          :class="isSubmit ? 'bg-grey-3' : ''"
          class="q-pt-sm q-pb-sm q-pr-md q-pl-md"
        />
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered>
      <div class="row q-pa-md">
        <div class="col-6">
          <a href="https://epfl.ch" target="_blank">
            <img src="/EPFL.svg" style="width: 100px" />
          </a>
        </div>
        <div class="col-6">
          <a href="https://www.epfl.ch/labs/eesd/" target="_blank">
            <img src="/EESD.svg" style="width: 105px" class="float-right" />
          </a>
        </div>
      </div>
      <div v-if="!isBuildings">
        <q-list>
          <q-item-label header class="text-h5">{{
            $t('resources')
          }}</q-item-label>
          <EssentialLink
            v-for="link in essentialLinks"
            :key="link.title"
            v-bind="link"
          />
        </q-list>
      </div>
      <div v-if="isBuildings">
        <q-list>
          <q-item-label header class="text-h5">{{
            $t('filters')
          }}</q-item-label>
        </q-list>
        <experiment-filters></experiment-filters>
      </div>
    </q-drawer>

    <q-drawer side="right" v-model="rightDrawerOpen" bordered>
      <div class="q-pa-md">
        <q-btn
          unelevated
          round
          icon="close"
          @click="toggleRightDrawer"
          class="float-right"
        />
      </div>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import EssentialLink, {
  EssentialLinkProps,
} from 'components/EssentialLink.vue';
import ExperimentFilters from 'src/components/ExperimentFilters.vue';

const route = useRoute();

const isHome = computed(() => route.path === '/');
const isBuildings = computed(() => route.path.startsWith('/buildings'));
const isSubmit = computed(() => route.path.startsWith('/submit'));

const essentialLinks: EssentialLinkProps[] = [
  {
    title: 'EPFL',
    caption: 'epfl.ch',
    icon: 'school',
    link: 'https://epfl.ch',
  },
  {
    title: 'EESD',
    caption: 'epfl.ch/labs/eesd',
    icon: 'record_voice_over',
    link: 'https://www.epfl.ch/labs/eesd/',
  },
  {
    title: 'MAST CLI',
    caption: 'EPFL-ENAC/eesd-mast-cli',
    icon: 'code',
    link: 'https://github.com/EPFL-ENAC/eesd-mast-cli',
  },
];
const leftDrawerOpen = ref(false);
const rightDrawerOpen = ref(false);

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value;
}
function toggleRightDrawer() {
  rightDrawerOpen.value = !rightDrawerOpen.value;
}
</script>
