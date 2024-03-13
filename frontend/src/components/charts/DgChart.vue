<template>
  <div v-if="option.series" :style="`height: ${height + 150}px;`">
    <e-charts
      ref="chart"
      autoresize
      :init-options="initOptions"
      :option="option"
      :update-options="updateOptions"
      class="q-ma-md"
      :loading="loading"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  name: 'DgChart',
});
</script>
<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import ECharts from 'vue-echarts';
import type { EChartsOption } from 'echarts';
import { use } from 'echarts/core';
import { ScatterChart } from 'echarts/charts';
import { SVGRenderer } from 'echarts/renderers';
import { initOptions, updateOptions } from '../charts';
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  DataZoomComponent,
} from 'echarts/components';
import { Experiment, RunResult } from 'src/components/models';
import { useRunResultsStore } from 'src/stores/run_results';

use([
  SVGRenderer,
  ScatterChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  DataZoomComponent,
]);

interface DgChartProps {
  experiment: Experiment;
  direction: string;
  height?: number;
}
const props = withDefaults(defineProps<DgChartProps>(), {
  experiment: undefined,
  direction: 'x',
  height: 300,
});

const { t } = useI18n({ useScope: 'global' });
const runResultsStore = useRunResultsStore();

const runResults = ref<RunResult[]>([]);
const chart = shallowRef(null);
const option = ref<EChartsOption>({});
const loading = ref(false);

watch(
  () => props.experiment,
  () => {
    initChartOptions();
  }
);

onMounted(() => {
  initChartOptions();
});

function initChartOptions() {
  option.value = {};
  if (!props.experiment) {
    return;
  }
  runResultsStore
    .fetchRunResults(props.experiment.id)
    .then((res: RunResult[]) => {
      runResults.value = res.filter(
        (run) => !['Initial', 'Final'].includes(run.run_id)
      );
      buildOptions();
    });
}

function buildOptions() {
  loading.value = true;
  const nominal = `nominal_pga_${props.direction}`;
  const actual = `actual_pga_${props.direction}`;
  const visibleColumns = [nominal, actual, 'dg_reported', 'dg_derived'].filter(
    (col) =>
      runResults.value.filter((run: RunResult) => run[col] !== null).length > 0
  );
  let pgaColumn = visibleColumns.includes(actual) ? actual : nominal;
  const dgColumn = visibleColumns.includes('dg_reported')
    ? 'dg_reported'
    : 'dg_derived';

  if (
    !visibleColumns.includes(pgaColumn) ||
    !visibleColumns.includes(dgColumn)
  ) {
    loading.value = false;
    return;
  }

  const datasetDG = runResults.value
    .filter((result) => result[dgColumn] !== null && result[pgaColumn] !== null)
    .map((result) => {
      return [result[dgColumn], result[pgaColumn]];
    });

  const datasetDG1 = datasetDG.filter((result) => result[0] === 1);
  const datasetDG2 = datasetDG.filter((result) => result[0] === 2);
  const datasetDG3 = datasetDG.filter((result) => result[0] === 3);
  const datasetDG4 = datasetDG.filter((result) => result[0] === 4);
  const datasetDG5 = datasetDG.filter((result) => result[0] === 5);

  const newOption: EChartsOption = {
    // title: {
    //   text: `${t(pgaColumn)} vs. ${t(dgColumn)}`,
    // },
    animation: false,
    height: props.height,
    grid: {
      left: 60,
      top: 10,
      right: 60,
      bottom: 0,
    },
    tooltip: {
      trigger: 'item',
      formatter: (params: unknown) => {
        return `${t(pgaColumn)}: ${params.value[1]} s`;
      },
    },
    xAxis: {
      type: 'value',
      name: t(dgColumn + '_axis'),
      nameLocation: 'middle',
      nameTextStyle: {
        fontWeight: 'bold',
        fontSize: 16,
        padding: [20, 0, 10, 0],
      },
    },
    yAxis: {
      type: 'value',
      name: `${t(pgaColumn + '_axis')} (s)`,
      nameLocation: 'middle',
      nameTextStyle: {
        fontWeight: 'bold',
        fontSize: 16,
        padding: [0, 0, 30, 0],
      },
    },
    series: [
      {
        name: t(dgColumn),
        data: datasetDG1,
        type: 'scatter',
        symbolSize: 15,
        itemStyle: {
          color: 'blue',
          opacity: 0.5,
        },
      },
      {
        name: t(dgColumn),
        data: datasetDG2,
        type: 'scatter',
        symbolSize: 15,
        itemStyle: {
          color: 'green',
          opacity: 0.5,
        },
      },
      {
        name: t(dgColumn),
        data: datasetDG3,
        type: 'scatter',
        symbolSize: 15,
        itemStyle: {
          color: 'yellow',
          opacity: 0.5,
        },
      },
      {
        name: t(dgColumn),
        data: datasetDG4,
        type: 'scatter',
        symbolSize: 15,
        itemStyle: {
          color: 'orange',
          opacity: 0.5,
        },
      },
      {
        name: t(dgColumn),
        data: datasetDG5,
        type: 'scatter',
        symbolSize: 15,
        itemStyle: {
          color: 'red',
          opacity: 0.5,
        },
      },
    ],
  };
  option.value = newOption;
  loading.value = false;
}
</script>
