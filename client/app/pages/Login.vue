<script setup lang="ts">

import type {AuthFormField} from "#ui/components/AuthForm.vue";
import {z} from 'zod'

const orm = inject('orm');

const schema = z.object({
  email: z.string().email(),
  password: z.string().nonempty(),
})
const fields = ref<AuthFormField[]>([
  { name: 'email', type: 'text',  label: 'Email' },
  { name: 'password', type: 'password', label: 'Password' }
]);

const view = reactive({
  loading: false,
  error: null,
});
const submit = async (evt: FormSubmitEvent<Schema>) => {
  view.loading = true;
  view.error = null;
  try {
    const result = await orm.login(evt.data.email, evt.data.password);
    if (result.error) {
      view.error = result.error;
    } else {
      navigateTo('/tests');
    }
  } catch (e) {
    console.error(e);
  } finally {
    view.loading = false;
  }
}
</script>

<template>
  <u-container class="flex items-center justify-center h-screen flex-col">
    <u-card >
      <u-auth-form :title="'Login'" :fields="fields"
                   :loading="view.loading"
                   icon="i-mdi-fingerprint"
                   :schema="schema"
                   :submit="{label: 'Log in', variant: 'subtle', icon: 'i-mdi-login'}"
                   description="Welcome to JSAlchemy demo application"
                   @submit="submit">
        <template #footer>
          <p>Don't have an account?
            <u-button variant="link" icon="i-mdi-account-plus" to="/register">
              Register here
            </u-button>
          </p>
          <p class="mt-10">
            This is a local instance of your application.
          </p>
          <p>
            By logginng in you're not sending information anywehere else.
          </p>
        </template>
        <template #validation>
          <u-alert v-if="view.error" color="error" title="Login denied"
                   :description="view.error" icon="i-mdi-alert" variant="subtle"/>
        </template>
      </u-auth-form>
    </u-card>
  </u-container>
</template>

<style scoped></style>
