<template>
  <div>
    <q-table
      flat
      ref="tableRef"
      :rows="rows"
      :columns="columns"
      row-key="id"
      :rows-per-page-options="[10, 25, 50, 0]"
      selection="multiple"
      v-model:selected="filters.references"
      v-model:pagination="pagination"
      :loading="loading"
      :filter="filter"
      binary-state-sort
      @request="onRequest"
    >
      <template v-slot:top-left>
        <q-btn
          v-if="filters.references.length"
          flat
          no-caps
          :label="$t('clear_all_selections')"
          color="grey-8"
          @click="filters.references = []"
        />
      </template>
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
      <template v-slot:body-cell-corresponding_author_name="props">
        <q-td :props="props">
          <a :href="`mailto:${props.row.corresponding_author_email}`">{{
            props.value
          }}</a>
        </q-td>
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
              v-if="props.row.link_to_experimental_paper"
              icon="article"
              color="primary"
              text-color="white"
              size="sm"
              class="q-ml-none"
            >
              <a
                :href="props.row.link_to_experimental_paper"
                target="_blank"
                class="ellipsis"
                style="text-decoration: none; color: white"
              >
                {{ $t('paper') }}
              </a>
            </q-chip>
            <q-chip
              v-if="props.row.link_to_request_data"
              icon="grid_on"
              color="secondary"
              text-color="white"
              size="sm"
            >
              <a
                :href="props.row.link_to_request_data"
                target="_blank"
                class="ellipsis"
                style="text-decoration: none; color: white"
              >
                {{ $t('data') }}
              </a>
            </q-chip>
          </div>
        </q-td>
      </template>
    </q-table>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  name: 'ReferencesTable',
});
</script>
<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { ref, onMounted } from 'vue';
import { api } from 'src/boot/axios';
import {
  makePaginationRequestHandler,
  QueryParams,
} from 'src/utils/pagination';
import { useFiltersStore } from 'src/stores/filters';

const filters = useFiltersStore();
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
  /*{
    name: 'id',
    required: true,
    label: t('id'),
    align: 'left',
    field: 'id',
    sortable: true,
  },*/
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
    name: 'corresponding_author_name',
    required: true,
    label: t('corresponding_author'),
    align: 'left',
    field: 'corresponding_author_name',
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
  const query: QueryParams = {
    filter: filter ? JSON.stringify({ full_reference: filter }) : undefined,
    sort: sortBy
      ? JSON.stringify([sortBy, descending ? 'DESC' : 'ASC'])
      : undefined,
    range: JSON.stringify([startRow, startRow + count - 1]),
  };
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
