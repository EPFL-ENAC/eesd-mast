<template>
  <div>
    <div v-if="!hasFiles" class="text-grey-6">
      {{ $t('no_files') }}
    </div>
    <div v-else>
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
          <div class="row">
            <span class="text-subtitle2 q-mt-sm">{{
              $t('files_count', filesCount)
            }}</span>
            <span class="on-right text-grey-6 text-caption q-mt-sm">
              ({{
                $t('files_size_uncompressed', {
                  size: fileSizeLabel(filesSize),
                })
              }})
            </span>
            <q-space />
            <q-btn
              :label="$t('download')"
              no-caps
              icon="download"
              color="secondary"
              flat
              class="on-left"
              @click="downloadFiles"
            />
            <q-input
              ref="filterRef"
              dense
              clearable
              debounce="300"
              v-model="filter"
              style="width: 200px"
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
                  color="secondary"
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
                    :src="`${cdnUrl}${prop.node.path}`"
                    spinner-color="grey-6"
                    fit="scale-down"
                  />
                  <div v-else-if="prop.node.name.endsWith('.md')">
                    <file-node-markdown :node="prop.node" />
                  </div>
                  <div v-else-if="prop.node.name.endsWith('.tcl')">
                    <file-node-txt :node="prop.node" />
                  </div>
                  <div v-else-if="prop.node.name.endsWith('.txt')">
                    <file-node-chart
                      :node="prop.node"
                      :xname="$t(getXName(prop.node))"
                      :yname="$t(getYName(prop.node))"
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
export default defineComponent({
  name: 'ExperimentFilesView',
});
</script>
<script setup lang="ts">
import { baseUrl, cdnUrl } from 'src/boot/axios';
import { withDefaults, computed, ref, watch } from 'vue';

import { Experiment, FileNode } from 'src/components/models';
import FileNodeChart from './charts/FileNodeChart.vue';
import FileNodeMarkdown from './FileNodeMarkdown.vue';
import FileNodeTxt from './FileNodeTxt.vue';
import VtkViewer from './VtkViewer.vue';

const displayed = ref<string[]>([]);
const filter = ref('');
const filterRef = ref(null);
const mdTab = ref<string>('');

interface ExperimentFilesViewProps {
  experiment: Experiment;
  type: 'test' | 'model';
}
const props = withDefaults(defineProps<ExperimentFilesViewProps>(), {
  experiment: undefined,
  type: 'test',
});

const hasFiles = computed(() =>
  props.experiment ? props.experiment[getAttribute()] != null : false
);

const fileNodes = computed(() => {
  const files =
    props.experiment && (props.experiment[getAttribute()] as FileNode);
  sortFilesRecursively(files);
  return files.children ? files.children : [];
});

const mdFiles = computed(() =>
  fileNodes.value.filter((node) => node.name.endsWith('.md'))
);

const filesCount = computed<number>(() => {
  return props.experiment
    ? countFiles(props.experiment[getAttribute()] as FileNode)
    : 0;
});

const filesSize = computed<number>(() => {
  return props.experiment
    ? totalFilesSize(props.experiment[getAttribute()] as FileNode)
    : 0;
});

watch(
  () => props.experiment,
  () => initViewer()
);

onMounted(() => {
  initViewer();
});

function getAttribute() {
  return `${props.type}_files`;
}

function initViewer() {
  displayed.value = [];
  filter.value = '';
  const mds =
    props.experiment && props.experiment[getAttribute()]
      ? (props.experiment[getAttribute()] as FileNode).children?.filter(
          (node: FileNode) => node.name.endsWith('.md')
        )
      : [];
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
  window.open(`${cdnUrl}${path}`);
}

function downloadFiles() {
  window.open(
    `${baseUrl}/experiments/${props.experiment.id}/${getAttribute().replace(
      '_',
      '-'
    )}`
  );
}

function canBeDisplayed(node: FileNode) {
  return (
    node.name.endsWith('.png') ||
    node.name.endsWith('.md') ||
    node.name.endsWith('.txt') ||
    node.name.endsWith('.tcl') ||
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
