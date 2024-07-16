<template>
  <div>
    <q-page style="padding-top: 40px">
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
        <template v-slot:top-left> </template>
        <template v-slot:top-right> </template>
        <template v-slot:body-cell-scheme="props">
          <q-td :props="props">
            <q-img
              v-if="props.value"
              :src="`${cdnUrl}${props.value.path}`"
              spinner-color="grey-6"
              width="100px"
            />
          </q-td>
        </template>
        <template v-slot:body-cell-models="props">
          <q-td :props="props">
            <q-img
              v-if="hasModels(props.row)"
              :src="getModelsSchemeUrl(props.row)"
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
                    filters.with3dModel
                      ? getModelsSchemeUrl(props.row)
                      : props.row.scheme
                      ? `${cdnUrl}${props.row.scheme.path}`
                      : '/no-image.png'
                  "
                  :alt="`${props.row.description} [${props.row.reference}]`"
                  spinner-color="grey-6"
                  height="250px"
                >
                  <div
                    v-if="!filters.with3dModel && hasModels(props.row)"
                    class="absolute-top text-right"
                  >
                    <q-icon
                      name="house_siding"
                      class="bg-secondary text-white"
                      size="sm"
                    />
                  </div>
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
                color="accent"
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
                color="grey-7"
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
      <q-page-sticky expand position="top">
        <q-toolbar class="bg-white q-pl-md q-pr-md">
          <span class="text-h6">{{ $t('buildings_title') }}</span>
          <q-btn
            flat
            round
            size="lg"
            icon="help_outline"
            class="on-right text-primary"
          >
            <q-tooltip v-model="showFilterTips" class="bg-grey-7 text-white">
              <div
                class="q-pt-md q-pl-md q-pr-md"
                style="width: 400px; font-size: medium"
              >
                <q-markdown :src="$t('buildings_help')" />
              </div>
            </q-tooltip>
          </q-btn>
          <q-toggle
            v-model="filters.with3dModel"
            :label="$t('show_numerical_models')"
            left-label
            color="secondary"
            keep-color
            icon="house_siding"
            size="70px"
          />
          <q-space />
          <q-btn
            v-if="!filters.with3dModel"
            :label="$t('download_test_files')"
            no-caps
            icon="download"
            color="secondary"
            flat
            class="on-left"
            @click="downloadFiles"
          />
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
        </q-toolbar>
      </q-page-sticky>
    </q-page>
    <q-dialog
      v-model="showExperiment"
      :maximized="$q.screen.lt.md"
      transition-show="slide-up"
      transition-hide="slide-down"
    >
      <q-card :style="$q.screen.lt.md ? '' : 'width: 800px; max-width: 80vw'">
        <q-bar class="bg-white q-pt-lg">
          <div class="q-pl-xs" style="font-size: larger">
            {{ experiment.description }}
            <span v-if="experiment.experiment_id">
              - {{ experiment.experiment_id }}
            </span>
          </div>
          <q-space />
          <q-btn dense flat size="xl" icon="close" v-close-popup />
        </q-bar>
        <q-card-section>
          <experiment-summary
            :experiment="experiment"
            @select="onReferenceExperimentSelection"
          ></experiment-summary>
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>

<script lang="ts">
export default defineComponent({
  name: 'ExperimentsTable',
});
</script>
<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { Settings } from 'src/stores/settings';
import { ref, onMounted } from 'vue';
import { api, baseUrl, cdnUrl } from 'src/boot/axios';
import { FileNode, Experiment, Reference } from 'src/components/models';
import ExperimentSummary from 'src/components/ExperimentSummary.vue';
import {
  makePaginationRequestHandler,
  QueryParams,
} from 'src/utils/pagination';
import { useFiltersStore } from 'src/stores/filters';

const { t } = useI18n({ useScope: 'global' });
const filters = useFiltersStore();
const settingsStore = useSettingsStore();

const view = ref(
  settingsStore.settings && settingsStore.settings.experiments_view
    ? settingsStore.settings.experiments_view
    : 'grid'
);
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
const showFilterTips = ref(false);

const columns = [
  {
    name: 'building_id',
    required: true,
    label: '#',
    align: 'left',
    field: 'building_id',
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
    name: 'models',
    required: true,
    label: t('model'),
    align: 'left',
    field: 'models',
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
    range:
      count > 0 ? JSON.stringify([startRow, startRow + count - 1]) : undefined,
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

watch(
  [
    () => filters.selections,
    () => filters.referenceSelections,
    () => filters.with3dModel,
  ],
  () => tableRef.value?.requestServerInteraction()
);

function onExperiment(selected: Experiment) {
  experiment.value = selected;
  showExperiment.value = true;
}

onMounted(() => {
  tableRef.value?.requestServerInteraction();
  if (settingsStore.settings?.intro_shown) {
    triggerFilterTips();
  }
});

watch(
  () => settingsStore.settings,
  () => {
    if (settingsStore.settings?.intro_shown) {
      triggerFilterTips();
    }
  }
);

function toggleView(newView: string) {
  view.value = newView;
  settingsStore.saveSettings({ experiments_view: view.value } as Settings);
}

function hasModels(row: Experiment) {
  return row.model_files;
}

function getModelsSchemeUrl(row: Experiment) {
  if (row.model_files) {
    const schemeInfo = (row.model_files as FileNode).children?.find(
      (child: FileNode) => child.name.startsWith('scheme')
    );
    return schemeInfo
      ? `${cdnUrl}${
          schemeInfo.alt_path ? schemeInfo.alt_path : schemeInfo.path
        }`
      : '';
  }
  return '';
}

function downloadFiles() {
  const dbFilter = filters.dbFilters;
  const query: QueryParams = {
    filter: JSON.stringify(
      filter.value ? { description: filter, ...dbFilter } : dbFilter
    ),
  };
  const queryStr =
    query.filter && query.filter !== '{}'
      ? `?filter=${encodeURIComponent(query.filter)}`
      : '';
  window.open(`${baseUrl}/experiments-download/test-files${queryStr}`);
}

function onReferenceExperimentSelection(selected: Experiment) {
  experiment.value = selected;
}

function triggerFilterTips() {
  if (!showFilterTips.value && !settingsStore.settings?.filter_tips) {
    showFilterTips.value = true;
    setTimeout(() => {
      showFilterTips.value = false;
      settingsStore.saveSettings({ filter_tips: true } as Settings);
    }, 5000);
  }
}
</script>
