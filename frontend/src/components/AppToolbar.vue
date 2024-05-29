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
    <a href="https://epfl.ch" target="_blank" class="q-mt-sm">
      <img src="/EPFL_logo.png" style="height: 25px" />
    </a>
    <span
      class="q-ml-lg q-mr-lg"
      :class="$q.screen.lt.md ? 'text-bold' : 'text-h6'"
    >
      {{ $t('app_title') }}
    </span>
    <q-btn
      flat
      dense
      :label="$t('overview')"
      no-caps
      to="/"
      :class="isHome ? 'text-primary' : ''"
      class="q-pt-sm q-pb-sm q-pr-md q-pl-md"
      style="font-size: 1.15rem"
    />
    <q-btn
      flat
      dense
      :label="$t('buildings')"
      no-caps
      to="/buildings"
      :class="isBuildings ? 'text-primary' : ''"
      class="on-left on-right q-pt-sm q-pb-sm q-pr-md q-pl-md"
      style="font-size: 1.15rem"
    />
    <q-space />
    <q-btn
      flat
      round
      icon="account_circle"
      :title="$t('contact_us')"
      @click="onShowContact"
    />
    <q-btn
      flat
      round
      icon="menu_book"
      :title="$t('resources')"
      @click="onShowResources"
    ></q-btn>
    <q-btn
      flat
      round
      icon="info"
      :title="$t('introduction')"
      @click="onShowIntro"
    ></q-btn>
    <q-btn
      flat
      round
      icon="handshake"
      :title="$t('acknowledgements')"
      @click="onShowAcknowledgements"
      class="on-left"
    ></q-btn>
    <a href="https://www.epfl.ch/labs/eesd/" target="_blank" class="q-mt-sm">
      <img
        src="/EESD_logo.png"
        style="height: 25px"
        class="float-right q-mb-xs"
      />
    </a>
  </q-toolbar>

  <q-dialog v-model="showIntro">
    <q-card>
      <q-card-section class="q-ml-md q-mr-md">
        <div class="text-h6 q-mb-md">
          {{ $t('app_title') }}
        </div>
        <div class="text-subtitle1 text-grey-8">
          <q-markdown :src="OverViewMd" no-line-numbers />
        </div>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat :label="$t('close')" color="primary" v-close-popup />
      </q-card-actions>
    </q-card>
  </q-dialog>

  <q-dialog v-model="showAcknowledgements">
    <q-card>
      <q-card-section class="q-ml-md q-mr-md">
        <div class="text-h6 q-mb-md">
          {{ $t('acknowledgements') }}
        </div>
        <div class="text-subtitle1 text-grey-8">
          <q-markdown :src="AcknowledgementsMd" />
        </div>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat :label="$t('close')" color="primary" v-close-popup />
      </q-card-actions>
    </q-card>
  </q-dialog>

  <q-dialog v-model="showResources">
    <q-card>
      <q-card-section class="q-ml-md q-mr-md">
        <div class="text-h6 q-mb-sm">
          {{ $t('resources') }}
        </div>
        <q-list class="bg-grey-2">
          <essential-link
            v-for="link in essentialLinks"
            :key="link.title"
            v-bind="link"
          />
        </q-list>
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
import AcknowledgementsMd from 'src/assets/acknowledgements.md';
import EssentialLink, {
  EssentialLinkProps,
} from 'components/EssentialLink.vue';

const emit = defineEmits(['toggle']);

const route = useRoute();

const showIntro = ref(false);
const showResources = ref(false);
const showContact = ref(false);
const showAcknowledgements = ref(false);

const isHome = computed(() => route.path === '/');
const isBuildings = computed(
  () =>
    route.path.startsWith('/buildings') ||
    route.path.startsWith('/test') ||
    route.path.startsWith('/model')
);

const essentialLinks: EssentialLinkProps[] = [
  {
    title: 'EPFL',
    caption: 'epfl.ch',
    icon: 'school',
    link: 'https://epfl.ch',
  },
  {
    title: 'EESD',
    caption: 'epfl.ch/labs/eesd',
    icon: 'engineering',
    link: 'https://www.epfl.ch/labs/eesd/',
  },
  {
    title: 'ENAC IT4R',
    caption: 'go.epfl.ch/it4r',
    icon: 'construction',
    link: 'https://www.epfl.ch/schools/enac/about/data-at-enac/enac-it4research/',
  },
  {
    title: 'MAST CLI',
    caption: 'EPFL-ENAC/eesd-mast-cli',
    icon: 'code',
    link: 'https://github.com/EPFL-ENAC/eesd-mast-cli',
  },
];

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

function onShowResources() {
  showResources.value = true;
}

function onShowContact() {
  showContact.value = true;
}

function onShowAcknowledgements() {
  showAcknowledgements.value = true;
}

function openPeoplePage(username: string) {
  window.open(`https://people.epfl.ch/${username}?lang=en`);
}

function toggleLeftDrawer() {
  emit('toggle');
}
</script>
