<template>
  <q-toolbar>
    <q-btn
      v-if="$q.screen.lt.md && isBuildings"
      flat
      dense
      round
      icon="menu"
      aria-label="Menu"
      :disable="!isBuildings"
      @click="toggleLeftDrawer"
    />

    <span
      class="q-ml-sm q-mr-lg"
      :class="$q.screen.lt.md ? 'text-bold' : 'text-h6'"
    >
      Masonry Shake Table Database
    </span>
    <q-btn
      flat
      dense
      :label="$t('overview')"
      no-caps
      to="/"
      :class="isHome ? 'text-primary' : ''"
      class="q-pt-sm q-pb-sm q-pr-md q-pl-md"
    />
    <q-btn
      flat
      dense
      :label="$t('buildings')"
      no-caps
      to="/buildings"
      :class="isBuildings ? 'text-primary' : ''"
      class="on-left on-right q-pt-sm q-pb-sm q-pr-md q-pl-md"
    />
    <q-space />
    <q-btn flat :label="$t('contact_us')" no-caps @click="onShowContact" />
    <q-btn
      flat
      round
      icon="info"
      :title="$t('introduction')"
      @click="onShowIntro"
      class="on-left"
    ></q-btn>
    <a href="https://epfl.ch" target="_blank" class="q-mr-lg q-mt-sm">
      <img src="/EPFL.svg" style="width: 80px" />
    </a>
    <a href="https://www.epfl.ch/labs/eesd/" target="_blank" class="q-mt-sm">
      <img src="/EESD.svg" style="width: 88px" class="float-right q-mb-xs" />
    </a>
  </q-toolbar>

  <q-dialog v-model="showIntro">
    <q-card>
      <q-card-section class="q-ml-md q-mr-md">
        <div class="text-subtitle1 text-grey-8">
          <q-markdown :src="OverViewMd" no-line-numbers />
        </div>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat :label="$t('close')" color="primary" v-close-popup />
      </q-card-actions>
    </q-card>
  </q-dialog>

  <q-dialog v-model="showContact">
    <q-card :style="$q.screen.lt.md ? '' : 'width: 500px; max-width: 80vw'">
      <q-card-section class="q-mt-md q-ml-md q-mr-md">
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
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat :label="$t('close')" color="primary" v-close-popup />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  name: 'AppToolbar',
});
</script>
<script setup lang="ts">
import { getSettings, saveSettings } from 'src/utils/settings';
import OverViewMd from 'src/assets/overview.md';

const emit = defineEmits(['toggle']);

const route = useRoute();

const showIntro = ref(false);
const showContact = ref(false);

const isHome = computed(() => route.path === '/');
const isBuildings = computed(() => route.path.startsWith('/buildings'));

onMounted(() => {
  const settings = getSettings();
  if (!settings.intro_shown) {
    showIntro.value = true;
    settings.intro_shown = true;
    saveSettings(settings);
  }
});

function onShowIntro() {
  showIntro.value = true;
}

function onShowContact() {
  showContact.value = true;
}

function openPeoplePage(username: string) {
  window.open(`https://people.epfl.ch/${username}?lang=en`);
}

function toggleLeftDrawer() {
  emit('toggle');
}
</script>