SELECT *
FROM portfolioProject..CovidDeaths
WHERE continent IS  NOT NULL
ORDER BY 3,4

-- Select Data  that  we are going to use

SELECT 
	location, date, total_cases, new_cases, total_deaths, population
FROM portfolioProject..CovidDeaths
ORDER BY 1, 2

-- Looking at Total cases vs Total Deaths
-- Shows the likelihood of dying if you contract covid in your country.
SELECT 
	location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 as DeathPerccentage
FROM portfolioProject..CovidDeaths
WHERE location LIKE '%states%'
ORDER BY 1, 2
 
-- Looking at the Total cases vs Population

SELECT
	location, date, total_cases, total_deaths, (total_cases/population)*100 AS Percentage
FROM portfolioProject..CovidDeaths
WHERE location LIKE '%states%'
ORDER BY 1, 2

-- Looking at country with  highest infection rate compared to population
SELECT
	location, population, MAX(total_cases) AS HighestInfectionCount, MAX((total_cases/population)*100)
	AS PercentPopulationInfected
FROM portfolioProject..CovidDeaths
GROUP BY location, population
ORDER BY PercentPopulationInfected DESC

-- Showing the country with the highest death count per population

SELECT 
	location, MAX(cast(Total_deaths AS int)) AS TotalDeathCount
FROM portfolioProject..CovidDeaths
WHERE continent IS NOT NULL
GROUP BY location
ORDER BY TotalDeathCount DESC

-- Break things down by continent
-- Showing the continent with  the highest death count
SELECT
	continent, MAX(cast(Total_deaths as int)) AS TotalDeathCount
FROM portfolioProject..CovidDeaths
WHERE continent IS NOT NULL
GROUP BY continent
ORDER BY TotalDeathCount DESC

-- Global Numbers
SELECT
	date, SUM(new_cases) as Total_new_cases, SUM(CAST(new_deaths as int)) as Total_new_deaths, SUM(CAST(new_deaths as int))/SUM(new_cases)*100 AS DeathPercentage
FROM portfolioProject..CovidDeaths
WHERE location LIKE '%states%'
AND continent IS NOT NULL
GROUP BY date
ORDER BY 1,2

-- Looking at Total Population vs Vaccination

WITH PopvsVac (continent, location, date, population, new_vaccinations, RollingPeopleVaccinated)
as
(
SELECT
	dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, SUM(cast(vac.new_vaccinations as int))
	OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date ROWS UNBOUNDED PRECEDING) as RollingPeopleVaccinated
FROM portfolioProject..CovidDeaths dea
JOIN portfolioProject..CovidVaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL
-- ORDER BY 2,3
)

SELECT *, (RollingPeopleVaccinated/population)*100
FROM PopvsVac

-- Temp Table
DROP TABLE if exists #PercentPopulationVaccinated
CREATE TABLE #PercentPopulationVaccinated
(
continent nvarchar(255),
location nvarchar(255),
date datetime,
population numeric,
new_vaccinations numeric,
RollingPeopleVaccinated numeric
)


INSERT INTO #PercentPopulationVaccinated
SELECT
	dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, SUM(cast(vac.new_vaccinations as int))
	OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date ROWS UNBOUNDED PRECEDING) as RollingPeopleVaccinated
FROM portfolioProject..CovidDeaths dea
JOIN portfolioProject..CovidVaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL
-- ORDER BY 2,3

SELECT *, (RollingPeopleVaccinated/population)*100
FROM #PercentPopulationVaccinated


-- Creating a view to store data for visualization

CREATE VIEW PercentPopulationVaccinated as
SELECT
	dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, SUM(cast(vac.new_vaccinations as int))
	OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date ROWS UNBOUNDED PRECEDING) as RollingPeopleVaccinated
FROM portfolioProject..CovidDeaths dea
JOIN portfolioProject..CovidVaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL
-- ORDER BY 2,3

SELECT * 
FROM PercentPopulationVaccinated
