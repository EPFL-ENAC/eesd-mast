<template>
  <div>
    <q-spinner v-if="loading" color="primary" size="3em" />
    <q-markdown :src="text" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  name: 'FileNodeMarkdown',
});
</script>
<script setup lang="ts">
import { api } from 'src/boot/axios';
import { FileNode } from 'src/components/models';

export interface FileNodeMarkdownProps {
  node: FileNode;
}
const props = withDefaults(defineProps<FileNodeMarkdownProps>(), {
  node: undefined,
});

const text = ref(null);
const loading = ref(false);

watch(
  () => props.node,
  () => {
    initMd();
  }
);

onMounted(() => {
  initMd();
});

function initMd() {
  if (!props.node) {
    return;
  }
  loading.value = true;
  api
    .get(`/files/${props.node.path}`)
    .then((res) => {
      text.value = res.data;
    })
    .finally(() => {
      loading.value = false;
    });
}
</script>
