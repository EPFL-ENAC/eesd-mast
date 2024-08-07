<template>
  <div class="q-mb-md">
    <div class="q-ml-xl q-mr-xl">
      <div class="q-mt-md">
        <span class="text-h6">
          {{ $t('aggregations_title') }}
        </span>
        <q-btn
          flat
          round
          size="lg"
          icon="help_outline"
          class="on-right text-primary q-pb-xs"
        >
          <q-tooltip v-model="showPieTips" class="bg-grey-7 text-white">
            <div
              class="q-pt-md q-pl-md q-pr-md"
              style="width: 400px; font-size: medium"
            >
              <q-markdown :src="$t('overview_help')" />
            </div>
          </q-tooltip>
        </q-btn>
        <q-toggle
          v-model="tabToggle"
          :label="$t('show_vulnerability')"
          left-label
          color="accent"
          size="xl"
          keep-color
          class="on-right q-pb-xs"
          @update:model-value="onTabToggle"
        />
      </div>
      <div class="row">
        <q-chip
          removable
          size="sm"
          color="secondary"
          text-color="white"
          v-for="criteria in analysis.filters"
          :key="criteria.field"
          :label="criteriaLabel(criteria)"
          class="on-left q-ml-none q-mt-sm"
          @remove="analysis.updateFilters(criteria)"
        />
        <q-btn
          v-if="analysis.filters.length"
          dense
          flat
          no-caps
          color="secondary"
          :label="$t('reset_filters')"
          @click="analysis.resetFilters()"
          class="q-mb-sm"
        ></q-btn>
        <q-btn
          v-if="analysis.filters.length"
          dense
          flat
          no-caps
          icon="visibility"
          color="accent"
          :label="$t('show_buildings')"
          class="on-right on-left q-mb-sm"
          @click="onShowExperiments"
        ></q-btn>
        <div class="q-mt-sm q-mb-sm q-pb-xs">
          {{ countLabel }}
        </div>
      </div>
    </div>

    <div class="row q-col-gutter-md q-mt-md justify-center">
      <div v-for="field in fields" :key="field" style="width: 450px">
        <field-frequencies-chart :field="field" @change:filter="onFilter" />
      </div>
    </div>

    <div class="q-ml-xl q-mr-xl">
      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="parallel" class="q-pa-none">
          <div class="row">
            <div class="col-12">
              <experiments-parallel-chart class="q-ml-lg q-mr-lg" />
            </div>
          </div>
        </q-tab-panel>
        <q-tab-panel name="vulnerabilities" class="q-pa-none">
          <div class="row">
            <div class="col-12 col-md-6">
              <run-results-vulnerabilities-chart
                :data="analysis.runResultsVulnerabilities"
                class="q-ml-md q-mr-md"
              />
              <div class="q-ma-md q-pl-lg q-pr-md text-grey-9">
                <q-markdown :src="VulnerabilitiesMd" no-line-numbers />
              </div>
            </div>
            <div class="col-12 col-md-6">
              <run-results-fragilities-chart
                :data="analysis.runResultsFragilities"
                class="q-ml-md q-mr-md"
              />
              <div class="q-ma-md q-pl-lg q-pr-md text-grey-9">
                <q-markdown :src="FragilitiesMd" no-line-numbers />
              </div>
            </div>
          </div>
        </q-tab-panel>
      </q-tab-panels>
      <q-tooltip
        v-model="showPlotlyTip"
        anchor="top middle"
        self="top middle"
        no-parent-event
        class="bg-grey-7 text-white"
      >
        <div
          class="q-pt-md q-pl-md q-pr-md"
          style="width: 400px; font-size: medium"
        >
          <q-markdown :src="$t('plotly_help')" />
        </div>
      </q-tooltip>
    </div>
  </div>
</template>

<script lang="ts">
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
import VulnerabilitiesMd from 'src/assets/vulnerabilities.md';
import FragilitiesMd from 'src/assets/fragilities.md';
import { Settings } from 'src/stores/settings';

const router = useRouter();
const settingsStore = useSettingsStore();
const analysis = useAnalysisStore();
const filters = useFiltersStore();
const { t } = useI18n({ useScope: 'global' });

const tabToggle = ref(false);
const showPlotlyTip = ref(false);
const showPieTips = ref(false);

const tab = computed(() => (tabToggle.value ? 'vulnerabilities' : 'parallel'));
const countLabel = computed(() => {
  return `${t('buildings_count', { count: analysis.buildings_counts })}, ${t(
    'models_count',
    { count: analysis.models_counts }
  )}`;
});

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

  return Object.keys(analysis.frequencies).filter((f) => f !== 'model_files');
});

onMounted(() => {
  analysis.loadExperimentsAnalysis();
  if (settingsStore.settings?.intro_shown) {
    triggerPieTips();
  }
});

watch(
  () => settingsStore.settings,
  () => {
    if (settingsStore.settings?.intro_shown) {
      triggerPieTips();
    }
  }
);

function criteriaLabel(criteria: FieldValue) {
  if (criteria.field === 'test_scale') {
    return `${t(criteria.field)}: ${testScaleLabel(criteria.value)}`;
  }
  const field =
    criteria.field === 'model_files' ? 'numerical_model' : criteria.field;
  const val = criteria.value === null ? 'N/A' : criteria.value;
  return `${t(field)}: ${val}`;
}

function onFilter(criteria: FieldValue | undefined) {
  analysis.updateFilters(criteria);
}

function onShowExperiments() {
  filters.resetFilters();
  filters.applySelections(analysis.filters);
  router.push('/buildings');
}

function onTabToggle() {
  if (tabToggle.value && !settingsStore.settings?.vulnerabilities_tips) {
    showPlotlyTip.value = true;
    setTimeout(() => {
      showPlotlyTip.value = false;
      const settings = { ...settingsStore.settings } as Settings;
      settings.vulnerabilities_tips = true;
      settingsStore.saveSettings(settings);
    }, 5000);
  } else if (!tabToggle.value) {
    showPlotlyTip.value = false;
  }
}

function triggerPieTips() {
  if (!showPieTips.value && !settingsStore.settings?.frequencies_tips) {
    showPieTips.value = true;
    setTimeout(() => {
      showPieTips.value = false;
      const settings = { ...settingsStore.settings } as Settings;
      settings.frequencies_tips = true;
      settingsStore.saveSettings(settings);
    }, 5000);
  }
}
</script>
