import Button from '@/components/ui/Button'
import Card from '@/components/ui/Card'
import Table from '@/components/ui/Table'
import Avatar from '@/components/ui/Avatar'
import {
    useReactTable,
    getCoreRowModel,
    flexRender,
    createColumnHelper,
} from '@tanstack/react-table'
import { FiPackage } from 'react-icons/fi'
import { useNavigate } from 'react-router-dom'

type Product = {
    id: string
    name: string
    img: string
    sold: number
}

type Job = {
    title: string
    pay: number
    description: string
    status: string
    date: string
    jobtype: string
    jobtime: string
    shift: string
    reqskills: string[]
    domain: string
    totalapplicants: number
}

type JobProps = {
    data?: Job[]
    className?: string
}

type TopProductProps = {
    data?: Product[]
    className?: string
}

const { Tr, Td, TBody, THead, Th } = Table

const ProductColumn = ({ row }: { row: Product }) => {
    const avatar = row.img ? (
        <Avatar src={row.img} />
    ) : (
        <Avatar icon={<FiPackage />} />
    )

    return (
        <div className="flex items-center gap-2">
            {/* {avatar} */}
            <span className="font-semibold">{row.name}</span>
        </div>
    )
}

const columnHelper = createColumnHelper<Job>()

const columns = [
    columnHelper.accessor('title', {
        header: 'Job',
        // cell: (props) => {
        //     const row = props.row.original
        //     return <ProductColumn row={row} />
        // },
    }),
    columnHelper.accessor('totalapplicants', {
        header: 'Applicants',
    }),
]

const Job = ({ data = [], className }: JobProps) => {
    const navigate = useNavigate()

    const table = useReactTable({
        data,
        columns,
        getCoreRowModel: getCoreRowModel(),
    })

    const onNavigate = () => {
        navigate('/app/jobs')
    }

    return (
        <Card className={className}>
            <div className="flex items-center justify-between mb-4">
                <h4>Jobs</h4>
                <Button size="sm" onClick={onNavigate}>View Jobs</Button>
            </div>
            <Table>
                <THead>
                    {table.getHeaderGroups().map((headerGroup) => (
                        <Tr key={headerGroup.id}>
                            {headerGroup.headers.map((header) => {
                                return (
                                    <Th
                                        key={header.id}
                                        colSpan={header.colSpan}
                                    >
                                        {flexRender(
                                            header.column.columnDef.header,
                                            header.getContext()
                                        )}
                                    </Th>
                                )
                            })}
                        </Tr>
                    ))}
                </THead>
                <TBody>
                    {table.getRowModel().rows.map((row) => {
                        return (
                            <Tr key={row.id}>
                                {row.getVisibleCells().map((cell) => {
                                    return (
                                        <Td key={cell.id}>
                                            {flexRender(
                                                cell.column.columnDef.cell,
                                                cell.getContext()
                                            )}
                                        </Td>
                                    )
                                })}
                            </Tr>
                        )
                    })}
                </TBody>
            </Table>
        </Card>
    )
}

export default Job

