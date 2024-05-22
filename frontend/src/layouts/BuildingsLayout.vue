<template>
  <q-layout view="hHh Lpr lFf">
    <q-header bordered class="bg-white text-grey-10">
      <app-toolbar @toggle="toggleDrawer" />
    </q-header>

    <q-drawer
      v-model="drawerOpen"
      :mini="!drawerOpen || miniState"
      show-if-above
      bordered
    >
      <div v-if="!miniState">
        <q-list>
          <q-item-label header class="text-h6 q-ml-md q-pl-xs">{{
            $t('filters')
          }}</q-item-label>
        </q-list>
        <experiment-filters></experiment-filters>
      </div>
      <div
        v-if="!$q.screen.lt.md"
        class="absolute"
        style="top: 10px; right: 10px"
      >
        <q-btn
          dense
          round
          unelevated
          color="accent"
          :icon="miniState ? 'chevron_right' : 'chevron_left'"
          @click="miniState = !miniState"
        />
      </div>
    </q-drawer>

    <q-page-container>
      <buildings-page />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import AppToolbar from 'src/components/AppToolbar.vue';
import BuildingsPage from 'src/pages/BuildingsPage.vue';
import ExperimentFilters from 'src/components/ExperimentFilters.vue';

const route = useRoute();

const drawerOpen = ref(false);
const miniState = ref(false);

const isBuildings = computed(() => route.path.startsWith('/buildings'));

watch(
  () => isBuildings.value,
  () => {
    drawerOpen.value = isBuildings.value;
  }
);

function toggleDrawer() {
  drawerOpen.value = !drawerOpen.value;
}
</script>
