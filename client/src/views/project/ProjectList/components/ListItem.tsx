import Card from '@/components/ui/Card'
import ItemDropdown from './ItemDropdown'
import Members from './Members'
import ProgressionBar from './ProgressionBar'
import { HiOutlineClipboardCheck } from 'react-icons/hi'
import { Link } from 'react-router-dom'
import Badge from '@/components/ui/Badge'

export type ListItemData = {
    id: number
    name: string
    category: string
    desc: string
    attachmentCount: number
    totalTask: number
    completedTask: number
    progression: number
    dayleft: number
    status: string
    member: {
        name: string
        img: string
    }[]
}

export type JobListItemProps = {
    job: {
        id: number;
        title: string;
        description: string;
        status: string;
        jobtype: string;
        jobtime: string;
        required_skills: string; 
        domain: string;
    };
    onJobUpdated?: () => void;
    cardBorder?: boolean;
}

const pay = "$120,000 - $150,000"

type ListItemProps = {
    data: ListItemData
    cardBorder?: boolean
}

const ListItem = ({ data, cardBorder }: ListItemProps) => {
    const { name, totalTask, completedTask, progression, member, category } =
        data

    return (
        <div className="mb-4">
            <Card bordered={cardBorder}>
                <div className="grid gap-x-4 grid-cols-12">
                    <div className="my-1 sm:my-0 col-span-12 sm:col-span-2 md:col-span-3 lg:col-span-3 md:flex md:items-center">
                        <div className="flex flex-col">
                            <h6 className="font-bold">
                                <Link to="/app/project/scrum-board">
                                    {name}
                                </Link>
                            </h6>
                            <span>{pay}</span>
                        </div>
                    </div>
                    <div className="my-1 sm:my-0 col-span-12 sm:col-span-2 md:col-span-2 lg:col-span-2 md:flex md:items-center md:justify-end">
                        <Badge className="mr-4 border border-gray-400" content={'Active'} innerClass="bg-white text-gray-500" />
                        {/* <div className="inline-flex items-center px-2 py-1 border border-gray-300 rounded-full"> */}
                            {/* <HiOutlineClipboardCheck className="text-base" />
                            <span className="ml-1 rtl:mr-1 whitespace-nowrap">
                                {completedTask} / {totalTask}
                            </span> */}
                        {/* </div> */}
                    </div>
                    <div className="my-1 sm:my-0 col-span-12 md:col-span-5 lg:col-span-6 md:flex md:items-center">
                        <ProgressionBar progression={progression} />
                    </div>
                    {/* <div className="my-1 sm:my-0 col-span-12 md:col-span-3 lg:col-span-3 md:flex md:items-center">
                        <Members members={member} />
                    </div> */}
                    <div className="my-1 sm:my-0 col-span-12 sm:col-span-1 flex md:items-center justify-end">
                        <ItemDropdown />
                    </div>
                </div>
            </Card>
        </div>
    )
}

const JobListItem = ({ job, onJobUpdated, cardBorder }: JobListItemProps) => {
    const skills = job.required_skills ? job.required_skills.split(',').map(s => s.trim()) : [];
    const statusBadgeColor = job.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800';
    
    return (
        <div className="mb-4">
            <Card bordered={cardBorder}>
                <div className="grid gap-x-4 grid-cols-12">
                    <div className="my-1 sm:my-0 col-span-12 sm:col-span-2 md:col-span-3 lg:col-span-3 md:flex md:items-center">
                        <div className="flex flex-col">
                            <h6 className="font-bold">
                                <Link to="/access-denied">
                                    {job.title}
                                </Link>
                            </h6>
                            <span className="text-sm text-gray-500">{job.domain}</span>
                        </div>
                    </div>
                    <div className="my-1 sm:my-0 col-span-12 sm:col-span-2 md:col-span-2 lg:col-span-2 md:flex md:items-center md:justify-end">
                        <Badge 
                            className={`mr-4 border border-gray-400 ${statusBadgeColor}`} 
                            content={job.status.charAt(0).toUpperCase() + job.status.slice(1)} 
                            innerClass="bg-white text-gray-500" 
                        />
                        {/* <div className="text-xs text-gray-500">
                            {job.jobtype} • {job.jobtime}
                        </div> */}
                    </div>
                    <div className="my-1 sm:my-0 col-span-12 md:col-span-5 lg:col-span-6 md:flex md:items-center">
                        <div className="flex flex-wrap gap-1">
                            {skills.slice(0, 3).map((skill, index) => (
                                <div key={index} className="inline-flex items-center px-2 py-1 border border-gray-300 rounded-full text-xs">
                                    <span className="whitespace-nowrap">{skill}</span>
                                </div>
                            ))}
                            {skills.length > 3 && (
                                <div key="more" className="inline-flex items-center px-2 py-1 border border-gray-300 rounded-full text-xs">
                                    <span>+{skills.length - 3} more</span>
                                </div>
                            )}
                        </div>
                    </div>
                    <div className="my-1 sm:my-0 col-span-12 sm:col-span-1 flex md:items-center justify-end">
                        <ItemDropdown job={job} onJobUpdated={onJobUpdated} />
                    </div>
                </div>
            </Card>
        </div>
    )
}

export { JobListItem }
export default ListItem
