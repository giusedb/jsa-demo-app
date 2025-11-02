import { LazyModelModal } from '#components'

const modal = useOverlay().create(LazyModelModal);

export const useModelmodal = () => {
  return function(props) {
    props.modal = modal;
    modal.open(props);
    console.log('open modal ', props.model);
    return modal;
  }
}
