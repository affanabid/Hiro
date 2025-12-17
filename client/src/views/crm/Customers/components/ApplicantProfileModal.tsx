import { useState, useEffect } from 'react'
import Dialog from '@/components/ui/Dialog'
import Button from '@/components/ui/Button'
import Badge from '@/components/ui/Badge'
import Spinner from '@/components/ui/Spinner'
import { HiRefresh, HiX, HiChevronDown, HiChevronRight } from 'react-icons/hi'
import ApiService from '@/services/ApiService'

interface Skill {
    name: string
    category: string
    proficiency?: string | null
}

interface Experience {
    company: string
    title: string
    duration: string
    description: string
}

interface Education {
    institution: string
    degree: string
    field: string | null
    year: string
}

interface Certification {
    name: string
    issuer: string
    year?: string | null
}

interface ApplicantProfile {
    id: number
    applicant: number
    applicant_name: string
    applicant_email: string
    summary: string
    skills: Skill[]
    experience: Experience[]
    education: Education[]
    certifications: Certification[]
    total_experience_years?: number | null
    extracted_at: string
    extraction_source: string
    github_url?: string | null
    github_username?: string | null
    github_insights?: {
        username: string
        repo_count: number
        top_languages: { name: string; percent: number }[]
        repos: {
            name_with_owner: string
            pushed_at?: string | null
            updated_at?: string | null
            stars: number
            forks: number
            languages: { name: string; percent: number }[]
            stack_labels: string[]
        }[]
    } | null
}

interface ApplicantProfileModalProps {
    applicantId: number | null
    applicantName: string
    isOpen: boolean
    onClose: () => void
}

