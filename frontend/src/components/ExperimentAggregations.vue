<template>
  <div>
    <div class="row">
      <div
        class="col-12 col-md-3 col-sm-12"
        v-for="field in fields"
        :key="field"
      >
        <field-frequencies-chart
          :field="field"
          :total="analysis.counts.experiments_count"
          @change:filter="onFilter"
        />
      </div>
    </div>

    <div class="q-pa-md" v-if="analysis.filters.length">
      <q-btn
        dense
        flat
        no-caps
        color="primary"
        :label="$t('reset_filters')"
        @click="analysis.resetFilters()"
      ></q-btn>
      <q-chip
        removable
        size="sm"
        color="primary"
        text-color="white"
        v-for="criteria in analysis.filters"
        :key="criteria.field"
        :label="criteriaLabel(criteria)"
        class="on-right"
        @remove="analysis.updateFilters(criteria)"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { FieldValue } from './models';
import { testScaleLabel } from 'src/utils/numbers';
export default defineComponent({
  name: 'ExperimentAggregations',
});
</script>
<script setup lang="ts">
import FieldFrequenciesChart from './charts/FieldFrequenciesChart.vue';
import { useAnalysisStore } from 'src/stores/analysis';

const analysis = useAnalysisStore();
const { t } = useI18n({ useScope: 'global' });

const fields = computed(() => {
  return analysis.frequencies === null ? [] : Object.keys(analysis.frequencies);
});

onMounted(() => {
  analysis.loadExperimentsAnalysis();
});

function criteriaLabel(criteria: FieldValue) {
  const val =
    criteria.field === 'test_scale'
      ? testScaleLabel(criteria.value)
      : criteria.value;
  return `${t(criteria.field)}: ${val}`;
}

function onFilter(value: FieldValue | undefined) {
  analysis.updateFilters(value);
}
</script>
