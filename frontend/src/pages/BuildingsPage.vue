<template>
  <q-page>
    <h5 class="q-pa-md q-mt-sm q-mb-sm">{{ $t('tested_buildings') }}</h5>
    <q-separator />
    <experiments-table></experiments-table>
  </q-page>
</template>

<script setup lang="ts">
import ExperimentsTable from 'components/ExperimentsTable.vue';
</script>
