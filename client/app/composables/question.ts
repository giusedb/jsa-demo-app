import { LazyModalQuestion } from '#components'

interface iButton {
    label: string,
    result?: string,
    icon?: string,
}

export const useQuestion = () => {
  return function(title: String, message: String, buttons?: Array<iButton | string>) {
      if (buttons === undefined) {
          buttons = [{label: 'OK', icon: 'i-line-md-confirm', result: 'ok'}]
      }
      buttons = buttons.map(button => {
          if (typeof button === 'string') {
              return {label: button, result: button, icon: ''};
          }
          return button;
      });

      return new Promise((resolve, reject) => {
          const modal = useOverlay().create(LazyModalQuestion);
          modal.open({title, message, buttons, result: (ret) => {
              modal.close();
              resolve(ret);
          }});
      })
  }
}
