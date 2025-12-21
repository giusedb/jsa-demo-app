<script setup lang="ts">

import { RecordSet } from 'jsalchemy';
import ModelForm from "~/components/jsalchemy-forms/ModelForm.vue";
import VueForm from "~/components/jsalchemy-forms/VueForm.vue";

const modalForm = useModelmodal();

const orm: Orm = inject('orm');
const manifacturer = ref(null);
const addManifacturer = () => {
  modalForm({model: 'Manifacturer'})
}

</script>

<template>
  <u-card class="w-full">
    <template #header>
      <h2>Cars and manifacturers</h2>
      <p>This Demo showcases the One to Many relationship between cars and manifacturers</p>
      <p>You can create several manifacturers and assign them to cars</p>
    </template>
    <template #default>
      <div class="w-full">
        <div class="flex justify-between">
          <div>
            <record-set resource="Manifacturer" :filter="{}" :paging="{}">
              <template #default="{ records, loading}">
                <u-button v-for="brand in records" :key="brand.id" :label="brand.name" />
              </template>
            </record-set>
            <model-form model="Manifacturer" :new="true"/>
          </div>
          <div>
            <u-button label="Add Manifacturer" icon="i-mdi-plus" @click="addManifacturer"/>
          </div>
        </div>
      </div>
    </template>
  </u-card>
</template>

<style scoped></style>
