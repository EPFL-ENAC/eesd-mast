<template>
  <div v-if="selected">
    <fields-list :items="items" :dbobject="selected" />
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

const items: FieldItem<NumericalModel>[] = [
  {
    field: 'software_used',
  },
  {
    field: 'modeling_approach',
  },
  {
    field: 'units',
  },
  {
    field: 'frame_elements',
  },
  {
    field: 'diaphragm_elements',
  },
  {
    field: 'damping_model',
  },
  {
    field: 'global_geometry_def',
  },
  {
    field: 'element_geometry_def',
  },
  {
    field: 'mass_def',
  },
  {
    field: 'gravity_loads_def',
  },
  {
    field: 'wall_connections',
  },
  {
    field: 'floor_connections',
  },
  {
    field: 'base_support',
  },
  {
    field: 'elastic_modulus',
  },
  {
    field: 'shear_modulus',
  },
  {
    field: 'compression_strength',
  },
  {
    field: 'tension_strength',
  },
  {
    field: 'cohesion',
  },
  {
    field: 'friction_coeff',
  },
  {
    field: 'residual_friction_coeff',
  },
  {
    field: 'damping_ratio',
  },
  {
    field: 'softening_coeff',
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
