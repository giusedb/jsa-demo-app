import { Orm } from 'jsalchemy';
export const user = ref(null);
const ormOptions = {
  endpoint: '/jsalchemy',
  autologin: true,
  keepSession: 3600,
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
export const orm = new Orm(ormOptions, handlers, reactive);
