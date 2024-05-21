<template>
  <div v-if="selected">
    <div class="text-h6">{{ $t('general_information') }}</div>
    <fields-list :items="itemsInfo" :dbobject="selected" />
    <div class="text-h6 q-mt-md">{{ $t('initial_material_properties') }}</div>
    <fields-list :items="itemsProps" :dbobject="selected" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  name: 'NumericalModelFields',
});
</script>
<script setup lang="ts">
import { withDefaults, ref, onMounted } from 'vue';
import FieldsList, { FieldItem } from './FieldsList.vue';
import { NumericalModel } from 'src/components/models';

interface NumericalModelFieldsProps {
  numerical_model: NumericalModel;
}
const props = withDefaults(defineProps<NumericalModelFieldsProps>(), {
  numerical_model: undefined,
});

const selected = ref(props.numerical_model);

const itemsInfo: FieldItem<NumericalModel>[] = [
  {
    field: 'software_used',
    comment: (val: NumericalModel) => val.software_used_comment,
  },
  {
    field: 'modeling_approach',
    comment: (val: NumericalModel) => val.modeling_approach_comment,
  },
  {
    field: 'units',
    comment: (val: NumericalModel) => val.units_comment,
  },
  {
    field: 'frame_elements',
    comment: (val: NumericalModel) => val.frame_elements_comment,
  },
  {
    field: 'diaphragm_elements',
    comment: (val: NumericalModel) => val.diaphragm_elements_comment,
  },
  {
    field: 'damping_model',
    comment: (val: NumericalModel) => val.damping_model_comment,
  },
  {
    field: 'global_geometry_def',
    comment: (val: NumericalModel) => val.global_geometry_def_comment,
  },
  {
    field: 'element_geometry_def',
    comment: (val: NumericalModel) => val.element_geometry_def_comment,
  },
  {
    field: 'mass_def',
    comment: (val: NumericalModel) => val.mass_def_comment,
  },
  {
    field: 'gravity_loads_def',
    comment: (val: NumericalModel) => val.gravity_loads_def_comment,
  },
  {
    field: 'wall_connections',
    comment: (val: NumericalModel) => val.wall_connections_comment,
  },
  {
    field: 'floor_connections',
    comment: (val: NumericalModel) => val.floor_connections_comment,
  },
  {
    field: 'base_support',
    comment: (val: NumericalModel) => val.base_support_comment,
  },
];

const itemsProps: FieldItem<NumericalModel>[] = [
  {
    field: 'elastic_modulus',
    comment: (val: NumericalModel) => val.elastic_modulus_comment,
    unit: 'MPa',
  },
  {
    field: 'shear_modulus',
    comment: (val: NumericalModel) => val.shear_modulus_comment,
    unit: 'MPa',
  },
  {
    field: 'compression_strength',
    comment: (val: NumericalModel) => val.compression_strength_comment,
    unit: 'MPa',
  },
  {
    field: 'tension_strength',
    comment: (val: NumericalModel) => val.tension_strength_comment,
    unit: 'MPa',
  },
  {
    field: 'cohesion',
    comment: (val: NumericalModel) => val.cohesion_comment,
    unit: 'MPa',
  },
  {
    field: 'friction_coeff',
    comment: (val: NumericalModel) => val.friction_coeff_comment,
  },
  {
    field: 'residual_friction_coeff',
    comment: (val: NumericalModel) => val.residual_friction_coeff_comment,
  },
  {
    field: 'damping_ratio',
    comment: (val: NumericalModel) => val.damping_ratio_comment,
    unit: '%',
  },
  {
    field: 'softening_coeff',
    comment: (val: NumericalModel) => val.softening_coeff_comment,
  },
];

watch(() => props.numerical_model, updateNumericalModel);

onMounted(updateNumericalModel);

function updateNumericalModel() {
  if (props.numerical_model) {
    selected.value = props.numerical_model;
  }
}
</script>
