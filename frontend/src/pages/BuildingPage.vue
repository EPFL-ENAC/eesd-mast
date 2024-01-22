<template>
  <q-page>
    <q-breadcrumbs class="q-pa-md q-mt-sm q-mb-sm text-h5">
      <q-breadcrumbs-el :label="$t('tested_buildings')" to="../buildings" />
      <q-breadcrumbs-el v-if="experiment" :label="experiment.description" />
    </q-breadcrumbs>
    <q-separator />
    <div class="q-pa-md">
      <experiment-view :experiment="experiment"></experiment-view>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import { api, baseUrl } from 'src/boot/axios';
import ExperimentView from 'components/ExperimentView.vue';

const route = useRoute();

const experiment = ref();

watch(() => route.params.id, updateExperiment);

onMounted(updateExperiment);

function updateExperiment() {
  api
    .get(`${baseUrl}/experiments/${route.params.id}`)
    .then((response) => (experiment.value = response.data));
}
</script>
