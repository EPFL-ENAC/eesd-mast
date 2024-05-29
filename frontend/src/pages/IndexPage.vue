<template>
  <q-page>
    <q-img
      :src="'/' + imageUrl"
      spinner-color="white"
      :style="
        $q.screen.lt.sm
          ? 'height: 190px'
          : $q.screen.lt.md
          ? 'height: 165px'
          : 'height: 180px'
      "
    >
      <div
        :class="
          $q.screen.lt.sm ? 'q-mt-sm' : $q.screen.lt.md ? 'q-mt-md' : 'q-mt-lg'
        "
        class="row q-pa-lg full-width"
        style="background: transparent"
      >
        <div class="col"></div>
        <div class="col-md-10 col-sm-11 col-xs-12">
          <div
            :class="
              $q.screen.lt.sm
                ? 'text-h4'
                : $q.screen.lt.md
                ? 'text-h3'
                : 'text-h2'
            "
            class="text-weight-thin text-white"
          >
            {{ $t('app_title') }}
          </div>
          <div
            :class="
              $q.screen.lt.sm
                ? 'text-subtitle1'
                : $q.screen.lt.md
                ? 'text-h6'
                : 'text-h5'
            "
            class="text-white"
          >
            {{ $t('app_subtitle') }}
          </div>
        </div>
        <div class="col"></div>
      </div>
    </q-img>
    <div>
      <metrics-banner />
      <experiment-aggregations />
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
</script>
