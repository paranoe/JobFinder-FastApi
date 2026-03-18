import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { PublicVacanciesPage } from '../pages/public/PublicVacanciesPage'
import { LoginPage } from '../pages/auth/LoginPage'
import { RegisterPage } from '../pages/auth/RegisterPage'
import { ApplicantPage } from '../pages/applicant/ApplicantPage'
import { EmployerPage } from '../pages/employer/EmployerPage'
import { AdminPage } from '../pages/admin/AdminPage'
import { RequireAuth } from '../shared/auth/RequireAuth'
import { VacancyDetailPage } from '../pages/vacancy/VacancyDetailPage'

const router = createBrowserRouter([
  { path: '/', element: <PublicVacanciesPage /> },
  { path: '/login', element: <LoginPage /> },
  { path: '/register', element: <RegisterPage /> },
  { path: '/vacancies/:vacancyId', element: <VacancyDetailPage /> },
  {
    element: <RequireAuth />,
    children: [
      {
        element: <RequireAuth allowedRoles={['applicant']} />,
        children: [{ path: '/applicant', element: <ApplicantPage /> }],
      },
      {
        element: <RequireAuth allowedRoles={['company']} />,
        children: [{ path: '/employer', element: <EmployerPage /> }],
      },
      {
        element: <RequireAuth allowedRoles={['admin']} />,
        children: [{ path: '/admin', element: <AdminPage /> }],
      },
    ],
  },
])

export const AppRouter = () => <RouterProvider router={router} />
