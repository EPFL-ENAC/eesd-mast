<template>
  <div>
    <q-table
      flat
      :grid="view === 'grid'"
      ref="tableRef"
      :rows="rows"
      :columns="columns"
      row-key="id"
      :rows-per-page-options="[12, 24, 48, 0]"
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
              @click="toggleView('grid')"
            />
            <q-btn
              flat
              icon="view_list"
              :class="view === 'table' ? 'bg-grey-4' : ''"
              @click="toggleView('table')"
            />
          </q-btn-group>
        </div>
      </template>
      <template v-slot:body-cell-scheme="props">
        <q-td :props="props">
          <q-img
            v-if="props.value"
            :src="`${baseUrl}/files/${props.value.path}`"
            spinner-color="grey-6"
            width="100px"
          />
        </q-td>
      </template>
      <template v-slot:item="props">
        <div class="q-pa-xs col-xs-12 col-sm-6 col-md-3 col-lg-2">
          <q-card flat bordered class="q-ma-md">
            <q-card-section
              class="q-pa-none"
              style="cursor: pointer"
              @click="onExperiment(props.row)"
            >
              <q-img
                :src="
                  props.row.scheme
                    ? `${baseUrl}/files/${props.row.scheme.path}`
                    : '/no-image.png'
                "
                :alt="`${props.row.description} [${props.row.reference}]`"
                spinner-color="grey-6"
                height="250px"
              >
                <div class="absolute-bottom text-center">
                  <div class="text-subtitle2">
                    {{ props.row.reference.reference }}
                  </div>
                  <div class="text-caption">
                    {{ props.row.description }}
                    <span v-if="props.row.experiment_id">
                      - {{ props.row.experiment_id }}
                    </span>
                  </div>
                </div>
                <template v-slot:error>
                  <div class="absolute-bottom text-center">
                    <div class="text-subtitle2">
                      {{ props.row.reference.reference }}
                    </div>
                    <div class="text-caption">
                      {{ props.row.description }}
                      <span v-if="props.row.experiment_id">
                        - {{ props.row.experiment_id }}
                      </span>
                    </div>
                  </div>
                </template>
              </q-img>
            </q-card-section>
          </q-card>
        </div>
      </template>

      <template v-slot:body-cell-full_reference="props">
        <q-td :props="props">
          <div
            style="overflow-wrap: break-word; width: 500px"
            class="ellipsis"
            :title="props.value"
          >
            {{ props.value }}
          </div>
          <div>
            <q-chip
              v-if="props.row.reference.link_to_experimental_paper"
              icon="article"
              color="primary"
              text-color="white"
              size="sm"
              class="q-ml-none"
            >
              <a
                :href="props.row.reference.link_to_experimental_paper"
                target="_blank"
                style="text-decoration: none; color: white"
              >
                {{ $t('paper') }}
              </a>
            </q-chip>
            <q-chip
              v-if="props.row.reference.link_to_request_data"
              icon="grid_on"
              color="secondary"
              text-color="white"
              size="sm"
            >
              <a
                :href="props.row.reference.link_to_request_data"
                target="_blank"
                style="text-decoration: none; color: white"
              >
                {{ $t('data') }}
              </a>
            </q-chip>
          </div>
        </q-td>
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
          <experiment-summary :experiment="experiment"></experiment-summary>
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
import { getSettings, saveSettings } from 'src/utils/settings';
import { ref, onMounted } from 'vue';
import { api, baseUrl } from 'src/boot/axios';
import { Experiment, Reference } from 'src/components/models';
import ExperimentSummary from 'src/components/ExperimentSummary.vue';
import {
  makePaginationRequestHandler,
  QueryParams,
} from 'src/utils/pagination';
import { useFiltersStore } from 'src/stores/filters';

const { t } = useI18n({ useScope: 'global' });
const filters = useFiltersStore();
const view = ref(getSettings().experiments_view);
const tableRef = ref();
const rows = ref([]);
const filter = ref('');
const loading = ref(false);
const pagination = ref({
  sortBy: 'id',
  descending: false,
  page: 1,
  rowsPerPage: 24,
  rowsNumber: 24,
});
const showExperiment = ref(false);
const experiment = ref<Experiment>();

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
    sortable: false,
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
    name: 'publication_year',
    required: true,
    label: t('year'),
    align: 'left',
    field: 'publication_year',
    sortable: true,
  },
  {
    name: 'reference',
    required: true,
    label: t('reference'),
    align: 'left',
    field: 'reference',
    format: (val: Reference) => val.reference,
    sortable: false,
  },
  {
    name: 'full_reference',
    required: true,
    label: t('full_reference'),
    align: 'left',
    field: 'reference',
    format: (val: Reference) => val.full_reference,
    sortable: false,
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

function toggleView(newView: string) {
  view.value = newView;
  const settings = getSettings();
  settings.experiments_view = view.value;
  saveSettings(settings);
}
</script>
