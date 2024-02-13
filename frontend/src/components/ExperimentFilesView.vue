<template>
  <div>
    <div v-if="props.experiment?.files == null" class="text-grey-6">
      {{ $t('no_files') }}
    </div>
    <div v-else>
      <div v-if="fileNodes.length" class="row q-mb-md">
        <div class="col-8 col-md-8 col-xs-12">
          <q-btn
            :label="$t('download')"
            no-caps
            icon="download"
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

      <q-card v-if="mdFiles.length" class="q-mb-md">
        <q-card-section class="bg-grey-3 text-grey-8 q-pa-none">
          <q-tabs v-model="mdTab" align="left">
            <q-tab
              :name="md.name"
              :label="md.name"
              v-for="md in mdFiles"
              :key="md.path"
              no-caps
            />
          </q-tabs>
        </q-card-section>
        <q-card-section>
          <q-tab-panels v-model="mdTab" animated>
            <q-tab-panel :name="md.name" v-for="md in mdFiles" :key="md.path">
              <file-node-markdown :node="md" />
            </q-tab-panel>
          </q-tab-panels>
        </q-card-section>
      </q-card>

      <q-card>
        <q-card-section class="bg-grey-3 text-grey-8">
          <div class="text-subtitle2">
            <span>{{ $t('files_count', filesCount) }}</span>
            <span class="on-right text-grey-6 text-caption">
              ({{
                $t('files_size_uncompressed', {
                  size: fileSizeLabel(filesSize),
                })
              }})
            </span>
          </div>
        </q-card-section>
        <q-card-section>
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
                <q-icon
                  v-if="!prop.node.is_file"
                  name="folder"
                  color="primary"
                  class="on-left"
                />
                <q-icon
                  v-else
                  name="insert_drive_file"
                  color="grey-6"
                  class="on-left"
                />
                <span>{{ prop.node.name }}</span>
                <q-btn
                  v-if="
                    prop.node.is_file &&
                    prop.node.size &&
                    canBeDisplayed(prop.node)
                  "
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
              <q-card v-if="displayed.includes(prop.node.path)" flat bordered>
                <q-card-section>
                  <q-img
                    v-if="prop.node.name.endsWith('.png')"
                    :src="`${baseUrl}/files/${prop.node.path}`"
                    spinner-color="grey-6"
                    fit="scale-down"
                  />
                  <div v-else-if="prop.node.name.endsWith('.md')">
                    <file-node-markdown :node="prop.node" />
                  </div>
                  <div v-else-if="prop.node.name.endsWith('.txt')">
                    <file-node-chart
                      :node="prop.node"
                      :xname="$t(getXName(prop.node))"
                      :yname="$t(getYName(prop.node))"
                      height="600px"
                    />
                  </div>
                  <div
                    v-else-if="
                      prop.node.name.endsWith('.vtp') ||
                      prop.node.alt_name?.endsWith('.vtp')
                    "
                  >
                    <vtk-viewer :file="prop.node" :download="false" />
                  </div>
                </q-card-section>
              </q-card>
            </template>
          </q-tree>
        </q-card-section>
      </q-card>
    </div>
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
import FileNodeMarkdown from './FileNodeMarkdown.vue';
import VtkViewer from './VtkViewer.vue';

const displayed = ref<string[]>([]);
const filter = ref('');
const filterRef = ref(null);
const mdTab = ref<string>('');

export interface ExperimentFilesViewProps {
  experiment: Experiment;
}
const props = withDefaults(defineProps<ExperimentFilesViewProps>(), {
  experiment: undefined,
});

const fileNodes = computed(() => {
  const files = props.experiment && props.experiment.files;
  sortFilesRecursively(files);
  return files.children ? files.children : [];
});

const mdFiles = computed(() =>
  fileNodes.value.filter((node) => node.name.endsWith('.md'))
);

const filesCount = computed<number>(() => {
  return countFiles(props.experiment?.files);
});

const filesSize = computed<number>(() => {
  return totalFilesSize(props.experiment?.files);
});

watch(
  () => props.experiment,
  () => initViewer()
);

onMounted(() => {
  initViewer();
});

function initViewer() {
  displayed.value = [];
  filter.value = '';
  const mds = props.experiment?.files?.children?.filter((node) =>
    node.name.endsWith('.md')
  );
  if (mds && mds.length) {
    mdTab.value =
      mds.find((md) => md.name.toLocaleLowerCase() === 'readme.md')?.name ||
      mds[0].name;
  } else {
    mdTab.value = '';
  }
}

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

function canBeDisplayed(node: FileNode) {
  return (
    node.name.endsWith('.png') ||
    node.name.endsWith('.md') ||
    node.name.endsWith('.txt') ||
    node.name.endsWith('.vtp') ||
    node.alt_name?.endsWith('.vtp')
  );
}

function getXName(node: FileNode) {
  const folders = decodeURI(node.path).split('/');
  if (
    folders.includes('Top displacement histories') ||
    folders.includes('Shake-table accelerations')
  ) {
    return 'time_sec';
  } else if (folders.includes('Global force-displacement curve')) {
    return 'top_displacement_mm';
  }
  return '';
}

function getYName(node: FileNode) {
  const folders = decodeURI(node.path).split('/');
  if (folders.includes('Top displacement histories')) {
    return 'displacement_mm';
  } else if (folders.includes('Shake-table accelerations')) {
    return 'acceleration_g';
  } else if (folders.includes('Global force-displacement curve')) {
    return 'base_shear_kn';
  }
  return '';
}

function displayFile(path: string) {
  if (!displayed.value.includes(path)) {
    displayed.value.push(path);
  } else {
    displayed.value = displayed.value.filter((p) => p !== path);
  }
}

function countFiles(node: FileNode): number {
  if (!node) {
    return 0;
  }
  if (node.is_file) {
    return 1;
  }
  return node.children
    ? node.children.reduce((acc, child) => acc + countFiles(child), 0)
    : 0;
}

function totalFilesSize(node: FileNode): number {
  if (!node) {
    return 0;
  }
  if (node.is_file) {
    return node.size as number;
  }
  return node.children
    ? node.children.reduce((acc, child) => acc + totalFilesSize(child), 0)
    : 0;
}

function sortFilesRecursively(node: FileNode) {
  if (node.children) {
    node.children.sort(sortFiles);
    node.children.forEach(sortFilesRecursively);
  }
}

function sortFiles(a: FileNode, b: FileNode) {
  if (a.is_file && !b.is_file) {
    return 1;
  }
  if (!a.is_file && b.is_file) {
    return -1;
  }
  return a.name.localeCompare(b.name);
}
</script>
