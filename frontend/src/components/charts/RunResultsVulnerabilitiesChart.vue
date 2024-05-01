<template>
  <vue-plotly :data="chartData" :layout="layout" :config="config" />
</template>

<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  components: { VuePlotly },
  name: 'RunResultsVulnerabilitiesChart',
});
</script>
<script setup lang="ts">
import { RunResultVulnerability } from '../models';
import { getDgColor } from 'src/utils/colors';
import VuePlotly from './VuePlotly.vue';

const { t } = useI18n({ useScope: 'global' });
const analysis = useAnalysisStore();

const layout = {
  //violingap: 0,
  violingroupgap: 0,
  violinmode: 'overlay',
  yaxis: {
    title: {
      text: t('dg_axis'),
    },
    tickvals: [1, 2, 3, 4, 5],
    ticktext: ['1', '2', '3', '4', '5'],
  },
  showlegend: false,
  xaxis: {
    title: {
      text: t('pga_axis'),
    },
    range: [0, 1.7],
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

interface ScatterTrace {
  x: number[];
  y: number[];
  mode: 'markers';
  marker: { color: string };
  name: string;
}

interface ViolinTrace {
  x: number[];
  type: 'violin';
  name: string;
  side: 'negative' | 'positive';
  marker: { color: string };
  jitter: number;
}

const chartData = computed(() => {
  const dgGroups: { [Key: string]: number[] } = {
    '1': [],
    '2': [],
    '3': [],
    '4': [],
    '5': [],
  };

  analysis.runResultsVulnerabilities.forEach((line: RunResultVulnerability) => {
    dgGroups[line.dg] = line.pgas;
  });

  const scatterTraces: ScatterTrace[] = Object.keys(dgGroups).map((key) => {
    return {
      y: dgGroups[key].map(() => parseInt(key)),
      x: dgGroups[key],
      mode: 'markers',
      marker: {
        color: getDgColor(key),
      },
      name: `DG${key}`,
    };
  });

  const violinTraces: ViolinTrace[] = Object.keys(dgGroups).map((key) => {
    return {
      x: dgGroups[key],
      type: 'violin',
      name: key,
      side: 'positive',
      marker: {
        color: getDgColor(key),
      },
      jitter: 0.05,
    };
  });
  return [...violinTraces, ...scatterTraces];
});
</script>
