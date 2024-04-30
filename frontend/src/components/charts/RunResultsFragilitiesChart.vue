<template>
  <vue-plotly :data="chartData" :layout="layout" :config="config" />
</template>

<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  components: { VuePlotly },
  name: 'RunResultsFragilitiesChart',
});
</script>
<script setup lang="ts">
import { RunResultFragility } from '../models';
import { getDgColor } from 'src/utils/colors';
import VuePlotly from './VuePlotly.vue';

const { t } = useI18n({ useScope: 'global' });
const analysis = useAnalysisStore();

const layout = {
  xaxis: {
    title: {
      text: t('pga_axis'),
    },
  },
  yaxis: {
    title: {
      text: t('dg_pga_axis'),
    },
  },
  margin: {
    l: 50, // Left margin
    r: 50, // Right margin
    b: 50, // Bottom margin
    t: 50, // Top margin
  },
};

const config = {
  displayModeBar: false,
  responsive: true,
};

interface LineTrace {
  x: number[];
  y: number[];
  mode: 'lines' | 'markers';
  marker: { color: string };
  line: { color: string };
}

const chartData = computed(() => {
  const dgGroups: { [Key: string]: RunResultFragility } = {
    '1': {} as RunResultFragility,
    '2': {} as RunResultFragility,
    '3': {} as RunResultFragility,
    '4': {} as RunResultFragility,
    '5': {} as RunResultFragility,
  };

  analysis.runResultsFragilities.forEach((line: RunResultFragility) => {
    dgGroups[line.dg] = line;
  });

  const probTraces: LineTrace[] = Object.keys(dgGroups).map((key) => {
    return {
      y: dgGroups[key].prob,
      x: dgGroups[key].thresh,
      mode: 'markers',
      marker: {
        color: getDgColor(key),
        size: 3,
      },
      line: {
        color: getDgColor(key),
      },
      name: `DG${key}`,
      showlegend: false,
    };
  });

  const fittedTraces: LineTrace[] = Object.keys(dgGroups).map((key) => {
    return {
      y: dgGroups[key].y,
      x: dgGroups[key].x,
      mode: 'lines',
      marker: {
        color: getDgColor(key),
      },
      line: {
        color: getDgColor(key),
        width: 2,
      },
      name: `DG${key}`,
    };
  });

  return [...probTraces, ...fittedTraces];
});
</script>
