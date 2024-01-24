<template>
  <div v-if="selected">
    <div class="q-mb-md">
      <span class="text-subtitle1 on-left">{{ selected.reference }}</span>
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
          :to="`/building/${exp.id}`"
        />
      </span>
    </div>

    <div class="text-subtitle1 text-grey-8">
      {{ selected.experimental_campaign_motivation }}
    </div>

    <div class="row q-gutter-md q-mt-md q-mb-md">
      <div class="col-12 col-md-auto">
        <div>
          <q-img
            v-if="imageDisplay === 'fitted'"
            :src="`${baseUrl}/files/${selected.scheme.path}`"
            :alt="`${selected.description} [${selected.reference}]`"
            spinner-color="grey-6"
            width="250px"
          />
          <img
            v-else
            :src="`${baseUrl}/files/${selected.scheme.path}`"
            :alt="`${selected.description} [${selected.reference}]`"
            spinner-color="grey-6"
          />
        </div>
        <div>
          <span class="text-caption">{{ $t('image_size') }}</span>
          <q-btn
            :disable="imageDisplay === 'fitted'"
            :label="$t('fitted_size')"
            dense
            flat
            no-caps
            size="sm"
            @click="imageDisplay = 'fitted'"
            class="on-left on-right"
          />
          <q-btn
            :disable="imageDisplay !== 'fitted'"
            :label="$t('original_size')"
            dense
            flat
            no-caps
            size="sm"
            @click="imageDisplay = 'full'"
          />
        </div>
      </div>
      <div class="col">
        <div v-for="file in periodDGEvolutionFiles" :key="file.path">
          <q-img
            :src="`${baseUrl}/files/${file.path}`"
            spinner-color="grey-6"
          />
        </div>
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
      <q-tab name="3d_model" :label="$t('3d_model')" />
      <q-tab name="run_results" :label="$t('run_results')" />
      <q-tab name="files" :label="$t('files')" :alert="hasFiles()" />
      <q-tab name="reference" :label="$t('reference')" />
    </q-tabs>

    <q-separator />

    <q-tab-panels v-model="tab" animated>
      <q-tab-panel name="details">
        <fields-list :items="items" :dbobject="selected" />
      </q-tab-panel>

      <q-tab-panel name="3d_model">
        <div v-if="threeDModelFiles.length === 0" class="text-grey-6">
          {{ $t('no_3d_model') }}
        </div>
        <div v-else v-for="file in threeDModelFiles" :key="file.path">
          <vtk-viewer :file="file" />
        </div>
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
  name: 'ExperimentView',
});
</script>
<script setup lang="ts">
import { withDefaults, ref, onMounted } from 'vue';
import { baseUrl } from 'src/boot/axios';
import VtkViewer from './VtkViewer.vue';
import ReferenceView from './ReferenceView.vue';
import RunResultsView from './RunResultsView.vue';
import ExperimentFilesView from './ExperimentFilesView.vue';
import FieldsList, { FieldItem } from './FieldsList.vue';
import { Experiment, FileNode } from 'src/components/models';
import { useReferencesStore } from 'src/stores/references';

const referencesStore = useReferencesStore();

export interface ExperimentViewProps {
  experiment: Experiment;
}
const props = withDefaults(defineProps<ExperimentViewProps>(), {
  experiment: undefined,
});

const imageDisplay = ref('fitted');
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
    field: 'material_characterizations',
    format: (val: Experiment) =>
      val.material_characterizations
        ? val.material_characterizations.join(' / ')
        : '-',
  },
  {
    field: 'associated_test_types',
    format: (val: Experiment) =>
      val.associated_test_types ? val.associated_test_types.join(' / ') : '-',
  },
  {
    field: 'material_characterization_refs',
    format: (val: Experiment) =>
      val.material_characterization_refs
        ? val.material_characterization_refs.join(' / ')
        : '-',
  },
  {
    field: 'digitalized_data',
    format: (val: Experiment) => (val.open_measured_data ? 'Yes' : 'No'),
  },
  {
    field: 'experimental_results_reported',
    format: (val: Experiment) =>
      val.experimental_results_reported
        ? val.experimental_results_reported.join(' / ')
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
  {
    field: 'crack_types_observed',
    format: (val: Experiment) =>
      val.crack_types_observed ? val.crack_types_observed.join(' / ') : '-',
  },
];

function hasFiles() {
  return (
    selected.value &&
    selected.value.files !== null &&
    selected.value.files.children.length > 0
  );
}

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

const periodDGEvolutionFiles = computed(() => {
  const nodes: FileNode[] = [];
  if (selected.value.files && selected.value.files.children) {
    selected.value.files.children.forEach((element: FileNode) => {
      if (element.name === 'Period and DG evolution' && element.children) {
        nodes.push(...element.children);
      }
    });
  }
  return nodes;
});

const threeDModelFiles = computed(() => {
  const nodes: FileNode[] = [];
  if (selected.value.files && selected.value.files.children) {
    selected.value.files.children.forEach((element: FileNode) => {
      if (element.name === '3D model' && element.children) {
        nodes.push(
          ...element.children.filter(
            (f) => f.name.endsWith('.vtp') || f.alt_name?.endsWith('.vtp')
          )
        );
      }
    });
  }
  return nodes;
});
</script>
