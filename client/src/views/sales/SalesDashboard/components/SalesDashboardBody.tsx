import { useEffect } from 'react'
import Loading from '@/components/shared/Loading'
import Statistic from './Statistic'
import SalesReport from './SalesReport'
import SalesByCategories from './SalesByCategories'
import LatestOrder from './ApplicantsDashboard'
import Job from './JobDashboard'
import { getSalesDashboardData, useAppSelector } from '../store'
import { useAppDispatch } from '@/store'
import Applicants from './ApplicantsDashboard'

const SalesDashboardBody = () => {
    const dispatch = useAppDispatch()

    const dashboardData = useAppSelector(
        (state) => state.salesDashboard.data.dashboardData
    )

    const loading = useAppSelector((state) => state.salesDashboard.data.loading)

    useEffect(() => {
        fetchData()
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    const fetchData = () => {
        dispatch(getSalesDashboardData())
    }

    return (
        <Loading loading={loading}>
            <Statistic data={dashboardData?.statisticData} />
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
                <SalesReport
                    data={dashboardData?.salesReportData}
                    className="col-span-2"
                />
                <SalesByCategories
                    data={dashboardData?.recruitmentByCategoriesData}
                />
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
                <Applicants
                    data={dashboardData?.latestApplicantData}
                    className="lg:col-span-2"
                />
                <Job data={dashboardData?.jobData} />
            </div>
        </Loading>
    )
}

export default SalesDashboardBody
