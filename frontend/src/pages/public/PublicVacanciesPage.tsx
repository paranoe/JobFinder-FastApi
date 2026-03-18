import { useEffect, useMemo, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link, useNavigate } from 'react-router-dom'
import { http } from '../../shared/api/http'
import { authSession, initializeSession } from '../../shared/auth/session'
import './public.css'

type Vacancy = {
  id: number
  title: string
  description: string
  salary_min: number
  salary_max: number
  company_name: string
  city_name: string
  profession_name: string
}

const featuredCompanies = [
  {
    name: 'Yandex',
    jobs: '1 240 вакансий',
    description: 'Поиск, карты, облака, AI и сервисы для миллионов пользователей.',
    image:
      'https://images.unsplash.com/photo-1521791136064-7986c2920216?auto=format&fit=crop&w=900&q=80',
  },
  {
    name: 'T-Bank',
    jobs: '860 вакансий',
    description: 'FinTech-продукты, мобильные приложения и data-driven команды.',
    image:
      'https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=900&q=80',
  },
  {
    name: 'VK',
    jobs: '510 вакансий',
    description: 'Социальные платформы, контент и инфраструктура высокого масштаба.',
    image:
      'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=900&q=80',
  },
]

const quickDirections = [
  { title: 'IT и разработка', subtitle: 'Frontend, Backend, DevOps, QA', count: '68 000 вакансий' },
  { title: 'Продажи', subtitle: 'B2B, Retail, Customer Success', count: '41 000 вакансий' },
  { title: 'Маркетинг', subtitle: 'SMM, Performance, Brand', count: '19 000 вакансий' },
  { title: 'Финансы', subtitle: 'Бухгалтерия, аналитика, аудит', count: '15 000 вакансий' },
]

const platformStats = [
  { label: 'Активных вакансий', value: '120 000+' },
  { label: 'Проверенных компаний', value: '7 500+' },
  { label: 'Откликов в сутки', value: '25 000+' },
  { label: 'Средний ответ HR', value: 'до 48 часов' },
]

const benefits = [
  {
    title: 'Умный подбор вакансий',
    text: 'Подсказки по навыкам и персональная выдача вакансий под ваш профиль.',
  },
  {
    title: 'Проверенные работодатели',
    text: 'Компании с прозрачными условиями и актуальными карточками вакансий.',
  },
  {
    title: 'Быстрый отклик',
    text: 'Откликайтесь в пару кликов и следите за статусом в личном кабинете.',
  },
]

const roleRoute = (role: string | null) => {
  if (role === 'company') return '/employer'
  if (role === 'admin') return '/admin'
  return '/applicant'
}

const fetchVacancies = async (search: string): Promise<Vacancy[]> => {
  const { data } = await http.get('/public/vacancies', {
    params: { search: search || undefined, limit: 20, skip: 0 },
  })
  return data
}

