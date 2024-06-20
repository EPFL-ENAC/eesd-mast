<template>
  <div>
    <div v-if="option.series" :style="`height: ${height + 80}px;`">
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
    <div v-if="showIncNote" class="text-center text-caption text-grey-6">
      {{ $t('increasing_pga_note') }}
    </div>
  </div>
</template>

<script lang="ts">
export default defineComponent({
  name: 'PgaChart',
});
</script>
<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import ECharts from 'vue-echarts';
import type { EChartsOption } from 'echarts';
import { use } from 'echarts/core';
import { LineChart } from 'echarts/charts';
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
  LineChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  DataZoomComponent,
]);

interface PgaChartProps {
  experiment: Experiment;
  direction: string;
  height?: number;
}
const props = withDefaults(defineProps<PgaChartProps>(), {
  experiment: undefined,
  direction: 'x',
  height: 300,
});
const emit = defineEmits<{
  (e: 'loaded', value: boolean): void;
}>();

const { t } = useI18n({ useScope: 'global' });
const runResultsStore = useRunResultsStore();

const chart = shallowRef(null);
const option = ref<EChartsOption>({});
const loading = ref(false);
const showIncNote = ref(false);

watch(
  () => runResultsStore.run_results_digest,
  () => {
    initChartOptions();
  }
);

function initChartOptions() {
  option.value = {};
  buildOptions();
}

function buildOptions() {
  loading.value = true;
  const nominal = `nominal_pga_${props.direction}`;
  const actual = `actual_pga_${props.direction}`;
  const reported = `reported_t1_${props.direction}`;
  const visibleColumns = [nominal, actual, reported].filter(
    (col) =>
      runResultsStore.run_results_digest.filter(
        (run: RunResult) => run[col] !== null
      ).length > 0
  );
  let pgaColumn = visibleColumns.includes(actual) ? actual : nominal;
  const periodColumn = reported;
  if (
    !visibleColumns.includes(pgaColumn) ||
    !visibleColumns.includes(periodColumn)
  ) {
    loading.value = false;
    emit('loaded', false);
    return;
  }

  const datasetPGA: number[][] = runResultsStore.run_results_digest
    .filter(
      (result) => result[pgaColumn] !== null && result[periodColumn] !== null
    )
    .map((result) => {
      return [result[pgaColumn], result[periodColumn]];
    });
  emit('loaded', true);

  // keep only increasing pga values
  const datasetPGAInc = [];
  let previous = 0;
  for (let i = 0; i < datasetPGA.length; i++) {
    const pga = datasetPGA[i][0];
    if (pga > previous) {
      datasetPGAInc.push([pga, datasetPGA[i][1]]);
      previous = pga;
    } else {
      showIncNote.value = true;
    }
  }

  const newOption: EChartsOption = {
    // title: {
    //   text: `${t(periodColumn)} vs. ${t(pgaColumn)}`,
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
        return `${t(pgaColumn)}: ${params.value[0]} g<br />${t(
          periodColumn
        )}: ${params.value[1]} s`;
      },
    },
    xAxis: {
      type: 'value',
      name: `${t(pgaColumn + '_axis')} [g units]`,
      nameLocation: 'middle',
      nameTextStyle: {
        fontWeight: 'bold',
        fontSize: 16,
        padding: [20, 0, 0, 0],
      },
    },
    yAxis: {
      type: 'value',
      name: `${t(periodColumn + '_axis')} [sec.]`,
      nameLocation: 'middle',
      nameTextStyle: {
        fontWeight: 'bold',
        fontSize: 16,
        padding: [0, 0, 30, 0],
      },
    },
    series: [
      {
        name: t(pgaColumn),
        data: datasetPGAInc,
        type: 'line',
        symbolSize: 5,
      },
    ],
  };
  option.value = newOption;
  loading.value = false;
}
</script>
