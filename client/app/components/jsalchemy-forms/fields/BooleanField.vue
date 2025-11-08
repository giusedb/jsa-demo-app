<script>
import WidgetBase from "@/jsalchemy-forms/fields/WidgetBase.vue";

export default {
  extends: WidgetBase,
  methods: {
    set(val) {
      this.val = val;
    }
  }
}
</script>

<template>
  <div v-if="editable" class="btn-group" role="group">
    <template v-for="v in [[true, 'yes'], [null, '-'], [false, 'No']]" :key="v[0]">
      <button type="button" class="btn btn-outline-primary"
              @click="set(v[0])"
              :class="val === v[0] ? 'active' : ''">
        {{ v[1]}}
      </button>
    </template>
  </div>
  <div v-else class="text-secondary">
    <span v-if="val === false">
      No
    </span>
    <span v-else-if="val === null">
      -
    </span>
    <span v-else-if="val === true">
      Yes
    </span>
    <span v-else> ... </span>
  </div>

</template>

<style scoped>

</style>
