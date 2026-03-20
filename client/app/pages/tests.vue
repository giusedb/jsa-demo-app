<script lang="ts">
import {defineComponent} from 'vue';

export default defineComponent({
  name: "tests",
  data() {
    const tests = new MainTests();
    const idxTests: Object<string, ITest> = Object.fromEntries(tests.list.map(x => [x.id, x]));
    return {
      tests,
      idxTests
    }
  },
  methods: {
    async runTest(id: string) {
      const test: ITest = this.idxTests[id];
      test.status = 'Not started 🫥';
      test.error = '';
      try {
        let result = test.func();
        if (result.constructor === Promise) {
          result = await result
        }
        if (result) {
          test.status = '❌ Fail';
          if (result.constructor === String) {
            test.error = String(result);
          } else {
            test.error = JSON.stringify(result)
          }
        } else {
          test.status = '✅ Passed'
        }
      } catch (e) {
        test.status = '⚡️ Error';
        test.error = e.message || ('' + e);
        console.error(e);
      }
    },
    async runAll() {
      for (let test of this.tests.list) {
        test.status = 'Not started 🫥';
        test.error = '';
      }
      for (let test of this.tests.list) {
        await this.runTest(test.id);
      }
    }
  }
})
</script>

<template>
<u-card class="w-full">
  <template #header>
    <div class="flex justify-between">
      <h2 class="border-b-1">Testing all Orm parts</h2>
      <u-button label="Run all tests"
                @click="runAll"/>
    </div>
    <p>Below a list of tests to run against the functionalities</p>
  </template>
  <template #default>
    <u-page-list>
      <u-page-card v-for="test in tests.list" :key="test.id"
                   :title="test.id"
                   class="flex justify-between"
                   variant="ghost">
        <div class="flex justify-between border-b-blue-700">
          <div>
            {{ test.status }}
          </div>
          <div class="text-error">
            {{ test.error}}
          </div>
          <div>
            <u-button label="Run " icon="i-ic-twotone-directions-run"
                      variant="subtle"
                      color="secondary"
                      @click="runTest(test.id)"/>
          </div>
        </div>
      </u-page-card>
    </u-page-list>
    <u-page-list>

    </u-page-list>
  </template>
</u-card>
</template>

<style scoped>

</style>