const ApplicantProfileModal = ({
    applicantId,
    applicantName,
    isOpen,
    onClose
}: ApplicantProfileModalProps) => {
    const [profile, setProfile] = useState<ApplicantProfile | null>(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [skillsExpanded, setSkillsExpanded] = useState(false)
    const [githubExpanded, setGithubExpanded] = useState(false)

    const fetchProfile = async () => {
        if (!applicantId) return

        setLoading(true)
        setError(null)

        try {
            const response = await ApiService.fetchData({
                url: `/applicants/${applicantId}/profile/`,
                method: 'get'
            })
            setProfile(response.data)
        } catch (err: any) {
            setError(err.response?.data?.error || 'Failed to load profile')
            console.error('Profile fetch error:', err)
        } finally {
            setLoading(false)
        }
    }

    const refreshProfile = async () => {
        if (!applicantId) return

        setLoading(true)
        setError(null)

        try {
            const response = await ApiService.fetchData({
                url: `/applicants/${applicantId}/profile/refresh/`,
                method: 'post'
            })
            setProfile(response.data)
        } catch (err: any) {
            setError(err.response?.data?.error || 'Failed to refresh profile')
            console.error('Profile refresh error:', err)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        if (isOpen && applicantId) {
            fetchProfile()
        }
        // Reset state when modal closes
        if (!isOpen) {
            setProfile(null)
            setError(null)
        }
    }, [isOpen, applicantId])

    // Group skills by category
    const skillsByCategory = profile?.skills.reduce((acc, skill) => {
        if (!acc[skill.category]) acc[skill.category] = []
        acc[skill.category].push(skill)
        return acc
    }, {} as Record<string, Skill[]>) || {}

    const github = profile?.github_insights

    return (
        <Dialog
            isOpen={isOpen}
            onClose={onClose}
            width={900}
            closable={false}
            overlayClassName="bg-black/80"
        >
            <div className="bg-white dark:bg-gray-900 -m-6 p-6 rounded-lg">
                <div className="flex items-center justify-between mb-6">
                    <div>
                        <h4 className="text-xl font-bold">{applicantName}'s Profile</h4>
                        {profile && (
                            <p className="text-sm text-gray-500 mt-1">
                                Extracted from {profile.extraction_source}
                            </p>
                        )}
                    </div>
                    <div className="flex gap-2">
                        <Button
                            size="sm"
                            variant="plain"
                            icon={<HiRefresh />}
                            onClick={refreshProfile}
                            disabled={loading}
                            title="Re-extract profile from resume"
                        >
                            Refresh
                        </Button>
                        <Button
                            size="sm"
                            variant="plain"
                            icon={<HiX />}
                            onClick={onClose}
                        />
                    </div>
                </div>

                {loading && (
                    <div className="flex flex-col items-center justify-center py-16">
                        <Spinner size={40} />
                        <p className="text-gray-500 mt-4">
                            {profile ? 'Refreshing profile...' : 'Extracting insights from resume...'}
                        </p>
                        <p className="text-sm text-gray-400 mt-1">This may take 10-30 seconds</p>
                    </div>
                )}

                {error && !loading && (
                    <div className="bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 p-4 rounded mb-4">
                        <p className="font-semibold">Error</p>
                        <p className="text-sm mt-1">{error}</p>
                    </div>
                )}

                {!loading && profile && (
                    <div className="space-y-6 max-h-[600px] overflow-y-auto pr-2">

                        {/* Skills - Collapsible */}
                        {profile.skills.length > 0 && (
                            <div className="border border-gray-200 dark:border-gray-700 rounded-lg">
                                <button
                                    onClick={() => setSkillsExpanded(!skillsExpanded)}
                                    className="w-full flex items-center justify-between p-4 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                                >
                                    <div className="flex items-center gap-2">
                                        {skillsExpanded ? <HiChevronDown className="text-lg" /> : <HiChevronRight className="text-lg" />}
                                        <h5 className="font-semibold flex items-center gap-2">
                                            <span>💡 Skills</span>
                                            <span className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300">
                                                {profile.skills.length}
                                            </span>
                                        </h5>
                                    </div>
                                </button>
                                {skillsExpanded && (
                                    <div className="px-4 pb-4 space-y-4 border-t border-gray-200 dark:border-gray-700 pt-4">
                                        {Object.entries(skillsByCategory).map(([category, skills]) => (
                                            <div key={category}>
                                                <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">
                                                    {category}
                                                </p>
                                                <div className="flex flex-wrap gap-2">
                                                    {skills.map((skill, idx) => (
                                                        <span
                                                            key={idx}
                                                            className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300"
                                                        >
                                                            {skill.name}
                                                        </span>
                                                    ))}
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        )}

                        {/* Experience */}
                        {profile.experience.length > 0 && (
                            <div>
                                <h5 className="font-semibold mb-3 flex items-center gap-2">
                                    <span>💼 Work Experience</span>
                                    <span className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300">
                                        {profile.experience.length}
                                    </span>
                                </h5>
                                <div className="space-y-4">
                                    {profile.experience.map((exp, idx) => (
                                        <div
                                            key={idx}
                                            className="border-l-4 border-blue-500 dark:border-blue-400 pl-4 py-2"
                                        >
                                            <p className="font-semibold text-gray-900 dark:text-gray-100">
                                                {exp.title}
                                            </p>
                                            <p className="text-sm text-gray-600 dark:text-gray-400 font-medium">
                                                {exp.company}
                                            </p>
                                            <p className="text-sm text-gray-500 dark:text-gray-500">
                                                {exp.duration}
                                            </p>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Education */}

                        {/* GitHub Insights */}
                        {github && github.repo_count > 0 && (
                            <div className="border border-gray-200 dark:border-gray-700 rounded-lg">
                                <button
                                    type="button"
                                    onClick={() => setGithubExpanded(!githubExpanded)}
                                    className="w-full flex items-center justify-between p-4 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                                >
                                    <div className="flex items-center gap-2">
                                        {githubExpanded ? <HiChevronDown className="text-lg" /> : <HiChevronRight className="text-lg" />}
                                        <h5 className="font-semibold flex items-center gap-2">
                                            <span>🐙 GitHub Insights</span>
                                            <span className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300">
                                                {github.repo_count} repos
                                            </span>
                                        </h5>
                                    </div>
                                </button>
                                {githubExpanded && (
                                    <div className="px-4 pb-4 space-y-4 border-t border-gray-200 dark:border-gray-700 pt-4">
                                        <div className="flex items-center justify-between">
                                            <div className="space-y-1">
                                                <p className="text-sm text-gray-600 dark:text-gray-400">
                                                    GitHub user:{' '}
                                                    <span className="font-medium text-gray-900 dark:text-gray-100">
                                                        {profile.github_username || github.username}
                                                    </span>
                                                </p>
                                                {profile.github_url && (
                                                    <a
                                                        href={profile.github_url}
                                                        target="_blank"
                                                        rel="noreferrer"
                                                        className="text-xs text-blue-600 dark:text-blue-400 underline"
                                                    >
                                                        View GitHub profile
                                                    </a>
                                                )}
                                            </div>
                                        </div>

                                        {github.top_languages && github.top_languages.length > 0 && (
                                            <div>
                                                <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">
                                                    Top Languages
                                                </p>
                                                <div className="flex flex-wrap gap-2">
                                                    {github.top_languages.map((lang, idx) => (
                                                        <span
                                                            key={idx}
                                                            className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300"
                                                        >
                                                            {lang.name} ({lang.percent}%)
                                                        </span>
                                                    ))}
                                                </div>
                                            </div>
                                        )}

                                        <div>
                                            <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">
                                                Recent Repositories
                                            </p>
                                            <div className="space-y-2 max-h-64 overflow-y-auto pr-1">
                                                {github.repos.slice(0, 10).map((repo, idx) => (
                                                    <div
                                                        key={idx}
                                                        className="flex flex-col gap-1 border border-gray-200 dark:border-gray-700 rounded p-2"
                                                    >
                                                        <div className="flex items-center justify-between">
                                                            <span className="font-medium text-sm text-gray-900 dark:text-gray-100">
                                                                {repo.name_with_owner}
                                                            </span>
                                                            {(repo.stars > 0 || repo.forks > 0) && (
                                                                <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
                                                                    {repo.stars > 0 && <span>★ {repo.stars}</span>}
                                                                    {repo.forks > 0 && <span>⑂ {repo.forks}</span>}
                                                                </div>
                                                            )}
                                                        </div>
                                                        {repo.languages && repo.languages.length > 0 && (
                                                            <div className="flex flex-wrap gap-1 mt-1">
                                                                {repo.languages.map((lang, i) => (
                                                                    <span
                                                                        key={i}
                                                                        className="inline-flex items-center px-2 py-0.5 rounded text-xs bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300"
                                                                    >
                                                                        {lang.name} ({lang.percent}%)
                                                                    </span>
                                                                ))}
                                                            </div>
                                                        )}
                                                        {repo.stack_labels && repo.stack_labels.length > 0 && (
                                                            <div className="flex flex-wrap gap-1 mt-1">
                                                                {repo.stack_labels.map((label, i) => (
                                                                    <span
                                                                        key={i}
                                                                        className="inline-flex items-center px-2 py-0.5 rounded text-xs bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300"
                                                                    >
                                                                        {label}
                                                                    </span>
                                                                ))}
                                                            </div>
                                                        )}
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    </div>
                                )}
                            </div>
                        )}

                        {/* Certifications */}
                        {profile.education.length > 0 && (
                            <div>
                                <h5 className="font-semibold mb-3 flex items-center gap-2">
                                    <span>🎓 Education</span>
                                    <span className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300">
                                        {profile.education.length}
                                    </span>
                                </h5>
                                <div className="space-y-3">
                                    {profile.education.map((edu, idx) => (
                                        <div key={idx} className="bg-gray-50 dark:bg-gray-800/50 p-3 rounded">
                                            <p className="font-semibold text-gray-900 dark:text-gray-100">
                                                {edu.degree}{edu.field && ` in ${edu.field}`}
                                            </p>
                                            <p className="text-sm text-gray-600 dark:text-gray-400">
                                                {edu.institution}
                                            </p>
                                            <p className="text-sm text-gray-500 dark:text-gray-500">
                                                {edu.year}
                                            </p>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Certifications */}
                        {profile.certifications.length > 0 && (
                            <div>
                                <h5 className="font-semibold mb-3 flex items-center gap-2">
                                    <span>🏆 Certifications</span>
                                    <span className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300">
                                        {profile.certifications.length}
                                    </span>
                                </h5>
                                <div className="space-y-2">
                                    {profile.certifications.map((cert, idx) => (
                                        <div
                                            key={idx}
                                            className="flex justify-between items-start bg-gray-50 dark:bg-gray-800/50 p-3 rounded"
                                        >
                                            <span className="font-medium text-gray-900 dark:text-gray-100">
                                                {cert.name}
                                            </span>
                                            <span className="text-sm text-gray-500 dark:text-gray-400 text-right">
                                                {cert.issuer}
                                                {cert.year && ` • ${cert.year}`}
                                            </span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Footer */}
                        <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
                            <p className="text-xs text-gray-400 dark:text-gray-500">
                                Extracted on: {new Date(profile.extracted_at).toLocaleString()}
                            </p>
                        </div>
                    </div>
                )}

                {!loading && !profile && !error && (
                    <div className="text-center py-12 text-gray-500">
                        <p>No profile data available</p>
                    </div>
                )}
            </div>
        </Dialog>
    )
}

export default ApplicantProfileModal
