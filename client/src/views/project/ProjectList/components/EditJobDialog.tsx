import Dialog from '@/components/ui/Dialog'
import EditJobForm from './EditJobForm'

type JobData = {
    id: number;
    title: string;
    description: string;
    status: string;
    jobtype: string;
    jobtime: string;
    required_skills: string; 
    domain: string;
}

type EditJobDialogProps = {
    isOpen: boolean;
    onClose: () => void;
    job: JobData;
    onJobUpdated?: () => void;
}

const EditJobDialog = ({ isOpen, onClose, job, onJobUpdated }: EditJobDialogProps) => {
    return (
        <Dialog
            isOpen={isOpen}
            onClose={onClose}
            onRequestClose={onClose}
        >
            <h4>Edit Job</h4>
            <div>
                <EditJobForm 
                    job={job} 
                    onClose={onClose}
                    onJobUpdated={onJobUpdated}
                />
            </div>
        </Dialog>
    )
}

export default EditJobDialog
