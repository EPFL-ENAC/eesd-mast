<template>
  <div>
    <q-spinner v-if="loading" color="primary" size="3em" />
    <q-markdown
      :src="text"
      :class="withShowMore && showMore ? 'fading-bottom' : ''"
    />
    <div v-if="withShowMore" class="bg-grey-3 text-grey-8 text-center">
      <q-btn
        flat
        no-caps
        @click="toggleShowMore()"
        :icon-right="showMore ? 'expand_more' : 'expand_less'"
        class="full-width"
        >{{ $t(`${showMore ? 'show_more' : 'show_less'}`) }}</q-btn
      >
    </div>
  </div>
</template>

<script lang="ts">
export default defineComponent({
  name: 'FileNodeMarkdown',
});
</script>
<script setup lang="ts">
import { api, cdnUrl } from 'src/boot/axios';
import { FileNode } from 'src/components/models';

export interface FileNodeMarkdownProps {
  node: FileNode;
}
const props = withDefaults(defineProps<FileNodeMarkdownProps>(), {
  node: undefined,
});

const text = ref(null);
const allText = ref('');
const loading = ref(false);
const withShowMore = ref(false);
const showMore = ref(true);

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
  withShowMore.value = false;
  showMore.value = true;
  api
    .get(`${cdnUrl}${props.node.path}`)
    .then((res) => {
      allText.value = res.data;
      if (res.data.length > 1000) {
        text.value = res.data.slice(0, 1000) + '...';
      } else {
        text.value = res.data;
      }
      withShowMore.value = res.data && res.data.length > 1000;
    })
    .finally(() => {
      loading.value = false;
    });
}

function toggleShowMore() {
  showMore.value = !showMore.value;
  if (showMore.value) {
    text.value = allText.value.slice(0, 1000) + '...';
  } else {
    text.value = allText.value;
  }
}
</script>

<style lang="scss" scoped>
.fading-bottom {
  mask-image: linear-gradient(to bottom, black 0%, transparent 100%);
}
</style>
