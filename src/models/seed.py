import asyncio
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import async_session
from src.models.model import (
    Role,
    City,
    Profession,
    Skill,
    WorkSchedule,
    EmploymentType,
    EducationalInstitution,
    User, 
)
from src.core.hash import HashService  

ROLES = [
    {"name": "admin"},
    {"name": "company"},
    {"name": "applicant"},
]

CITIES = [
    "Минск",
    "Гомель",
    "Могилёв",
    "Витебск",
    "Гродно",
    "Брест",
    "Бобруйск",
    "Барановичи",
    "Борисов",
    "Пинск",
    "Орша",
    "Мозырь",
    "Солигорск",
    "Новополоцк",
    "Лида",
    "Молодечно",
    "Полоцк",
    "Жлобин",
    "Светлогорск",
    "Речица",
    "Слуцк",
    "Жодино",
]

PROFESSIONS = [
    "Программист",
    "Системный администратор",
    "Менеджер по продажам",
    "Бухгалтер",
    "Водитель",
    "Учитель",
    "Врач",
    "Инженер",
    "Экономист",
    "Юрист",
    "Дизайнер",
    "Маркетолог",
    "Строитель",
    "Электрик",
    "Сварщик",
    "Повар",
    "Официант",
    "Администратор",
    "Аналитик",
    "Тестировщик",
]

SKILLS = [
    "Python",
    "SQL",
    "JavaScript",
    "HTML",
    "CSS",
    "Коммуникабельность",
    "Ответственность",
    "Работа в команде",
    "Управление проектами",
    "Английский язык",
    "1С",
    "Photoshop",
    "Excel",
    "Word",
    "Adobe Illustrator",
    "C++",
    "Java",
    "C#",
    "PHP",
    "Ruby",
    "Go",
    "Linux",
    "Windows Server",
    "Стрессоустойчивость",
    "Обучаемость",
]

WORK_SCHEDULES = [
    "Полный день",
    "Сменный график",
    "Гибкий график",
    "Удаленная работа",
    "Вахтовый метод",
]

EMPLOYMENT_TYPES = [
    "Полная занятость",
    "Частичная занятость",
    "Стажировка",
    "Проектная работа",
    "Волонтерство",
]

EDUCATIONAL_INSTITUTIONS = [
    "Белорусский государственный университет (БГУ)",
    "Белорусский национальный технический университет (БНТУ)",
    "Белорусский государственный университет информатики и радиоэлектроники (БГУИР)",
    "Белорусский государственный экономический университет (БГЭУ)",
    "Минский государственный лингвистический университет (МГЛУ)",
    "Белорусский государственный медицинский университет (БГМУ)",
    "Гродненский государственный университет имени Янки Купалы",
    "Витебский государственный университет имени П.М. Машерова",
    "Могилёвский государственный университет имени А.А. Кулешова",
    "Полесский государственный университет",
    "Брестский государственный университет имени А.С. Пушкина",
    "Гомельский государственный университет имени Франциска Скорины",
    "Белорусский государственный технологический университет",
    "Белорусский государственный аграрный технический университет",
    "Академия управления при Президенте Республики Беларусь",
    "Минский государственный колледж электроники",
    "Минский государственный колледж сферы обслуживания",
    "Минский государственный профессионально-технический колледж строительства",
    "Гомельский государственный колледж связи",
    "Витебский государственный колледж культуры и искусств",
]


async def seed_roles(db: AsyncSession) -> None:
    for role_data in ROLES:
        existing = await db.execute(
            select(Role).where(Role.name == role_data["name"])
        )
        if not existing.scalar_one_or_none():
            role = Role(**role_data)
            db.add(role)
    await db.flush()
    print("✅ Роли обработаны.")


async def seed_cities(db: AsyncSession) -> None:
    for city_name in CITIES:
        existing = await db.execute(
            select(City).where(City.name == city_name)
        )
        if not existing.scalar_one_or_none():
            city = City(name=city_name)
            db.add(city)
    await db.flush()
    print("✅ Города обработаны.")


async def seed_professions(db: AsyncSession) -> None:
    for prof_name in PROFESSIONS:
        existing = await db.execute(
            select(Profession).where(Profession.name == prof_name)
        )
        if not existing.scalar_one_or_none():
            profession = Profession(name=prof_name)
            db.add(profession)
    await db.flush()
    print("✅ Профессии обработаны.")


async def seed_skills(db: AsyncSession) -> None:
    for skill_name in SKILLS:
        existing = await db.execute(
            select(Skill).where(Skill.name == skill_name)
        )
        if not existing.scalar_one_or_none():
            skill = Skill(name=skill_name)
            db.add(skill)
    await db.flush()
    print("✅ Навыки обработаны.")


async def seed_work_schedules(db: AsyncSession) -> None:
    for schedule_name in WORK_SCHEDULES:
        existing = await db.execute(
            select(WorkSchedule).where(WorkSchedule.name == schedule_name)
        )
        if not existing.scalar_one_or_none():
            schedule = WorkSchedule(name=schedule_name)
            db.add(schedule)
    await db.flush()
    print("✅ Графики работы обработаны.")


async def seed_employment_types(db: AsyncSession) -> None:
    for et_name in EMPLOYMENT_TYPES:
        existing = await db.execute(
            select(EmploymentType).where(EmploymentType.name == et_name)
        )
        if not existing.scalar_one_or_none():
            emp_type = EmploymentType(name=et_name)
            db.add(emp_type)
    await db.flush()
    print("✅ Типы занятости обработаны.")


async def seed_educational_institutions(db: AsyncSession) -> None:
    for inst_name in EDUCATIONAL_INSTITUTIONS:
        existing = await db.execute(
            select(EducationalInstitution).where(EducationalInstitution.name == inst_name)
        )
        if not existing.scalar_one_or_none():
            institution = EducationalInstitution(name=inst_name)
            db.add(institution)
    await db.flush()
    print("✅ Учреждения образования обработаны.")


async def seed_admin_user(db: AsyncSession) -> None:
    result = await db.execute(select(Role).where(Role.name == "admin"))
    admin_role = result.scalar_one_or_none()
    if not admin_role:
        print("⚠️ Роль admin не найдена, администратор не создан.")
        return

    existing = await db.execute(
        select(User).where(User.email == "admin@example.com")
    )
    if existing.scalar_one_or_none():
        print("ℹ️ Администратор уже существует.")
        return

    hashed_password = HashService.get_password_hash("admin123")
    admin_user = User(
        email="admin@example.com",
        password_hash=hashed_password,
        role_id=admin_role.id,
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(admin_user)
    await db.flush()
    print("✅ Создан пользователь-администратор (admin@example.com / admin123).")


async def seed_all():
    async with async_session() as db:
        await seed_roles(db)
        await seed_cities(db)
        await seed_professions(db)
        await seed_skills(db)
        await seed_work_schedules(db)
        await seed_employment_types(db)
        await seed_educational_institutions(db)
        await seed_admin_user(db)

        await db.commit()
        print("🎉 Все справочники и администратор успешно созданы.")


if __name__ == "__main__":
    asyncio.run(seed_all())