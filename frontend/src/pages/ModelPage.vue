<template>
  <q-page>
    <q-breadcrumbs class="q-pa-md q-mt-sm q-mb-sm text-h6">
      <q-breadcrumbs-el v-if="experiment" :label="title" icon="house_siding" />
      <q-btn
        v-if="experiment"
        :label="$t('view_test')"
        no-caps
        flat
        icon="analytics"
        color="accent"
        :to="`/test/${experiment.id}`"
      />
    </q-breadcrumbs>
    <q-separator />
    <div class="q-pa-md">
      <experiment-model-view :experiment="experiment"></experiment-model-view>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import { api, baseUrl } from 'src/boot/axios';
import ExperimentModelView from 'components/ExperimentModelView.vue';

const route = useRoute();
const router = useRouter();

const experiment = ref();

watch(() => route.params.id, updateExperiment);

onMounted(updateExperiment);

const title = computed(() => {
  if (experiment.value) {
    return experiment.value.experiment_id
      ? `${experiment.value.description} - ${experiment.value.experiment_id}`
      : experiment.value.description;
  }
  return '';
});

function updateExperiment() {
  api
    .get(`${baseUrl}/experiments/${route.params.id}`)
    .then((response) => (experiment.value = response.data))
    .then(() => {
      if (!experiment.value.model_files) {
        router.push(`/test/${experiment.value.id}`);
      }
    })
    .catch(() => router.push('/error'));
}
</script>
