<template>
  <q-page>
    <h5 class="q-pa-md q-mt-sm q-mb-sm">{{ $t('data_submission') }}</h5>
    <q-separator />
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
      <div></div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
function openPeoplePage(username: string) {
  window.open(`https://people.epfl.ch/${username}?lang=en`);
}
</script>
