<template>
  <q-page>
    <q-breadcrumbs class="q-pa-md q-mt-sm q-mb-sm text-h6">
      <q-breadcrumbs-el :label="$t('buildings')" to="../buildings" />
      <q-breadcrumbs-el v-if="experiment" :label="title" icon="analytics" />
      <q-btn
        v-if="hasModels"
        :label="$t('view_model')"
        no-caps
        flat
        icon="house_siding"
        color="secondary"
        :to="`/model/${experiment.id}`"
      />
    </q-breadcrumbs>
    <q-separator />
    <div class="q-pa-md">
      <experiment-test-view :experiment="experiment"></experiment-test-view>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import { api, baseUrl } from 'src/boot/axios';
import ExperimentTestView from 'components/ExperimentTestView.vue';

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

const hasModels = computed(
  () => experiment.value && experiment.value?.model_files
);

function updateExperiment() {
  api
    .get(`${baseUrl}/experiments/${route.params.id}`)
    .then((response) => (experiment.value = response.data))
    .catch(() => router.push('/error'));
}
</script>
