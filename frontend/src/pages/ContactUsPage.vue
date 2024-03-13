<template>
  <q-page>
    <div class="q-pa-md">
      <p>{{ $t('contact_us_intro') }}</p>

      <div class="q-mt-md">
        <q-btn
          color="red"
          no-caps
          label="Katrin Beyer"
          @click="openPeoplePage('katrin.beyer')"
        />
        <q-btn
          class="on-right"
          color="red"
          no-caps
          label="Mathias Haindl"
          @click="openPeoplePage('mathias.haindl')"
        />
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import DataSubmissionMd from 'src/assets/data-submission.md';

function openPeoplePage(username: string) {
  window.open(`https://people.epfl.ch/${username}?lang=en`);
}
</script>
