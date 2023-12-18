<template>
  <div>
    <q-table
      flat
      grid
      ref="tableRef"
      :rows="rows"
      :columns="columns"
      row-key="id"
      v-model:pagination="pagination"
      :loading="loading"
      :filter="filter"
      binary-state-sort
      @request="onRequest"
    >
      <template v-slot:top-right>
        <q-input
          borderless
          dense
          clearable
          debounce="300"
          v-model="filter"
          :placeholder="$t('search')"
        >
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
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
            <q-card-section class="q-pa-none">
              <q-img
                :src="`${baseUrl}/files/${props.row.scheme.path}`"
                spinner-color="grey-6"
                height="250px"
              >
                <div class="absolute-bottom text-subtitle1 text-center">
                  {{ props.row.description }}
                </div>
              </q-img>
            </q-card-section>
          </q-card>
        </div>
      </template>
    </q-table>
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
import {
  makePaginationRequestHandler,
  QueryParams,
} from 'src/utils/pagination';
import { useFiltersStore } from 'src/stores/filters';

const { t } = useI18n({ useScope: 'global' });
const filters = useFiltersStore();

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

const columns = [
  {
    name: 'id',
    required: true,
    label: t('id'),
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
    field: 'reference_id',
    sortable: true,
  },
];

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

onMounted(() => {
  tableRef.value?.requestServerInteraction();
});
</script>