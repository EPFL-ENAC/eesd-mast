<template>
  <q-page>
    <q-img
      :src="'/' + imageUrl"
      spinner-color="white"
      :style="
        $q.screen.lt.lg
          ? $q.screen.lt.md
            ? 'height: 150px'
            : 'height: 165px'
          : 'height: 180px'
      "
    >
      <div
        class="row q-pa-lg q-mt-lg full-width"
        style="background: transparent"
      >
        <div class="col"></div>
        <div class="col-md-10 col-sm-10 col-xs-12">
          <div
            :class="
              $q.screen.lt.lg
                ? $q.screen.lt.md
                  ? 'text-h4'
                  : 'text-h3'
                : 'text-h2'
            "
            class="text-weight-thin text-white"
          >
            {{ $t('app_title') }}
          </div>
          <div class="text-subtitle1 text-white">
            {{ $t('app_subtitle') }}
          </div>
        </div>
        <div class="col"></div>
      </div>
    </q-img>
    <div class="row">
      <div :class="$q.screen.lt.xl ? 'col-0' : 'col-1'"></div>
      <div :class="$q.screen.lt.xl ? 'col-12' : 'col-10'">
        <metrics-banner />
        <experiment-aggregations />
      </div>
      <div :class="$q.screen.lt.xl ? 'col-0' : 'col-1'"></div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import MetricsBanner from 'src/components/MetricsBanner.vue';
import ExperimentAggregations from 'src/components/ExperimentAggregations.vue';

const imageUrls = [
  'Website_Background_Title_Option1_blue.webp',
  'Website_Background_Title_Option2.webp',
];
const imageIndex = ref(0);
const imageUrl = ref(imageUrls[imageIndex.value]);

onMounted(() => {
  const intervalId = setInterval(() => {
    imageIndex.value = (imageIndex.value + 1) % imageUrls.length;
    imageUrl.value = imageUrls[imageIndex.value];
  }, 5000);

  return () => clearInterval(intervalId);
});
</script>
