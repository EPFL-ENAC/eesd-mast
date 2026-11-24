// Configuration for your app
// https://v2.quasar.dev/quasar-cli-vite/quasar-config-file

import { defineConfig } from '#q-app';

export default defineConfig((ctx) => {
  return {
    // app boot file (/src/boot)
    // --> boot files are part of "main.js"
    // https://v2.quasar.dev/quasar-cli-vite/boot-files
    boot: ['i18n', 'axios', 'settings'],

    // https://v2.quasar.dev/quasar-cli-vite/quasar-config-file#css
    css: ['app.scss'],

    // https://github.com/quasarframework/quasar/tree/dev/extras
    extras: ['roboto-font', 'material-icons'],

    // Full list of options: https://v2.quasar.dev/quasar-cli-vite/quasar-config-file#build
    build: {
      target: {
        browser: ['es2022', 'firefox115', 'chrome115', 'safari14'],
        node: 'node22',
      },

      typescript: {
        strict: false,
        vueShim: true,
      },

      vueRouterMode: 'history', // available values: 'hash', 'history'

      defineEnv: {
        API_URL: ctx.dev ? 'http://localhost:8000' : process.env.API_URL,
        API_PATH: ctx.dev ? '' : process.env.API_PATH,
      },

      vitePlugins: [
        [
          'unplugin-auto-import/vite',
          {
            imports: ['vue', 'vue-router', 'vue-i18n', 'pinia'],
            dts: 'src/auto-imports.d.ts',
            dirs: ['src/composables', 'src/models', 'src/stores'],
            vueTemplate: true,
            eslintrc: {
              enabled: true,
              filepath: './.eslintrc-auto-import.json',
              globalsPropValue: true,
            },
          },
        ],
      ],
    },

    devServer: {
      open: false, // do not open browser window automatically
    },

    framework: {
      config: {},
      plugins: ['Notify', 'LocalStorage', 'LoadingBar'],
    },

    animations: [],
  };
});
