<template>
  <div :style="`height: ${height}`">
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
  xname?: string;
  yname?: string;
  height?: string;
}
const props = withDefaults(defineProps<FileNodeChartProps>(), {
  node: undefined,
  xname: '',
  yname: '',
  height: '200px',
});

const chart = shallowRef(null);
const option = ref<EChartsOption>({});
const loading = ref(false);

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
      left: 60,
      top: 60,
      right: 50,
      bottom: 100,
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
      name: props.xname,
      nameLocation: 'middle',
      nameTextStyle: {
        fontWeight: 'bold',
        fontSize: 16,
        padding: [10, 0, 0, 0],
      },
    },
    yAxis: {
      type: 'value',
      name: props.yname,
      nameLocation: 'middle',
      nameTextStyle: {
        fontWeight: 'bold',
        fontSize: 16,
        padding: [0, 0, 30, 0],
      },
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
  loading.value = true;
  api.get(`/files/${props.node.path}`).then((res) => {
    Papa.parse(res.data, {
      header: false,
      dynamicTyping: true,
      complete: (results) => {
        loading.value = false;
        const data = results.data;
        option.value.series[0].data = data;
        chart.value?.setOption(option.value);
      },
    });
  });
}
</script>
