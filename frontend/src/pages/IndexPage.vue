<template>
  <q-page>
    <div>
      <app-header url="/Website_Background_Title_Option1_blue.webp" />
      <metrics-banner />
      <experiment-aggregations />
      <div class="q-ml-xl q-mr-xl q-mb-xl">
        <div class="text-h6 q-mb-md">{{ $t('how_to_cite') }}</div>
        <q-markdown :src="CiteMd" class="epfl-md" />
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import AppHeader from 'src/components/AppHeader.vue';
import MetricsBanner from 'src/components/MetricsBanner.vue';
import ExperimentAggregations from 'src/components/ExperimentAggregations.vue';
import CiteMd from 'src/assets/cite.md';
</script>
