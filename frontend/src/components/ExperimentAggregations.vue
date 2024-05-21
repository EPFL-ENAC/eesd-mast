<template>
  <div class="q-mb-xl">
    <div class="q-pa-md">
      <div v-if="analysis.filters.length">
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
          :label="$t('show_buildings')"
          @click="onShowExperiments"
        ></q-btn>
      </div>
      <div v-else class="q-pa-xs text-caption text-grey-8">
        <q-icon name="info" size="sm"></q-icon>
        <span class="on-right">{{ $t('aggregations_hint') }}</span>
      </div>
    </div>
    <div class="row">
      <div
        class="col-12 col-md-3 col-sm-12"
        v-for="field in fields"
        :key="field"
      >
        <field-frequencies-chart
          :field="field"
          @change:filter="onFilter"
          class="q-ml-md q-mr-md"
        />
      </div>
    </div>

    <q-tabs
      v-model="tab"
      dense
      class="text-grey-8 q-mt-md q-ml-md q-mr-md"
      active-color="primary"
      indicator-color="primary"
      align="center"
      narrow-indicator
    >
      <q-tab name="parallel" :label="$t('key_features')" />
      <q-tab name="vulnerabilities" :label="$t('vulnerability')" />
    </q-tabs>

    <q-tab-panels v-model="tab" animated>
      <q-tab-panel name="parallel">
        <div class="row">
          <div class="col-12">
            <experiments-parallel-chart class="q-ml-md q-mr-md" />
          </div>
        </div>
      </q-tab-panel>
      <q-tab-panel name="vulnerabilities">
        <div class="row">
          <div class="col-12 col-md-6">
            <run-results-vulnerabilities-chart class="q-ml-md q-mr-md" />
          </div>
          <div class="col-12 col-md-6">
            <run-results-fragilities-chart class="q-ml-md q-mr-md" />
          </div>
        </div>
      </q-tab-panel>
    </q-tab-panels>
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
import RunResultsVulnerabilitiesChart from './charts/RunResultsVulnerabilitiesChart.vue';
import RunResultsFragilitiesChart from './charts/RunResultsFragilitiesChart.vue';
import { useAnalysisStore } from 'src/stores/analysis';
import { isStone, isMixedMaterial } from 'src/utils/criteria';

const router = useRouter();
const analysis = useAnalysisStore();
const filters = useFiltersStore();
const { t } = useI18n({ useScope: 'global' });

const tab = ref('parallel');

const fields = computed(() => {
  // cumulate frequencies of stones
  if (analysis.frequencies === null) return [];
  const stoneFreq = Object.keys(analysis.frequencies.masonry_unit_material)
    .filter(isStone)
    .reduce((acc, key) => {
      return acc + (analysis.frequencies?.masonry_unit_material[key] || 0);
    }, 0);
  const newMumFreq: FieldFrequencies = {
    Stone: stoneFreq,
  };
  Object.keys(analysis.frequencies.masonry_unit_material)
    .filter((key) => !isStone(key))
    .forEach((key) => {
      if (analysis.frequencies !== null) {
        newMumFreq[key] = analysis.frequencies.masonry_unit_material[key];
      }
    });
  analysis.frequencies.masonry_unit_material = newMumFreq;

  // cumulate frequencies of mixed materials
  const mixedFreq = Object.keys(analysis.frequencies.diaphragm_material)
    .filter(isMixedMaterial)
    .reduce((acc, key) => {
      return acc + (analysis.frequencies?.diaphragm_material[key] || 0);
    }, 0);
  const newMatFreq: FieldFrequencies = {
    Mixed: mixedFreq,
  };
  Object.keys(analysis.frequencies.diaphragm_material)
    .filter((key) => !isMixedMaterial(key))
    .forEach((key) => {
      if (analysis.frequencies !== null) {
        newMatFreq[key] = analysis.frequencies.diaphragm_material[key];
      }
    });
  analysis.frequencies.diaphragm_material = newMatFreq;

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
