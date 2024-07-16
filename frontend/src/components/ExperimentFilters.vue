<template>
  <div>
    <q-btn
      dense
      flat
      no-caps
      color="secondary"
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
      color="secondary"
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
      class="col-12 col-sm-6 q-ml-sm"
      :nodes="filterNodes"
      node-key="key"
      no-connectors
      tick-strategy="leaf"
      control-color="primary"
      v-model:ticked="filters.selections"
    >
    </q-tree>
    <div class="q-mb-md">
      <div class="text-center text-bold text-grey-7 q-mt-md">
        {{ $t('vulnerability_analysis') }}
      </div>
      <run-results-fragilities-chart
        :data="filters.runResultsFragilities"
        :compact="true"
        :show-empirical="false"
        class="q-mb-sm"
      />
      <div class="row justify-center">
        <q-btn
          dense
          flat
          no-caps
          icon="zoom_in"
          class="text-caption text-primary"
          :label="$t('view_details')"
          @click="onShowFragilities"
        />
      </div>
    </div>

    <simple-dialog v-model="showFragilities" :width="800">
      <div>
        <div class="text-center text-h6">
          {{ $t('vulnerability_analysis') }}
        </div>
        <run-results-fragilities-chart :data="filters.runResultsFragilities" />
        <div class="q-ma-md q-pl-lg q-pr-md text-grey-9">
          <q-markdown :src="FragilitiesMd" no-line-numbers />
        </div>
      </div>
    </simple-dialog>
  </div>
</template>

<script lang="ts">
export default defineComponent({
  name: 'ExperimentFilters',
});
</script>
<script setup lang="ts">
import { api } from 'src/boot/axios';
import { Reference } from './models';
import { testScaleLabel } from 'src/utils/numbers';
import {
  DIAPHRAGM_MATERIAL,
  MASONRY_UNIT_MATERIAL,
  MASONRY_UNIT_TYPE,
  RETROFITTING_APPLICATION,
  SIMULTANEOUS_EXCITATIONS_NB,
  STOREYS_NB,
  TEST_SCALE,
  WALL_LEAVES_NB,
} from 'src/utils/criteria';
import RunResultsFragilitiesChart from 'src/components/charts/RunResultsFragilitiesChart.vue';
import SimpleDialog from 'src/components/SimpleDialog.vue';
import FragilitiesMd from 'src/assets/fragilities.md';

const { t } = useI18n({ useScope: 'global' });
const filters = useFiltersStore();
const references = ref([]);
const showFragilities = ref(false);

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
    children: MASONRY_UNIT_MATERIAL.map((value) => ({
      label: value,
      key: `masonry_unit_material:${value}`,
    })),
  },
  {
    label: t('masonry_unit_type'),
    key: 'masonry_unit_type',
    children: MASONRY_UNIT_TYPE.map((value) => ({
      label: value,
      key: `masonry_unit_type:${value}`,
    })),
  },
  {
    label: t('storeys_nb'),
    key: 'storeys_nb',
    children: STOREYS_NB.map((value) => ({
      label: value,
      key: `storeys_nb:${value}`,
    })),
  },
  {
    label: t('wall_leaves_nb'),
    key: 'wall_leaves_nb',
    children: WALL_LEAVES_NB.map((value) => ({
      label: value,
      key: `wall_leaves_nb:${value}`,
    })),
  },
  {
    label: t('test_scale'),
    key: 'test_scale',
    children: TEST_SCALE.map((value) => ({
      label: testScaleLabel(value),
      key: `test_scale:${value}`,
    })),
  },
  {
    label: t('diaphragm_material'),
    key: 'diaphragm_material',
    children: DIAPHRAGM_MATERIAL.map((value) => ({
      label: value === null ? 'N/A' : value,
      key: `diaphragm_material:${value}`,
    })),
  },
  {
    label: t('simultaneous_excitations_nb'),
    key: 'simultaneous_excitations_nb',
    children: SIMULTANEOUS_EXCITATIONS_NB.map((value) => ({
      label: value,
      key: `simultaneous_excitations_nb:${value}`,
    })),
  },
  {
    label: t('retrofitting_application'),
    key: 'retrofitting_application',
    children: RETROFITTING_APPLICATION.map((value) => ({
      label: value,
      key: `retrofitting_application:${value}`,
    })),
  },
]);

onMounted(() => {
  filters.loadRunResultsFragilities();
});

watch(
  () => filters.dbFilters,
  () => {
    filters.loadRunResultsFragilities();
  }
);

function onShowFragilities() {
  showFragilities.value = true;
}
</script>
