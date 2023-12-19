<template>
  <div v-if="selected">
    <div class="text-h5">
      {{ selected.description }}
      <span v-if="selected.experiment_id">
        - {{ selected.experiment_id }}
      </span>
    </div>
    <div class="q-mb-md">
      <span class="text-subtitle1 on-left">{{ selected.reference }}</span>
      <q-chip
        v-for="exp in other_experiments"
        :key="exp.id"
        :label="exp.experiment_id"
        :title="exp.description"
        clickable
        @click="onExperiment(exp)"
      />
    </div>

    <div class="text-subtitle1 text-grey-8">
      {{ selected.experimental_campaign_motivation }}
    </div>
    <q-card flat class="q-mt-md q-mb-md">
      <q-card-section>
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
      </q-card-section>
    </q-card>
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
      <q-tab name="reference" :label="$t('reference')" />
      <q-tab name="run_results" :label="$t('run_results')" />
    </q-tabs>

    <q-separator />

    <q-tab-panels v-model="tab" animated>
      <q-tab-panel name="details">
        <fields-list :items="items" :dbobject="selected" />
      </q-tab-panel>

      <q-tab-panel name="reference">
        <reference-view :experiment="selected" />
      </q-tab-panel>

      <q-tab-panel name="run_results">
        <run-results-view :experiment="selected" />
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
import { defineProps, withDefaults, ref, onMounted, computed } from 'vue';
import { baseUrl } from 'src/boot/axios';
import ReferenceView from './ReferenceView.vue';
import RunResultsView from './RunResultsView.vue';
import FieldsList from './FieldsList.vue';
import { Experiment } from 'src/components/models';
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
const reference_experiments = ref([]);

const items = [
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
    format: (val: any) =>
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
    format: (val: any) =>
      val.masonry_wall_thickness ? val.masonry_wall_thickness.join(' / ') : '-',
    unit: 'mm',
  },
  {
    field: 'wall_leaves_nb',
  },
  {
    field: 'internal_walls',
    format: (val: any) => (val.open_measured_data ? 'Yes' : 'No'),
  },
  {
    field: 'mechanical_connectors',
  },
  {
    field: 'connectors_activation',
  },
  {
    field: 'retrofitted',
    format: (val: any) => (val.open_measured_data ? 'Yes' : 'No'),
  },
  {
    field: 'retrofitting_application',
  },
  {
    field: 'retrofitting_type',
    format: (val: any) =>
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
    format: (val: any) =>
      val.material_characterizations
        ? val.material_characterizations.join(' / ')
        : '-',
  },
  {
    field: 'associated_test_types',
    format: (val: any) =>
      val.associated_test_types ? val.associated_test_types.join(' / ') : '-',
  },
  {
    field: 'material_characterization_refs',
    format: (val: any) =>
      val.material_characterization_refs
        ? val.material_characterization_refs.join(' / ')
        : '-',
  },
  {
    field: 'digitalized_data',
    format: (val: any) => (val.open_measured_data ? 'Yes' : 'No'),
  },
  {
    field: 'experimental_results_reported',
    format: (val: any) =>
      val.experimental_results_reported
        ? val.experimental_results_reported.join(' / ')
        : '-',
  },
  {
    field: 'open_measured_data',
    format: (val: any) => (val.open_measured_data ? 'Yes' : 'No'),
  },
  {
    field: 'link_to_open_measured_data',
    html: (val: any) =>
      val.link_to_open_measured_data
        ? `<a href="${val.link_to_open_measured_data}" target="_blank">${val.link_to_open_measured_data}</a>`
        : '-',
  },
  {
    field: 'crack_types_observed',
    format: (val: any) =>
      val.crack_types_observed ? val.crack_types_observed.join(' / ') : '-',
  },
];

const other_experiments = computed(() => {
  return selected.value
    ? reference_experiments.value.filter((e: any) => e.id !== selected.value.id)
    : [];
});

const onExperiment = (exp: Experiment) => {
  selected.value = exp;
};

onMounted(() => {
  if (props.experiment) {
    referencesStore
      .fetchExperiments(props.experiment.reference_id)
      .then((res) => {
        reference_experiments.value = res;
      });
    selected.value = props.experiment;
  }
});
</script>
