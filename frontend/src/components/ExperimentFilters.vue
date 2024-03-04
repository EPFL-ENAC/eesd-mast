<template>
  <div>
    <q-btn
      dense
      flat
      no-caps
      color="primary"
      :label="$t('reset_filters')"
      class="q-ml-md q-mb-md"
      @click="filters.resetFilters()"
    ></q-btn>
    <q-select
      filled
      v-model="filters.referenceSelections"
      use-chips
      use-input
      multiple
      clearable
      dense
      input-debounce="300"
      :label="$t('references')"
      :hint="$t('select_references_hint')"
      :options="references"
      @filter="filterFn"
      style="width: 250px"
      class="q-ml-md q-mb-md"
    >
      <template v-slot:no-option>
        <q-item>
          <q-item-section class="text-grey">{{
            $t('no_results')
          }}</q-item-section>
        </q-item>
      </template>
    </q-select>
    <q-tree
      class="col-12 col-sm-6 q-ml-md"
      :nodes="filterNodes"
      node-key="key"
      no-connectors
      tick-strategy="leaf"
      v-model:ticked="filters.selections"
    >
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
import { api } from 'src/boot/axios';
import { Reference } from './models';

const { t } = useI18n({ useScope: 'global' });
const filters = useFiltersStore();
const references = ref([]);
function filterFn(val, update, abort) {
  const query = {
    filter: val ? JSON.stringify({ full_reference: val }) : undefined,
    sort: JSON.stringify(['reference', 'ASC']),
  };
  api({
    method: 'get',
    url: '/references',
    params: query,
  })
    .then((response) => {
      references.value = response.data.map((item: Reference) => ({
        label: item.reference,
        value: item,
      }));
      update();
    })
    .catch((error) => {
      console.error(error);
      abort();
    });
}

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
    children: storeysNb.map((label) => ({
      label: label,
      key: `storeys_nb:${label}`,
    })),
  },
  {
    label: t('wall_leaves_nb'),
    key: 'wall_leaves_nb',
    children: wallLeavesNb.map((label) => ({
      label: label,
      key: `wall_leaves_nb:${label}`,
    })),
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
    label: t('simultaneous_excitations_nb'),
    key: 'simultaneous_excitations_nb',
    children: simultaneousExcitationsNb.map((label) => ({
      label: label,
      key: `simultaneous_excitations_nb:${label}`,
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

const storeysNb = ['1', '2', '3', '4', '5'];

const wallLeavesNb = ['1', '2', '3'];

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

const simultaneousExcitationsNb = ['1', '2', '3'];
</script>
