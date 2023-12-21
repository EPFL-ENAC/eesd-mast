<template>
  <div>
    <q-table
      flat
      :grid="view === 'grid'"
      ref="tableRef"
      :rows="rows"
      :columns="columns"
      row-key="id"
      :rows-per-page-options="[12, 25, 50, 0]"
      v-model:pagination="pagination"
      :loading="loading"
      :filter="filter"
      binary-state-sort
      @request="onRequest"
      @row-click="onRowClick"
    >
      <template v-slot:top-left>
        <q-chip
          removable
          v-for="sel in filters.references"
          :key="sel.id"
          @remove="onRemoveReferenceFilter(sel)"
        >
          {{ sel.reference }}
        </q-chip>
      </template>
      <template v-slot:top-right>
        <q-input
          dense
          clearable
          debounce="300"
          v-model="filter"
          :placeholder="$t('search')"
          class="on-left"
        >
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
        <div>
          <q-btn-group flat :class="$q.screen.lt.sm ? 'q-mt-md' : ''">
            <q-btn
              flat
              icon="grid_view"
              :class="view === 'grid' ? 'bg-grey-4' : ''"
              @click="view = 'grid'"
            />
            <q-btn
              flat
              icon="table_view"
              :class="view === 'table' ? 'bg-grey-4' : ''"
              @click="view = 'table'"
            />
          </q-btn-group>
        </div>
      </template>
      <template v-slot:body-cell-scheme="props">
        <q-td :props="props">
          <q-img
            :src="`${baseUrl}/files/${props.value.path}`"
            spinner-color="grey-6"
            width="100px"
          />
        </q-td>
      </template>
      <template v-slot:item="props">
        <div class="q-pa-xs col-xs-12 col-sm-6 col-md-3">
          <q-card flat bordered class="q-ma-md">
            <q-card-section
              class="q-pa-none"
              style="cursor: pointer"
              @click="onExperiment(props.row)"
            >
              <q-img
                :src="`${baseUrl}/files/${props.row.scheme.path}`"
                :alt="`${props.row.description} [${props.row.reference}]`"
                spinner-color="grey-6"
                height="250px"
              >
                <div class="absolute-bottom text-subtitle1 text-center">
                  <div>
                    {{ props.row.description }}
                    <span v-if="props.row.experiment_id">
                      - {{ props.row.experiment_id }}
                    </span>
                  </div>
                  <div>{{ props.row.reference }}</div>
                </div>
              </q-img>
            </q-card-section>
          </q-card>
        </div>
      </template>
    </q-table>

    <q-dialog
      v-model="showExperiment"
      :maximized="$q.screen.lt.md"
      transition-show="slide-up"
      transition-hide="slide-down"
    >
      <q-card :style="$q.screen.lt.md ? '' : 'width: 1000px; max-width: 90vw'">
        <q-bar class="bg-white q-pt-lg">
          <q-space />
          <q-btn dense flat size="xl" icon="close" v-close-popup />
        </q-bar>
        <q-card-section>
          <experiment-view :experiment="experiment"></experiment-view>
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  name: 'ExperimentsTable',
});
</script>
<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { ref, onMounted } from 'vue';
import { api, baseUrl } from 'src/boot/axios';
import { Experiment, Reference } from 'src/components/models';
import ExperimentView from 'src/components/ExperimentView.vue';
import {
  makePaginationRequestHandler,
  QueryParams,
} from 'src/utils/pagination';
import { useFiltersStore } from 'src/stores/filters';

const { t } = useI18n({ useScope: 'global' });
const filters = useFiltersStore();

const view = ref('grid');
const tableRef = ref();
const rows = ref([]);
const filter = ref('');
const loading = ref(false);
const pagination = ref({
  sortBy: 'id',
  descending: false,
  page: 1,
  rowsPerPage: 12,
  rowsNumber: 12,
});
const showExperiment = ref(false);
const experiment = ref({});

const columns = [
  {
    name: 'id',
    required: true,
    label: '#',
    align: 'left',
    field: 'id',
    sortable: true,
  },
  {
    name: 'scheme',
    required: true,
    label: t('scheme'),
    align: 'left',
    field: 'scheme',
    sortable: true,
  },
  {
    name: 'experiment_id',
    required: true,
    label: t('experiment_id'),
    align: 'left',
    field: 'experiment_id',
    sortable: true,
  },
  {
    name: 'description',
    required: true,
    label: t('description'),
    align: 'left',
    field: 'description',
    sortable: true,
  },
  {
    name: 'reference',
    required: true,
    label: t('reference'),
    align: 'left',
    field: 'reference',
    sortable: true,
  },
];

const onRowClick = (evt: unknown, row: Experiment) => {
  experiment.value = row;
  showExperiment.value = true;
};

const onRequest = makePaginationRequestHandler(fetchFromServer, pagination);

function fetchFromServer(
  startRow: number,
  count: number,
  filter: string,
  sortBy: string,
  descending: boolean
) {
  loading.value = true;
  const dbFilter = filters.dbFilters;
  const query: QueryParams = {
    filter: JSON.stringify(
      filter ? { description: filter, ...dbFilter } : dbFilter
    ),
    sort: sortBy
      ? JSON.stringify([sortBy, descending ? 'DESC' : 'ASC'])
      : undefined,
    range: JSON.stringify([startRow, startRow + count - 1]),
  };
  return api({
    method: 'get',
    url: '/experiments',
    params: query,
  }).then((result) => {
    const total = parseInt(
      result.headers['content-range']?.split('/')[1] ?? '0'
    );
    rows.value = result.data;
    loading.value = false;
    return {
      data: result.data,
      total,
    };
  });
}

filters.$subscribe(() => {
  tableRef.value?.requestServerInteraction();
});

function onExperiment(selected: Experiment) {
  experiment.value = selected;
  showExperiment.value = true;
}

function onRemoveReferenceFilter(reference: Reference) {
  filters.references = filters.references.filter((r) => r.id !== reference.id);
}

onMounted(() => {
  tableRef.value?.requestServerInteraction();
});
</script>
