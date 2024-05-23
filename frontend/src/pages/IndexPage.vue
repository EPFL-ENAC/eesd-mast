<template>
  <q-page>
    <div class="row">
      <div :class="$q.screen.lt.xl ? 'col-0' : 'col-1'"></div>
      <div :class="$q.screen.lt.xl ? 'col-12' : 'col-10'">
        <metrics-banner />
        <experiment-aggregations />
      </div>
      <div :class="$q.screen.lt.xl ? 'col-0' : 'col-1'"></div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import MetricsBanner from 'src/components/MetricsBanner.vue';
import ExperimentAggregations from 'src/components/ExperimentAggregations.vue';
</script>
