<template>
  <div v-if="file">
    <div class="q-mb-md row">
      <q-select
        v-model="representation"
        :options="representationOptions"
        map-options
        @update:model-value="applyRepresentation"
        style="width: 200px"
      />
      <q-space v-if="download" />
      <q-btn
        v-if="download"
        :label="file.name"
        no-caps
        color="primary"
        icon="download"
        @click="downloadFile(file.path)"
        class="q-mt-md q-mb-md on-left"
      />
    </div>
    <div>
      <div ref="vtkContainer" style="height: 600px" />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  name: 'VtkViewer',
});
</script>
<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { baseUrl } from 'src/boot/axios';
import { FileNode } from './models';

import '@kitware/vtk.js/Rendering/Profiles/Geometry';

import vtkFullScreenRenderWindow from '@kitware/vtk.js/Rendering/Misc/FullScreenRenderWindow';
import vtkXMLPolyDataReader from '@kitware/vtk.js/IO/XML/XMLPolyDataReader';

import vtkActor from '@kitware/vtk.js/Rendering/Core/Actor';
import vtkMapper from '@kitware/vtk.js/Rendering/Core/Mapper';

export interface VtkViewerProps {
  file: FileNode | undefined;
  download: boolean;
}
const props = withDefaults(defineProps<VtkViewerProps>(), {
  file: undefined,
  download: true,
});

const { t } = useI18n({ useScope: 'global' });

const representationOptions = [
  { label: t('wireframe'), value: 1 },
  { label: t('surface'), value: 2 },
];
const representation = ref(representationOptions[1]);
const vtkContainer = ref(null);
const context = ref(null);

function applyRepresentation() {
  if (context.value) {
    const { actor, renderWindow } = context.value;
    actor.getProperty().setRepresentation(representation.value.value);
    renderWindow.render();
  }
}

watch(
  () => props.file,
  () => {
    cleanContext();
    initContext();
  }
);

onMounted(initContext);

onBeforeUnmount(cleanContext);

function initContext() {
  if (props.file && !context.value) {
    // Create a renderer
    const fullScreenRenderer = vtkFullScreenRenderWindow.newInstance({
      container: vtkContainer.value,
    });
    const renderer = fullScreenRenderer.getRenderer();
    const renderWindow = fullScreenRenderer.getRenderWindow();

    // Set up the HTTP dataset reader
    // const reader = vtkHttpDataSetReader.newInstance();
    // reader.setUrl(`${baseUrl}/files/${props.file.path}`, { fullpath: true });
    const reader = vtkXMLPolyDataReader.newInstance();
    const path = props.file.path.endsWith('.vtp')
      ? props.file.path
      : props.file.alt_path;
    reader.setUrl(`${baseUrl}/files/${path}`);

    // Load the dataset
    reader.loadData().then(() => {
      const dataset = reader.getOutputData(0);

      // Create a mapper and set its input connection to the dataset
      const mapper = vtkMapper.newInstance();
      mapper.setInputData(dataset);

      // Create an actor and set its mapper
      const actor = vtkActor.newInstance();
      actor.setMapper(mapper);
      actor.getProperty().setColor(0.5, 1, 0); // RGB values between 0 and 1

      // Add the actor to the renderer
      renderer.addActor(actor);

      // Initialize the rendering process
      renderer.resetCamera();
      renderWindow.render();

      context.value = {
        renderWindow,
        renderer,
        actor,
        mapper,
      };
    });
  }
}

function cleanContext() {
  if (context.value) {
    const { actor, mapper } = context.value;
    actor.delete();
    mapper.delete();
    context.value = null;
  }
}

function downloadFile(path: string) {
  window.open(`${baseUrl}/files/${path}`);
}
</script>

<style scoped>
.controls {
  position: absolute;
  top: 25px;
  left: 25px;
  background: white;
  padding: 12px;
}
</style>
