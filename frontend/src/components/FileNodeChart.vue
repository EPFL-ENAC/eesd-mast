<template>
  <div :style="`height: ${height}`">
    <e-charts
      ref="chart"
      autoresize
      :init-options="initOptions"
      :option="option"
      :update-options="updateOptions"
      class="q-ma-md"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  name: 'FileNodeChart',
});
</script>
<script setup lang="ts">
import ECharts from 'vue-echarts';
import type { EChartsOption } from 'echarts';
import { use } from 'echarts/core';
import { LineChart } from 'echarts/charts';
import { SVGRenderer } from 'echarts/renderers';
import { initOptions, updateOptions } from './charts';
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  DataZoomComponent,
} from 'echarts/components';
import Papa from 'papaparse';
import { api } from 'src/boot/axios';
import { FileNode } from 'src/components/models';

use([
  SVGRenderer,
  LineChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  DataZoomComponent,
]);

export interface FileNodeChartProps {
  node: FileNode;
  height?: string;
}
const props = withDefaults(defineProps<FileNodeChartProps>(), {
  node: undefined,
  height: '200px',
});

const chart = shallowRef(null);
const option = ref<EChartsOption>({});

watch(
  () => props.node,
  () => {
    initChartOptions();
  }
);

onMounted(() => {
  initChartOptions();
});

function initChartOptions() {
  if (option.value.series && option.value.series.length > 0) {
    return;
  }
  const name = props.node.name.split('.')[0];
  const newOption: EChartsOption = {
    title: {
      text: name,
    },
    grid: {
      left: 30,
      top: 40,
      right: 20,
      bottom: 40,
    },
    tooltip: {
      trigger: 'axis',
    },
    dataZoom: [
      {
        id: 'dataZoomX',
        type: 'slider',
        xAxisIndex: [0],
        filterMode: 'filter',
      },
      {
        id: 'dataZoomY',
        type: 'slider',
        yAxisIndex: [0],
        filterMode: 'empty',
      },
    ],
    xAxis: {
      type: 'value',
    },
    yAxis: {
      type: 'value',
    },
    series: [
      {
        data: [],
        type: 'line',
        symbolSize: 0,
      },
    ],
  };
  option.value = newOption;
  api.get(`/files/${props.node.path}`).then((res) => {
    Papa.parse(res.data, {
      header: false,
      dynamicTyping: true,
      complete: (results) => {
        const data = results.data;
        option.value.series[0].data = data;
        chart.value?.setOption(option.value);
      },
    });
  });
}
</script>
