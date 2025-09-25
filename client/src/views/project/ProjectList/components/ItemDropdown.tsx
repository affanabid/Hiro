import Dropdown from '@/components/ui/Dropdown'
import {
    HiOutlineSwitchHorizontal,
    HiOutlineFlag,
    HiOutlineCog,
} from 'react-icons/hi'
import { MdDelete } from "react-icons/md";
import { FaEdit } from "react-icons/fa";
import EllipsisButton from '@/components/shared/EllipsisButton'
import { useState } from 'react'
import { updateJob, deleteJob } from '@/services/JobServices'
import EditJobDialog from './EditJobDialog'

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

type ItemDropdownProps = {
    job?: JobData;
    onJobUpdated?: () => void;
}

const dropdownList = [
    { label: 'Edit', value: 'edit', icon: <FaEdit/> },
    { label: 'Delete', value: 'delete', icon: <MdDelete /> },
    // { label: 'Setting', value: 'projectSetting', icon: <HiOutlineCog /> },
]

const ItemDropdown = ({ job, onJobUpdated }: ItemDropdownProps) => {
    const [editDialogOpen, setEditDialogOpen] = useState(false)

    const handleDropdownSelect = (eventKey: string) => {
        if (!job) return;
        
        switch (eventKey) {
            case 'edit':
                setEditDialogOpen(true)
                break
            case 'delete':
                handleDelete()
                break
        }
    }

    const handleDelete = async () => {
        if (!job) return;
        
        const confirmed = window.confirm(`Are you sure you want to delete "${job.title}"?`)
        if (confirmed) {
            try {
                await deleteJob(job.id)
                onJobUpdated?.()
                // You might want to show a success toast here
            } catch (error) {
                console.error('Failed to delete job:', error)
                // You might want to show an error toast here
            }
        }
    }

    return (
        <>
            <Dropdown 
                placement="bottom-end" 
                renderTitle={<EllipsisButton />}
                onSelect={handleDropdownSelect}
            >
                {dropdownList.map((item) => (
                    <Dropdown.Item key={item.value} eventKey={item.value}>
                        <span className="text-lg">{item.icon}</span>
                        <span className="ml-2 rtl:mr-2">{item.label}</span>
                    </Dropdown.Item>
                ))}
            </Dropdown>
            
            {job && (
                <EditJobDialog 
                    isOpen={editDialogOpen}
                    onClose={() => setEditDialogOpen(false)}
                    job={job}
                    onJobUpdated={onJobUpdated}
                />
            )}
        </>
    )
}

export default ItemDropdown
