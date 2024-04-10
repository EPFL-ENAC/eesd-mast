<template>
  <div>
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
      <q-btn
        dense
        flat
        no-caps
        icon="visibility"
        color="secondary"
        :label="$t('show_tested_buildings')"
        @click="onShowExperiments"
      ></q-btn>
    </div>
    <div class="row">
      <div
        class="col-12 col-md-3 col-sm-12"
        v-for="field in fields"
        :key="field"
      >
        <field-frequencies-chart :field="field" @change:filter="onFilter" />
      </div>
    </div>
    <div>
      <experiments-parallel-chart />
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
import { FieldFrequencies } from './models';
import FieldFrequenciesChart from './charts/FieldFrequenciesChart.vue';
import ExperimentsParallelChart from './charts/ExperimentsParallelChart.vue';
import { useAnalysisStore } from 'src/stores/analysis';
import { isStone } from 'src/utils/criteria';

const router = useRouter();
const analysis = useAnalysisStore();
const filters = useFiltersStore();
const { t } = useI18n({ useScope: 'global' });

const fields = computed(() => {
  // cumulate frequencies of stones
  if (analysis.frequencies === null) return [];
  const stoneFreq = Object.keys(analysis.frequencies.masonry_unit_material)
    .filter(isStone)
    .reduce((acc, key) => {
      return acc + (analysis.frequencies?.masonry_unit_material[key] || 0);
    }, 0);
  const newMum: FieldFrequencies = {
    Stone: stoneFreq,
  };
  Object.keys(analysis.frequencies.masonry_unit_material)
    .filter((key) => !isStone(key))
    .forEach((key) => {
      if (analysis.frequencies !== null) {
        newMum[key] = analysis.frequencies.masonry_unit_material[key];
      }
    });
  analysis.frequencies.masonry_unit_material = newMum;
  return Object.keys(analysis.frequencies);
});

onMounted(() => {
  analysis.loadExperimentsAnalysis();
});

function criteriaLabel(criteria: FieldValue) {
  if (criteria.field === 'test_scale') {
    return `${t(criteria.field)}: ${testScaleLabel(criteria.value)}`;
  }
  const val = criteria.value === null ? 'N/A' : criteria.value;
  return `${t(criteria.field)}: ${val}`;
}

function onFilter(criteria: FieldValue | undefined) {
  analysis.updateFilters(criteria);
}

function onShowExperiments() {
  filters.resetFilters();
  filters.applySelections(analysis.filters);
  router.push('/buildings');
}
</script>
