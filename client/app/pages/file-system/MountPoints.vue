<script lang="ts">
import {defineComponent} from 'vue'
import { RecordSet } from 'jsalchemy';
import {useModelmodal} from "~/composables/modelmodal";
import {FolderTree} from "#components";

const modelModal = useModelmodal();

export default defineComponent({
  name: "MountPoints",
  inject: ['orm'],
  components: { RecordSet, FolderTree },
  data() {
    return {
      mountPoint: null
    }
  },
  methods: {
    async runFixture() {
      (await this.orm.getModel('MountPoint')).runFixture();
    }
  }
})
</script>

<template>
  <u-card class="w-full">
    <template #header>
      <record-set resource="MountPoint" :sort="['name']">
        <template #default="{ records, total}">
          <div class="flex row justify-between w-full">
            <h3 >Mount points</h3 >
            <div class="button-box">
              <u-popover v-for="mp in records" :key="mp.id" mode="hover">
                <u-button :variant="mp === mountPoint ? 'outline' : 'secondary'"
                          @click="mountPoint = mp"
                          icon="vaadin-harddrive" :label="mp.name"/>
                <template #content>
                  Mount point options: {{ mp.options }}
                </template>
              </u-popover>
            </div>
            <u-button icon="vaadin-refresh" label="reset" variant="subtle" color="error"
                      @click.prevent="runFixture"/>
          </div>
        </template>
      </record-set>
    </template>
    <folder-tree v-if="mountPoint?.root" :folder="mountPoint.root"/>
  </u-card>
</template>

<style scoped>

</style>