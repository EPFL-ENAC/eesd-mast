<template>
  <q-page>
    <div>
      <app-header url="/Website_Background_Title_Option1_blue.webp" />
      <metrics-banner />
      <experiment-aggregations />
    </div>
  </q-page>
</template>

<script setup lang="ts">
import AppHeader from 'src/components/AppHeader.vue';
import MetricsBanner from 'src/components/MetricsBanner.vue';
import ExperimentAggregations from 'src/components/ExperimentAggregations.vue';
</script>
