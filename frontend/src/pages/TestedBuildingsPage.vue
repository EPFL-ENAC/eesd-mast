<template>
  <q-page>
    <h5 class="q-pa-md q-mt-sm q-mb-sm">{{ $t('tested_buildings') }}</h5>
    <q-separator />
    <div class="row">
      <div class="col-12">
        <q-table
          flat
          ref="tableRef"
          :title="$t('references')"
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
              debounce="300"
              v-model="filter"
              :placeholder="$t('search')"
            >
              <template v-slot:append>
                <q-icon name="search" />
              </template>
            </q-input>
          </template>
        </q-table>
      </div>
      <div class="col-9"></div>
    </div>
    <div></div>
    <div class="q-pa-md"></div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { api } from 'src/boot/axios';
import { makePaginationRequestHandler } from 'src/utils/pagination';
const { t } = useI18n({ useScope: 'global' });

const tableRef = ref();
const rows = ref([]);
const filter = ref('');
const loading = ref(false);
const pagination = ref({
  sortBy: 'id',
  descending: false,
  page: 1,
  rowsPerPage: 10,
  rowsNumber: 10,
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
    name: 'reference',
    required: true,
    label: t('reference'),
    align: 'left',
    field: 'reference',
    sortable: true,
  },
  {
    name: 'publication_year',
    required: true,
    label: t('publication_year'),
    align: 'left',
    field: 'publication_year',
    sortable: true,
  },
  {
    name: 'corresponding_author',
    required: true,
    label: t('corresponding_author'),
    align: 'left',
    field: 'corresponding_author_name',
    format: (val, row) => {
      return `${row.corresponding_author_name} (${row.corresponding_author_email})`;
    },
    sortable: true,
  },
  {
    name: 'full_reference',
    required: true,
    label: t('full_reference'),
    align: 'left',
    field: 'full_reference',
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
  const query = {
    range: JSON.stringify([startRow, startRow + count - 1]),
  };
  if (filter) {
    query.filter = JSON.stringify({
      reference: filter,
    });
  }
  if (sortBy) {
    query.sort = JSON.stringify([sortBy, descending ? 'DESC' : 'ASC']);
  }
  return api({
    method: 'get',
    url: '/references',
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

onMounted(() => {
  tableRef.value?.requestServerInteraction();
});
</script>
