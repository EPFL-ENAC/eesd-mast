<template>
  <div>
    <div v-if="fileNodes.length" class="row q-mb-md">
      <div class="col-8 col-md-8 col-xs-12">
        <q-btn
          :label="$t('download')"
          icon="download"
          size="sm"
          color="primary"
          class="q-mt-md q-mb-md"
          @click="downloadFiles"
        />
      </div>
      <div class="col-4 col-md-4 col-xs-12">
        <q-input
          ref="filterRef"
          dense
          clearable
          debounce="300"
          v-model="filter"
          :label="$t('search_files')"
        >
          <template v-slot:append>
            <q-icon
              v-if="filter !== ''"
              name="clear"
              class="cursor-pointer"
              @click="resetFilter"
            />
          </template>
        </q-input>
      </div>
    </div>
    <q-tree
      :nodes="fileNodes"
      node-key="path"
      label-key="name"
      :no-nodes-label="$t('no_files')"
      :no-results-label="$t('no_files')"
      :filter="filter"
      :filter-method="filesFilter"
    >
      <template v-slot:default-header="prop">
        <div>
          <span>{{ prop.node.name }}</span>
          <q-btn
            v-if="prop.node.is_file && prop.node.size"
            dense
            flat
            no-caps
            size="sm"
            :icon="
              displayed.includes(prop.node.path)
                ? 'visibility_off'
                : 'visibility'
            "
            color="grey-6"
            @click="displayFile(prop.node.path)"
            class="on-right"
          ></q-btn>
          <q-btn
            v-if="prop.node.is_file && prop.node.size"
            :label="fileSizeLabel(prop.node.size)"
            dense
            flat
            no-caps
            size="sm"
            icon="download"
            color="grey-6"
            @click="downloadFile(prop.node.path)"
            class="on-right"
          ></q-btn>
        </div>
      </template>
      <template v-slot:default-body="prop">
        <div v-if="displayed.includes(prop.node.path)">
          <q-img
            v-if="prop.node.name.endsWith('.png')"
            :src="`${baseUrl}/files/${prop.node.path}`"
            spinner-color="grey-6"
            fit="scale-down"
          />
          <div v-else-if="prop.node.name.endsWith('.txt')">
            <file-node-chart :node="prop.node" height="600px" />
          </div>
        </div>
      </template>
    </q-tree>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  name: 'ExperimentFilesView',
});
</script>
<script setup lang="ts">
import { baseUrl } from 'src/boot/axios';
import { withDefaults, computed, ref, watch } from 'vue';

import { Experiment, FileNode } from 'src/components/models';
import FileNodeChart from './FileNodeChart.vue';

const displayed = ref<string[]>([]);
const filter = ref('');
const filterRef = ref(null);

export interface ExperimentFilesViewProps {
  experiment: Experiment;
}
const props = withDefaults(defineProps<ExperimentFilesViewProps>(), {
  experiment: undefined,
});

const fileNodes = computed(() =>
  props.experiment && props.experiment.files && props.experiment.files.children
    ? props.experiment.files.children
    : []
);

watch(
  () => props.experiment,
  () => {
    displayed.value = [];
  }
);

function filesFilter(node: FileNode, filter: string) {
  const filt = filter.toLowerCase();
  return node.name && node.name.toLowerCase().indexOf(filt) > -1;
}

function resetFilter() {
  filter.value = '';
  if (filterRef.value) filterRef.value.focus();
}

function fileSizeLabel(size: number) {
  let val = size;
  let unit = 'B';
  if (val > 1024) {
    val /= 1024;
    unit = 'kB';
  }
  if (val > 1024) {
    val /= 1024;
    unit = 'MB';
  }
  return `${Math.round(val)} ${unit}`;
}

function downloadFile(path: string) {
  window.open(`${baseUrl}/files/${path}`);
}

function downloadFiles() {
  window.open(`${baseUrl}/experiments/${props.experiment.id}/files`);
}

function displayFile(path: string) {
  if (!displayed.value.includes(path)) {
    displayed.value.push(path);
  } else {
    displayed.value = displayed.value.filter((p) => p !== path);
  }
}
</script>
