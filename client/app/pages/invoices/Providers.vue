<script lang="ts">
import {defineComponent} from 'vue'
import {RecordSet} from "../../../../libs/jsa-client";

const defaulItem = () => {
  return {
    name: '',
    address: '',
  }
}

export default defineComponent({
  name: "Providers",
  components: {RecordSet},
  inject: { orm },
  data() {
    return {
      selected: defaulItem(),
    }
  },
  computed: {
    isNew() {
      return !this.selected.id;
    }
  },
  methods: {
    async add() {
      const Provider = await this.orm.getModel('Provider');
      const provider = new Provider(this.selected);
      await provider.$save();
      this.selected = defaulItem();
    },
    select(item) {
      this.selected = item;
    },
    update() {
      this.selected.$save();
    },
    deleteProvider() {
      this.selected.$delete();
    }
  }
})
</script>

<template>
  <u-card class="w-full">
    <template #header>
      <h3>Provider list</h3>
      <p>
        Under the invoices menu, the demo showcases a One to Many relation among two
        DB entities and shows to interact with data without any definition of endpoint
        interaction.
      </p>
    </template>
    <div class="border-b-1 border-b-primary-200 w-full">
      <u-form class="mb-2 w-full">
        <u-form-field label="Name" name="name" class="w-full">
          <u-input v-model="selected.name" class="w-full"/>
        </u-form-field>
        <u-form-field label="Address" name="address" class="w-full">
          <u-input v-model="selected.address" class="w-full"/>
        </u-form-field>
        <template v-if="isNew">
          <u-button label="Add" @click="add" class="mt-2"/>
        </template>
        <template v-else>
          <u-button label="delete" @click="deleteProvider" class="mt-2 me-2" variant="outline" color="error"/>
          <u-button label="update" @click="update" class="mt-2" variant="outline" color="secondary"/>
        </template>
      </u-form>
    </div>
    <h3>Provider list</h3>
    <div class="w-full grid grid-cols-3">
      <record-set resource="Provider">
        <template #default="{ records }">

          <u-page-card v-for="provider in records" :key="provider.id"
                       class="m-1" orientation="horizontal"
                       :variant="selected === provider ? 'solid' : 'subtle'"
                       spotlight
                       spotlight-color="warning" @click="select(provider)">
            <template #header>
              <u-badge >{{ provider.id }}</u-badge>
              <h4 class="flex row justify-between w-full">
                <div>
                  {{ provider.name }}
                </div>
              </h4>
              <p>
                {{ provider.address }}
              </p>
            </template>
          </u-page-card>
          {{ records.map(x => x.id) }}
        </template>
      </record-set>
    </div>
  </u-card>
</template>

<style scoped>

</style>