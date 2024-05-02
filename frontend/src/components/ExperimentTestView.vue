<template>
  <div v-if="selected">
    <div class="q-mb-md">
      <span class="text-h6 on-left">{{ selected.reference.reference }}</span>
      <q-chip
        v-if="selected.reference.link_to_experimental_paper"
        icon="article"
        color="primary"
        text-color="white"
        class="on-left"
      >
        <a
          :href="selected.reference.link_to_experimental_paper"
          target="_blank"
          style="text-decoration: none; color: white"
        >
          {{ $t('paper') }}
        </a>
      </q-chip>
      <q-chip
        v-if="selected.reference.link_to_request_data"
        icon="grid_on"
        color="grey-7"
        text-color="white"
        class="on-left"
      >
        <a
          :href="selected.reference.link_to_request_data"
          target="_blank"
          style="text-decoration: none; color: white"
        >
          {{ $t('data') }}
        </a>
      </q-chip>
      <span v-if="reference_experiments.length > 1">
        <q-btn
          v-for="exp in reference_experiments"
          :key="exp.id"
          no-caps
          rounded
          :label="exp.experiment_id || exp.id"
          :title="exp.description"
          :disable="exp.id === selected.id"
          class="on-left"
          :class="exp.id === selected.id ? 'bg-primary text-white' : ''"
          :to="`/test/${exp.id}`"
        />
      </span>
    </div>
    <div v-if="selected.experimental_campaign_motivation">
      <div class="text-caption">
        {{ $t('test_motivation') }}
      </div>
      <div class="text-subtitle1 text-grey-8">
        {{ selected.experimental_campaign_motivation }}
      </div>
    </div>
    <div class="row q-gutter-md q-mt-md q-mb-md">
      <div class="col-12 col-md-auto">
        <div v-if="selected.scheme">
          <div>
            <q-img
              :src="schemeUrl"
              :alt="`${selected.description} [${selected.reference}]`"
              spinner-color="grey-6"
              width="250px"
            />
          </div>
          <div>
            <a :href="schemeUrl" target="_blank" class="text-caption">{{
              $t('original_image')
            }}</a>
          </div>
        </div>
      </div>
      <div class="col-12 col-md">
        <pga-chart :experiment="selected" direction="x" :height="300" />
        <pga-chart :experiment="selected" direction="y" :height="300" />
      </div>
      <div class="col-12 col-md">
        <dg-chart :experiment="selected" direction="x" :height="300" />
        <dg-chart :experiment="selected" direction="y" :height="300" />
      </div>
    </div>

    <div class="q-ma-md"></div>
    <div class="q-ma-md"></div>
    <q-tabs
      v-model="tab"
      dense
      class="text-grey"
      active-color="primary"
      indicator-color="primary"
      align="justify"
      narrow-indicator
    >
      <q-tab name="details" :label="$t('details')" />
      <q-tab name="run_results" :label="$t('run_results')" />
      <q-tab name="files" :label="$t('files')" />
      <q-tab name="reference" :label="$t('reference')" />
    </q-tabs>

    <q-separator />

    <q-tab-panels v-model="tab" animated>
      <q-tab-panel name="details">
        <fields-list :items="items" :dbobject="selected" />
      </q-tab-panel>

      <q-tab-panel name="run_results">
        <run-results-view :experiment="selected" />
      </q-tab-panel>

      <q-tab-panel name="files">
        <experiment-files-view :experiment="selected" />
      </q-tab-panel>

      <q-tab-panel name="reference">
        <reference-view :experiment="selected" />
      </q-tab-panel>
    </q-tab-panels>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  name: 'ExperimentTestView',
});
</script>
<script setup lang="ts">
import { withDefaults, ref, onMounted } from 'vue';
import { baseUrl } from 'src/boot/axios';
import ReferenceView from './ReferenceView.vue';
import RunResultsView from './RunResultsView.vue';
import ExperimentFilesView from './ExperimentFilesView.vue';
import FieldsList, { FieldItem } from './FieldsList.vue';
import PgaChart from './charts/PgaChart.vue';
import DgChart from './charts/DgChart.vue';
import { Experiment } from 'src/components/models';
import { testScaleLabel } from 'src/utils/numbers';
import { useReferencesStore } from 'src/stores/references';

const referencesStore = useReferencesStore();

interface ExperimentViewProps {
  experiment: Experiment;
}
const props = withDefaults(defineProps<ExperimentViewProps>(), {
  experiment: undefined,
});

const tab = ref('details');
const selected = ref();
const reference_experiments = ref<Experiment[]>([]);

const items: FieldItem<Experiment>[] = [
  {
    field: 'storeys_nb',
  },
  {
    field: 'building_height',
    unit: 'm',
  },
  {
    field: 'total_building_height',
    unit: 'm',
  },
  {
    field: 'test_scale',
    format: (val: Experiment) => testScaleLabel(val.test_scale),
  },
  {
    field: 'simultaneous_excitations_nb',
  },
  {
    field: 'applied_excitation_directions',
    format: (val: Experiment) =>
      val.applied_excitation_directions
        ? val.applied_excitation_directions.join(' / ')
        : '-',
  },
  {
    field: 'diaphragm_material',
  },
  {
    field: 'roof_material_geometry',
  },
  {
    field: 'masonry_unit_material',
  },
  {
    field: 'masonry_unit_type',
  },
  {
    field: 'mortar_type',
  },
  {
    field: 'masonry_compressive_strength',
    unit: 'MPa',
  },
  {
    field: 'masonry_wall_thickness',
    format: (val: Experiment) =>
      val.masonry_wall_thickness ? val.masonry_wall_thickness.join(' / ') : '-',
    unit: 'mm',
  },
  {
    field: 'wall_leaves_nb',
  },
  {
    field: 'internal_walls',
    format: (val: Experiment) => (val.internal_walls ? 'Yes' : 'No'),
  },
  {
    field: 'mechanical_connectors',
  },
  {
    field: 'connectors_activation',
  },
  {
    field: 'retrofitted',
    format: (val: Experiment) => (val.retrofitted ? 'Yes' : 'No'),
  },
  {
    field: 'retrofitting_application',
  },
  {
    field: 'retrofitting_type',
    format: (val: Experiment) =>
      val.retrofitting_type ? val.retrofitting_type.join(' / ') : '-',
  },
  {
    field: 'first_estimated_fundamental_period',
  },
  {
    field: 'last_estimated_fundamental_period',
  },
  {
    field: 'max_horizontal_pga',
  },
  {
    field: 'max_estimated_dg',
  },
  {
    field: 'material_characterization_refs',
    format: (val: Experiment) =>
      val.material_characterization_refs
        ? val.material_characterization_refs.join(' / ')
        : '-',
  },
  {
    field: 'open_measured_data',
    format: (val: Experiment) => (val.open_measured_data ? 'Yes' : 'No'),
  },
  {
    field: 'link_to_open_measured_data',
    html: (val: Experiment) =>
      val.link_to_open_measured_data
        ? `<a href="${val.link_to_open_measured_data}" target="_blank">${val.link_to_open_measured_data}</a>`
        : '-',
  },
];

const schemeUrl = computed(() => {
  if (selected.value && selected.value.scheme) {
    return `${baseUrl}/files/${selected.value.scheme.path}`;
  }
  return '';
});

watch(() => props.experiment, updateExperiment);

onMounted(updateExperiment);

function updateExperiment() {
  if (props.experiment) {
    referencesStore
      .fetchExperiments(props.experiment.reference_id)
      .then((res) => {
        reference_experiments.value = res;
      });
    selected.value = props.experiment;
  }
}
</script>
