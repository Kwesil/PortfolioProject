/*

	Cleaning data in SQL query

*/

SELECT *
FROM portfolioProject..nashville

-----------------------------------------------------------------------------------------------------

-- Standardize Date format

SELECT SaleDateConverted, CONVERT(DATE, SaleDate)
FROM portfolioProject..nashville

UPDATE portfolioProject..nashville
SET SaleDate = CONVERT(DATE, SaleDate)

ALTER TABLE portfolioProject..nashville
ADD SaleDateConverted Date;

UPDATE portfolioProject..nashville
SET SaleDateConverted = CONVERT(DATE, SaleDate)

------------------------------------------------------------------------------------------------

-- Populate property address data

SELECT *
FROM portfolioProject..nashville
-- WHERE PropertyAddress is null
ORDER BY ParcelID


SELECT 
	a.ParcelID, a.PropertyAddress, 
	b.ParcelID, b.PropertyAddress, ISNULL(a.PropertyAddress, b.PropertyAddress)
FROM portfolioProject..nashville a
JOIN portfolioProject..nashville b
	ON a.ParcelID = b.ParcelID
	AND a.[UniqueID ] <> b.[UniqueID ]
WHERE a.PropertyAddress is null

UPDATE a
SET PropertyAddress = ISNULL(a.PropertyAddress, b.PropertyAddress)
FROM portfolioProject..nashville a
JOIN portfolioProject..nashville b
	ON a.ParcelID = b.ParcelID
	AND a.[UniqueID ] <> b.[UniqueID ]
WHERE a.PropertyAddress is null

--------------------------------------------------------------------------------------------------

-- Breaking out Address into Individual Columns (Address, City, State)

SELECT PropertyAddress
FROM portfolioProject..nashville



SELECT 
SUBSTRING(PropertyAddress, 1, CHARINDEX(',', PropertyAddress)- 1) as Address,
  SUBSTRING(PropertyAddress, CHARINDEX(',', PropertyAddress) + 1, LEN(PropertyAddress)) as Address


FROM portfolioProject..nashville


ALTER TABLE portfolioProject..nashville
ADD PropertySplitAddress NVARCHAR(255);

UPDATE portfolioProject..nashville
SET PropertySplitAddress = SUBSTRING(PropertyAddress, 1, CHARINDEX(',', PropertyAddress)- 1) 

ALTER TABLE portfolioProject..nashville
ADD PropertySplitCity NVARCHAR(255);

UPDATE portfolioProject..nashville
SET PropertySplitCity =  SUBSTRING(PropertyAddress, CHARINDEX(',', PropertyAddress) + 1, LEN(PropertyAddress))

SELECT *
FROM portfolioProject..nashville

 
 SELECT OwnerAddress
 FROM portfolioProject..nashville

 SELECT
	 PARSENAME(REPLACE(OwnerAddress, ',', '.'), 3),
	 PARSENAME(REPLACE(OwnerAddress, ',', '.'), 2),
	 PARSENAME(REPLACE(OwnerAddress, ',', '.'), 1)
 FROM portfolioProject..nashville



ALTER TABLE portfolioProject..nashville
ADD OwnerSplitAddress NVARCHAR(255);

UPDATE portfolioProject..nashville
SET OwnerSplitAddress =  PARSENAME(REPLACE(OwnerAddress, ',', '.'), 3)

ALTER TABLE portfolioProject..nashville
ADD OwnerSplitCity NVARCHAR(255);

UPDATE portfolioProject..nashville
SET OwnerSplitCity =  PARSENAME(REPLACE(OwnerAddress, ',', '.'), 2)

ALTER TABLE portfolioProject..nashville
ADD OwnerSplitState NVARCHAR(255);

UPDATE portfolioProject..nashville
SET OwnerSplitState =  PARSENAME(REPLACE(OwnerAddress, ',', '.'), 1)

SELECT *
FROM portfolioProject..nashville

-----------------------------------------------------------------------------------------------------------------------------------------

-- Change Y and N to Yes and No in "Sold as vacant" field

SELECT DISTINCT(SoldAsVacant), COUNT(SoldAsVacant)
FROM portfolioProject..nashville
GROUP BY SoldAsVacant
ORDER BY 2

SELECT SoldAsVacant,
	CASE when SoldAsVacant = 'Y' then 'Yes'
		 when SoldAsVacant = 'N' then 'No'
		 ELSE SoldAsVacant
		 END
FROM portfolioProject..nashville

UPDATE portfolioProject..nashville
SET SoldAsVacant = CASE when SoldAsVacant = 'Y' then 'Yes'
		 when SoldAsVacant = 'N' then 'No'
		 ELSE SoldAsVacant
		 END

-----------------------------------------------------------------------------------------------------------------------------------------------

-- Removing Duplicates



WITH RowNumCTE AS(
SELECT *,
	ROW_NUMBER() OVER (
	PARTITION BY ParcelID,
				 PropertyAddress,
				 SalePrice,
				 SaleDate,
				 LegalReference
				 ORDER BY 
					UniqueID
					) row_num

FROM portfolioProject..nashville
)
SELECT *
FROM RowNumCTE
WHERE row_num > 1
ORDER BY PropertyAddress

-----------------------------------------------------------------------------------------------------------------------------------------------

-- Delete Unused Columns

SELECT * 
FROM portfolioProject..nashville

ALTER TABLE portfolioProject..nashville
DROP COLUMN OwnerAddress, PropertyAddress, TaxDistrict

ALTER TABLE portfolioProject..nashville
DROP COLUMN SaleDate
