import Dialog from '@/components/ui/Dialog'
import NewProjectForm from './NewProjectForm'
import {
    toggleNewProjectDialog,
    useAppDispatch,
    useAppSelector,
} from '../store'

type NewProjectDialogProps = {
    onJobUpdated?: () => void;
}

const NewProjectDialog = ({ onJobUpdated }: NewProjectDialogProps) => {
    const dispatch = useAppDispatch()

    const newProjectDialog = useAppSelector(
        (state) => state.projectList.data.newProjectDialog
    )

    const onDialogClose = () => {
        dispatch(toggleNewProjectDialog(false))
    }

    return (
        <Dialog
            isOpen={newProjectDialog}
            onClose={onDialogClose}
            onRequestClose={onDialogClose}
        >
            <h4>Post New Job</h4>
            <div >
                <NewProjectForm onJobUpdated={onJobUpdated} />
            </div>
        </Dialog>
    )
}

export default NewProjectDialog
