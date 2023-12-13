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
        <q-btn flat dense :label="$t('overview')" no-caps to="/" />
        <q-btn
          flat
          dense
          :label="$t('tested_buildings')"
          no-caps
          to="/buildings"
          class="on-left on-right"
        />
        <q-btn flat dense :label="$t('data_submission')" no-caps to="/submit" />
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered>
      <div class="row q-pa-md">
        <div class="col-6">
          <a href="https://epfl.ch" target="_blank">
            <img src="EPFL.svg" style="width: 100px" />
          </a>
        </div>
        <div class="col-6">
          <a href="https://www.epfl.ch/labs/eesd/" target="_blank">
            <img src="EESD.svg" style="width: 105px" class="float-right" />
          </a>
        </div>
      </div>
      <q-list>
        <q-item-label header> Essential Links </q-item-label>

        <EssentialLink
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import EssentialLink, {
  EssentialLinkProps,
} from 'components/EssentialLink.vue';

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

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value;
}
</script>
