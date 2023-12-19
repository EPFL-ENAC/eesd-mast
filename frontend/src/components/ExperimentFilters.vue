<template>
  <div>
    <q-tree
      class="col-12 col-sm-6"
      :nodes="filterNodes"
      node-key="key"
      no-connectors
      tick-strategy="leaf"
      v-model:ticked="filters.selections"
      @update:ticked="onFilterTicked"
    >
      <template v-slot:body-storeys>
        <q-input
          v-show="filters.selections.indexOf('storeys_nb') !== -1"
          :disable="filters.selections.indexOf('storeys_nb') === -1"
          v-model.number="filters.storeysNb"
          type="number"
          dense
          style="max-width: 200px"
          class="q-ml-lg"
          :rules="[(val) => val > -1 || 'Positive number expected']"
        />
      </template>
      <template v-slot:body-wall_leaves>
        <q-input
          v-show="filters.selections.indexOf('wall_leaves_nb') !== -1"
          :disable="filters.selections.indexOf('wall_leaves_nb') === -1"
          v-model.number="filters.wallLeavesNb"
          type="number"
          dense
          style="max-width: 200px"
          class="q-ml-lg"
          :rules="[(val) => val > -1 || 'Positive number expected']"
        />
      </template>
    </q-tree>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  name: 'ExperimentFilters',
});
</script>
<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { computed } from 'vue';
import { useFiltersStore } from 'src/stores/filters';

const { t } = useI18n({ useScope: 'global' });
const filters = useFiltersStore();

const filterNodes = computed(() => [
  {
    label: t('masonry_unit_material'),
    key: 'masonry_unit_material',
    children: masonryUnitMaterial.map((label) => ({
      label: label,
      key: `masonry_unit_material:${label}`,
    })),
  },
  {
    label: t('masonry_unit_type'),
    key: 'masonry_unit_type',
    children: masonryUnitType.map((label) => ({
      label: label,
      key: `masonry_unit_type:${label}`,
    })),
  },
  {
    label: t('storeys_nb'),
    key: 'storeys_nb',
    body: 'storeys',
  },
  {
    label: t('wall_leaves_nb'),
    key: 'wall_leaves_nb',
    body: 'wall_leaves',
  },
  {
    label: t('diaphragm_material'),
    key: 'diaphragm_material',
    children: diaphragmMaterial.map((label) => ({
      label: label,
      key: `diaphragm_material:${label}`,
    })),
  },
  {
    label: t('applied_excitation_directions'),
    key: 'applied_excitation_directions',
    children: appliedExcitationDirections.map((label) => ({
      label: label,
      key: `applied_excitation_directions:${label}`,
    })),
  },
  {
    label: t('retrofitting_application'),
    key: 'retrofitting_application',
    children: retrofittingApplication.map((label) => ({
      label: label,
      key: `retrofitting_application:${label}`,
    })),
  },
]);

const masonryUnitMaterial = [
  'Clay',
  'Calcareous sandstone',
  'Calcium silicate',
  'Granite',
  'Limestone',
  'Tuff stone',
  'Concrete',
  'Adobe',
  'Calcareous tuff stone',
  'Neopolitan tuff stone',
];

const masonryUnitType = [
  'Hollow brick',
  'Solid brick',
  'Dressed stone',
  'Undressed stone',
];

const diaphragmMaterial = [
  'RC',
  'Timber',
  'RC & Timber',
  'Steel & bricks',
  'Hollow tile slab',
];

const retrofittingApplication = [
  'Not present',
  'From beginning',
  'After damage',
];

const appliedExcitationDirections = ['N-S', 'E-W'];

function onFilterTicked() {
  if (filters.selections.indexOf('storeys_nb') === -1) {
    filters.storeysNb = 1;
  }
  if (filters.selections.indexOf('wall_leaves_nb') === -1) {
    filters.wallLeavesNb = 1;
  }
}
</script>
