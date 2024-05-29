<template>
  <q-layout view="hHh Lpr lFf">
    <q-header bordered class="bg-white text-grey-10">
      <app-toolbar @toggle="toggleDrawer" />
      <app-header
        v-if="isBuildings2"
        url="Website_Background_Title_Option2.webp"
      />
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
import AppHeader from 'src/components/AppHeader.vue';
import BuildingsPage from 'src/pages/BuildingsPage.vue';
import ExperimentFilters from 'src/components/ExperimentFilters.vue';

const route = useRoute();

const drawerOpen = ref(false);
const miniState = ref(false);

const isBuildings = computed(() => route.path === '/buildings');
const isBuildings2 = computed(() => route.path === '/buildings2');

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
