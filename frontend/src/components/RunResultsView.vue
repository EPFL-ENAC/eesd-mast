<template>
  <div>
    <q-table
      :rows="runResults"
      :columns="columns"
      row-key="run_id"
      hide-pagination
      :rows-per-page-options="[0]"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  name: 'RunResultsView',
});
</script>
<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { defineProps, withDefaults, onMounted, ref } from 'vue';
import { useRunResultsStore } from 'src/stores/run_results';
import { Experiment } from 'src/components/models';

const { t } = useI18n({ useScope: 'global' });

export interface RunResultsViewProps {
  experiment: Experiment;
}
const props = withDefaults(defineProps<RunResultsViewProps>(), {
  experiment: undefined,
});

const runResultsStore = useRunResultsStore();
const runResults = ref();

const columns = [
  'run_id',
  'nominal_pga_x',
  'nominal_pga_y',
  'nominal_pga_z',
  'actual_pga_x',
  'actual_pga_y',
  'actual_pga_z',
  'dg_reported',
  'dg_derived',
  'max_top_drift_x',
  'max_top_drift_y',
  'residual_top_drift_x',
  'residual_top_drift_y',
  'base_shear_coef',
  'reported_t1_x',
  'reported_t1_y',
].map((name) => {
  return {
    name: name,
    required: true,
    label: t(name),
    align: 'left',
    field: name,
    sortable: true,
  };
});

onMounted(() => {
  if (props.experiment) {
    runResultsStore.fetchRunResults(props.experiment.id).then((res) => {
      runResults.value = res;
    });
  }
});
</script>
