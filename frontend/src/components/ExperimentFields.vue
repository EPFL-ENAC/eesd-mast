<template>
  <div v-if="selected">
    <fields-list :items="items" :dbobject="selected" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  name: 'ExperimentFields',
});
</script>
<script setup lang="ts">
import { withDefaults, ref, onMounted } from 'vue';
import FieldsList, { FieldItem } from './FieldsList.vue';
import { Experiment } from 'src/components/models';
import { testScaleLabel, makeLiteralLabel } from 'src/utils/numbers';

interface ExperimentFieldsProps {
  experiment: Experiment;
}
const props = withDefaults(defineProps<ExperimentFieldsProps>(), {
  experiment: undefined,
});

const selected = ref(props.experiment);

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
      val.masonry_wall_thickness
        ? makeLiteralLabel(val.masonry_wall_thickness)
        : '-',
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

watch(() => props.experiment, updateExperiment);

onMounted(updateExperiment);

function updateExperiment() {
  if (props.experiment) {
    selected.value = props.experiment;
  }
}
</script>
