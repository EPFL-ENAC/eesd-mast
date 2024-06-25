<template>
  <vue-plotly :data="chartData" :layout="layout" :config="config" />
</template>

<script lang="ts">
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

interface Props {
  data: RunResultFragility[];
  showLegend: boolean;
  showEmpirical: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  showLegend: true,
  showEmpirical: true,
});

const layout = {
  xaxis: {
    title: {
      text: t('pga_axis'),
    },
    range: [0, 1],
  },
  yaxis: {
    title: {
      text: t('dg_pga_axis'),
    },
  },
  margin: {
    l: 50, // Left margin
    r: 10, // Right margin
    b: 50, // Bottom margin
    t: 50, // Top margin
  },
  showLegend: props.showLegend,
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

  props.data.forEach((line: RunResultFragility) => {
    dgGroups[line.dg] = line;
  });

  const probTraces: LineTrace[] = props.showEmpirical
    ? Object.keys(dgGroups)
        .filter((key) => dgGroups[key].prob && dgGroups[key].thresh)
        .map((key) => {
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
            name: `DG${key} (empirical)`,
            showlegend: props.showLegend,
            legendgroup: 'empirical',
          };
        })
    : [];

  const fittedTraces: LineTrace[] = Object.keys(dgGroups)
    .filter((key) => dgGroups[key].x && dgGroups[key].y)
    .map((key) => {
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
        name: `DG${key} (fitted)`,
        showlegend: props.showLegend,
        legendgroup: 'fitted',
      };
    });

  return [...fittedTraces, ...probTraces];
});
</script>
