import { useCallback } from 'react'
import Card from '@/components/ui/Card'
import Button from '@/components/ui/Button'
import Table from '@/components/ui/Table'
import Badge from '@/components/ui/Badge'
import useThemeClass from '@/utils/hooks/useThemeClass'
import {
    useReactTable,
    getCoreRowModel,
    flexRender,
    createColumnHelper,
} from '@tanstack/react-table'
import { useNavigate } from 'react-router-dom'
import { NumericFormat } from 'react-number-format'
import dayjs from 'dayjs'

type Order = {
    id: string
    date: number
    customer: string
    status: number
    paymentMehod: string
    paymentIdendifier: string
    totalAmount: number
}

type Applicant = {
    name: string
    email: string
    status: string
    telephone: string
    job: string
    score: number
}

type LatestApplicantProps = {
    data?: Applicant[]
    className?: string
}

type OrderColumnPros = {
    row: Applicant
}

const { Tr, Td, TBody, THead, Th } = Table

// const orderStatusColor: Record<
//     number,
//     {
//         label: string
//         dotClass: string
//         textClass: string
//     }
// > = {
//     0: {
//         label: 'Paid',
//         dotClass: 'bg-emerald-500',
//         textClass: 'text-emerald-500',
//     },
//     1: {
//         label: 'Pending',
//         dotClass: 'bg-amber-500',
//         textClass: 'text-amber-500',
//     },
//     2: { label: 'Failed', dotClass: 'bg-red-500', textClass: 'text-red-500' },
// }

// const OrderColumn = ({ row }: OrderColumnPros) => {
//     const { textTheme } = useThemeClass()
//     const navigate = useNavigate()

//     const onView = useCallback(() => {
//         navigate(`/app/sales/order-details/${row.id}`)
//     }, [navigate, row])

//     return (
//         <span
//             className={` select-none font-semibold`}
//             // onClick={onView} disable click
//         >
//             #{row.id}
//         </span>
//     )
// }

const columnHelper = createColumnHelper<Applicant>()

const columns = [
    columnHelper.accessor('name', {
        header: 'Name',
    }),
    columnHelper.accessor('status', {
        header: 'Status',
    }),
    columnHelper.accessor('email', {
        header: 'Email',
    }),
    // columnHelper.accessor('date', {
    //     header: 'Date',
    //     cell: (props) => {
    //         const row = props.row.original
    //         return <span>{dayjs.unix(row.date).format('DD/MM/YYYY')}</span>
    //     },
    // }),
    
    columnHelper.accessor('job', {
        header: 'Job',
    }),
    columnHelper.accessor('score', {
        header: 'Score',
    }),
]

const Applicants = ({ data = [], className }: LatestApplicantProps) => {
    const navigate = useNavigate()

    const table = useReactTable({
        data,
        columns,
        getCoreRowModel: getCoreRowModel(),
    })

    const onNavigate = () => {
        navigate('/app/applicants')
    }

    return (
        <Card className={className}>
            <div className="flex items-center justify-between mb-6">
                <h4>Applicants</h4>
                <Button size="sm" onClick={onNavigate}>View Applicants</Button>
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

export default Applicants
