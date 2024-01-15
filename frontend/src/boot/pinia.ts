import { createPinia } from 'pinia';

const pinia = createPinia();

// @ts-expect-error initial test
export default ({ app }) => {
  app.use(pinia);
};
