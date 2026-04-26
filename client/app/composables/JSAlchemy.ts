import { Orm } from 'jsalchemy';
import { reactive } from "@vue/reactivity";
import type {IOrmOptions} from "jsalchemy/jsalchemy/ts/interfaces";

export const user = ref(null);
const ormOptions: IOrmOptions = {
  endpoint: '/jsalchemy',
  autologin: true,
  keepSession: 3600,
  ws: {
    host: 'localhost',
    port: 7998,
    channel: 'js-router'
  },
  uiFramework: 'vue',
  reactiveFunc: ref,
};

const handlers = {
    'logged-in': (status: object) => {
        console.info(`User ${status.user.first_name} ${status.user.last_name} logged in`);
        user.value = status.user;
    },
    'logged-out': () => {
        console.info('Log out');
        user.value = null;
    },
};
export const orm = new Orm(ormOptions, handlers);
