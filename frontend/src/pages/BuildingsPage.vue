<template>
  <q-page>
    <h6 class="q-pa-md q-mt-sm q-mb-sm">{{ $t('buildings') }}</h6>
    <q-separator />
    <experiments-table></experiments-table>
  </q-page>
</template>

<script setup lang="ts">
import ExperimentsTable from 'components/ExperimentsTable.vue';
</script>
