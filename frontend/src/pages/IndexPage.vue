<template>
  <q-page>
    <div class="q-pa-md">
      <h5 class="q-mt-sm q-mb-sm">{{ $t('overview') }}</h5>
      <div class="text-subtitle1 text-grey-8">
        {{ $t('summary') }}
      </div>
    </div>

    <q-separator />
    <div class="q-pa-md">
      <div>
        <q-markdown :src="OverViewMd" no-line-numbers />
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import OverViewMd from 'src/assets/overview.md';
</script>
