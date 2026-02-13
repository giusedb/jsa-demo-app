
export default defineAppConfig({
  ui: {
    prose: {
      card: {
        h2: {
          slots: {
            base: 'border-b-1'
          }
        }
      },
      h1: {
        slots: {
          base: 'text-4xl font-bold'
        }
      },
      h2: {
        slots: {
          base: 'text-3xl font-bold'
        }
      },
      h3: {
        slots: {
          base: 'text-2xl font-bold'
        }
      },
      h4: {
        slots: {
          base: 'text-xl font-bold'
        }
      },
      h5: {
        slots: {
          base: 'text-lg font-bold'
        }
      },
      h6: {
        slots: {
          base: 'font-bold'
        }
      },
      p: {
        base: 'leading-7 [&:not(:first-child)]:mt-6'
      }
    }
  }
});