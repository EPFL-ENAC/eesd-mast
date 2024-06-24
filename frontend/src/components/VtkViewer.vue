<template>
  <div v-if="file">
    <div class="row">
      <div
        class="col-lg-6 col-md-8 col-sm-12"
        :style="`width: ${width}; height: ${width};`"
      >
        <div v-if="withRepresentation || download" class="q-mb-md row">
          <q-select
            v-if="withRepresentation"
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
        <div ref="vtkContainer" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
export default defineComponent({
  name: 'VtkViewer',
});
</script>
<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { cdnUrl } from 'src/boot/axios';
import { FileNode } from './models';

import '@kitware/vtk.js/Rendering/Profiles/Geometry';

import vtkFullScreenRenderWindow from '@kitware/vtk.js/Rendering/Misc/FullScreenRenderWindow';
import vtkXMLPolyDataReader from '@kitware/vtk.js/IO/XML/XMLPolyDataReader';

import vtkActor from '@kitware/vtk.js/Rendering/Core/Actor';
import vtkMapper from '@kitware/vtk.js/Rendering/Core/Mapper';
import vtkRenderWindow from '@kitware/vtk.js/Rendering/Core/RenderWindow';
import vtkRenderer from '@kitware/vtk.js/Rendering/Core/Renderer';

export interface VtkViewerProps {
  file: FileNode | undefined;
  download: boolean;
  withRepresentation: boolean;
  width: string;
}
const props = withDefaults(defineProps<VtkViewerProps>(), {
  file: undefined,
  download: true,
  withRepresentation: false,
  width: '400px',
});

const { t } = useI18n({ useScope: 'global' });

const representationOptions = [
  { label: t('wireframe'), value: 1 },
  { label: t('surface'), value: 2 },
];
const representation = ref(representationOptions[1]);
const vtkContainer = ref();
const context = ref<{
  renderWindow: vtkRenderWindow;
  renderer: vtkRenderer;
  actor: vtkActor;
  mapper: vtkMapper;
}>();

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
      background: [0.9, 0.9, 0.9],
    });
    const renderer = fullScreenRenderer.getRenderer();
    const renderWindow = fullScreenRenderer.getRenderWindow();

    // Set up the HTTP dataset reader
    // const reader = vtkHttpDataSetReader.newInstance();
    // reader.setUrl(`${cdnUrl}${props.file.path}`, { fullpath: true });
    const reader = vtkXMLPolyDataReader.newInstance();
    const path = props.file.path.endsWith('.vtp')
      ? props.file.path
      : props.file.alt_path;
    reader.setUrl(`${cdnUrl}${path}`);

    // Load the dataset
    reader.loadData().then(() => {
      const dataset = reader.getOutputData(0);

      // Create a mapper and set its input connection to the dataset
      const mapper = vtkMapper.newInstance();
      mapper.setInputData(dataset);

      // Create an actor and set its mapper
      const actor = vtkActor.newInstance();
      actor.setMapper(mapper);
      // actor.getProperty().setColor(0.5, 1, 0); // RGB values between 0 and 1

      // Add the actor to the renderer
      renderer.addActor(actor);

      // Access the camera and set the view angle
      const camera = renderer.getActiveCamera();

      // Adjust the camera
      //camera.setPosition(0, 0, 0);
      camera.setFocalPoint(10, 20, -10);
      camera.setViewUp(0, 0, 1);

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
    context.value = undefined;
  }
}

function downloadFile(path: string) {
  window.open(`${cdnUrl}${path}`);
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
