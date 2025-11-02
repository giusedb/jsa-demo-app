<script setup lang="ts">
import {z} from 'zod'

const registerField = [
  { name: 'email', type: 'text',  label: 'Email' },
  { name: 'first_name', type: 'text', label: 'First Name'},
  { name: 'last_name', type: 'text', label: 'Last Name'},
  { name: 'password', type: 'password', label: 'Password' },
  { name: 'confirmPassword', type: 'password', label: 'Confirm Password' },
];

const schema: z.ZodType = z.object({
  email: z.string().email(),
  first_name: z.string().min(2),
  last_name: z.string().min(2),
  password: z.string().min(8),
  confirmPassword: z.string().min(8),
});

const view = reactive({
  user: {
    first_name: 'Mario'
  },
  error: null,
  loading: false,
})

async function register(evt: FormSubmitEvent<Schema>) {
  try {
    view.error = null;
    view.loading = true;
    const payload = Object.assign({}, evt.data);
    delete payload.confirmPassword;
    try {
      await $fetch('/auth/register', {
        method: 'POST',
        body: payload
      })
    } catch (e) {
      view.error = e.data.error;
    }
    console.info(payload);
  } catch (e) {
    view.error = e;
    console.error(e)
  } finally {
    view.loading = false;
  }
}
</script>

<template>
  <u-container class="flex items-center justify-center h-screen flex-col">
    <u-card>
      <u-auth-form title="Register" :fields="registerField"
                   icon="i-mdi-account-plus"
                   :schema="schema"
                   description="Welcome to JSAlchemy demo application"
                   :loading="view.loading"
                   :submit="{label: 'Register', variant: 'subtle', icon: 'i-mdi-account-plus'}"
                   @submit="register">
        <template #footer>
          <p>Already have an account?
            <u-button variant="link" icon="i-mdi-login" to="/login">
              Login here
            </u-button>
          </p>
          <p class="mt-10">
            This is a local instance of your application.
          </p>
          <p>
            By registering you're not sending information anywehere else.
          </p>
        </template>
        <template #validation>
          <u-alert v-if="view.error" color="error" title="Registration denied"
                   :description="view.error" icon="i-mdi-alert" variant="subtle"/>
        </template>
      </u-auth-form>
    </u-card>
  </u-container>
</template>

<style scoped></style>
