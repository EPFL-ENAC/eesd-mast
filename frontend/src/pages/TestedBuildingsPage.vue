<template>
  <q-page>
    <h5 class="q-pa-md q-mt-sm q-mb-sm">{{ $t('tested_buildings') }}</h5>
    <q-separator />
    <div>
      <q-tabs
        v-model="tab"
        dense
        class="text-grey"
        active-color="primary"
        indicator-color="primary"
        align="justify"
        narrow-indicator
      >
        <q-tab name="references" :label="$t('references')" />
        <q-tab name="experiments" :label="$t('experiments')" />
      </q-tabs>

      <q-separator />

      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="references">
          <references-table></references-table>
        </q-tab-panel>

        <q-tab-panel name="experiments">
          <experiments-table></experiments-table>
        </q-tab-panel>
      </q-tab-panels>
    </div>
    <div class="row">
      <div class="col-6"></div>
      <div class="col-6"></div>
    </div>
    <div></div>
    <div class="q-pa-md"></div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
const tab = ref('references');
import ReferencesTable from 'components/ReferencesTable.vue';
import ExperimentsTable from 'components/ExperimentsTable.vue';
</script>