export const PublicVacanciesPage = () => {
  const navigate = useNavigate()
  const [searchInput, setSearchInput] = useState('')
  const [search, setSearch] = useState('')
  const [info, setInfo] = useState('Найдите вакансию и откликайтесь после входа в аккаунт.')
  const [favorites, setFavorites] = useState<number[]>([])
  const [checkingSession, setCheckingSession] = useState(true)

  useEffect(() => {
    const bootstrap = async () => {
      const hasSession = await initializeSession()
      if (hasSession) {
        navigate(roleRoute(authSession.getRole()), { replace: true })
        return
      }

      setCheckingSession(false)
    }

    void bootstrap()
  }, [navigate])

  const vacanciesQuery = useQuery({
    queryKey: ['public-vacancies', search],
    queryFn: () => fetchVacancies(search),
    retry: 1,
  })

  const hasVacancies = useMemo(() => (vacanciesQuery.data?.length ?? 0) > 0, [vacanciesQuery.data])

  const goToLogin = (message: string) => {
    setInfo(message)
    navigate('/login')
  }

  const toggleFavorite = (id: number, title: string) => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      goToLogin('Добавление в избранное доступно только после входа в аккаунт.')
      return
    }

    setFavorites((prev) => {
      const hasFavorite = prev.includes(id)
      if (hasFavorite) {
        setInfo(`Вакансия «${title}» удалена из избранного.`)
        return prev.filter((item) => item !== id)
      }

      setInfo(`Вакансия «${title}» добавлена в избранное.`)
      return [...prev, id]
    })
  }

  if (checkingSession) {
    return <main style={{ padding: 24 }}>Проверяем сессию...</main>
  }

  return (
    <div className="home-page">
      <header className="topbar">
        <div className="logo">jobfinder</div>
        <nav>
          <a href="#vacancies">Вакансии</a>
          <a href="#companies">Компании</a>
          <a href="#benefits">Преимущества</a>
        </nav>
        <div className="topbar-actions">
          <Link to="/login" className="login-link">Войти</Link>
          <button className="primary-btn" onClick={() => goToLogin('Для размещения вакансии войдите как работодатель.')}>Разместить вакансию</button>
        </div>
      </header>

      <section className="hero">
        <div className="hero-left">
          <h1>Найди работу мечты в пару кликов</h1>
          <p>Современный поиск вакансий, проверенные компании и быстрые отклики в одном месте.</p>
          <div className="hero-tags">
            {['Удалёнка', 'Без опыта', 'Гибкий график', 'Стажировки'].map((tag) => (
              <button
                key={tag}
                type="button"
                onClick={() => {
                  setSearchInput(tag)
                  setSearch(tag)
                  setInfo(`Применен фильтр: ${tag}.`)
                }}
              >
                {tag}
              </button>
            ))}
          </div>
          <div className="hero-stats">
            {platformStats.map((item) => (
              <article key={item.label}>
                <strong>{item.value}</strong>
                <p>{item.label}</p>
              </article>
            ))}
          </div>
        </div>
        <img
          src="https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&fit=crop&w=1200&q=80"
          alt="Команда на встрече"
          className="hero-image"
        />
      </section>

      <section className="quick-directions">
        {quickDirections.map((item) => (
          <article key={item.title} className="direction-card">
            <h3>{item.title}</h3>
            <p>{item.subtitle}</p>
            <span>{item.count}</span>
          </article>
        ))}
      </section>

      <section className="vacancies-section" id="vacancies">
        <div className="vacancies-header">
          <h2>Свежие вакансии</h2>
          <button
            onClick={() => {
              vacanciesQuery.refetch()
              setInfo('Обновляем список вакансий...')
            }}
            className="secondary-btn"
          >
            Обновить
          </button>
        </div>

        <form
          className="search-box search-box-top"
          onSubmit={(e) => {
            e.preventDefault()
            const value = searchInput.trim()
            setSearch(value)
            setInfo(value ? `Ищем вакансии по запросу: «${value}».` : 'Показываем все доступные вакансии.')
          }}
        >
          <input
            placeholder="Профессия, должность или компания"
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
          />
          <button type="submit">Найти</button>
        </form>

        <p className="info-box">{info}</p>

        {vacanciesQuery.isLoading && <p className="info-box">Загружаем вакансии...</p>}

        {vacanciesQuery.isError && (
          <div className="error-box">
            <p>Не удалось загрузить вакансии. Проверь подключение к серверу.</p>
            <button onClick={() => vacanciesQuery.refetch()} className="secondary-btn">Повторить</button>
          </div>
        )}

        {!vacanciesQuery.isLoading && !vacanciesQuery.isError && !hasVacancies && (
          <div className="empty-box">
            <p>По вашему запросу вакансий пока нет.</p>
            <button
              onClick={() => {
                setSearchInput('')
                setSearch('')
                setInfo('Поиск сброшен. Показываем все вакансии.')
              }}
              className="secondary-btn"
            >
              Сбросить поиск
            </button>
          </div>
        )}

        {hasVacancies && (
          <div className="vacancy-grid">
            {vacanciesQuery.data?.map((vacancy) => {
              const isFavorite = favorites.includes(vacancy.id)

              return (
                <article key={vacancy.id} className="vacancy-card">
                  <div className="vacancy-card-head">
                    <h3>
                      <a href={`/vacancies/${vacancy.id}`} target="_blank" rel="noreferrer">
                        {vacancy.title}
                      </a>
                    </h3>
                    <span className="chip">{vacancy.profession_name}</span>
                  </div>
                  <p className="vacancy-meta">{vacancy.company_name} • {vacancy.city_name}</p>
                  <p className="vacancy-salary">
                    {vacancy.salary_min.toLocaleString('ru-RU')} — {vacancy.salary_max.toLocaleString('ru-RU')} ₽
                  </p>
                  <p className="vacancy-desc">{vacancy.description}</p>
                  <div className="vacancy-actions">
                    <button className="primary-btn" onClick={() => goToLogin('Для отклика сначала войдите в аккаунт.')}>Откликнуться</button>
                    <button className="favorite-btn" onClick={() => toggleFavorite(vacancy.id, vacancy.title)}>
                      {isFavorite ? '★ В избранном' : '☆ В избранное'}
                    </button>
                  </div>
                </article>
              )
            })}
          </div>
        )}
      </section>

      <section className="companies" id="companies">
        <div className="section-head">
          <h2>Топ компании</h2>
          <p>Крупные работодатели, которые активно нанимают прямо сейчас.</p>
        </div>
        <div className="company-grid">
          {featuredCompanies.map((company) => (
            <article key={company.name} className="company-card">
              <img src={company.image} alt={company.name} />
              <div>
                <h3>{company.name}</h3>
                <p className="vacancy-salary">{company.jobs}</p>
                <p className="vacancy-desc">{company.description}</p>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="benefits" id="benefits">
        <div className="section-head">
          <h2>Почему JobFinder</h2>
          <p>Платформа, где удобно и быстро искать работу.</p>
        </div>
        <div className="benefit-grid">
          {benefits.map((benefit) => (
            <article key={benefit.title} className="benefit-card">
              <h3>{benefit.title}</h3>
              <p>{benefit.text}</p>
            </article>
          ))}
        </div>
      </section>
    </div>
  )
}
