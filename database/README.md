---

# Chinook Database Schema

The Chinook Database is a relational database designed to model a digital media store. It contains information about artists, albums, tracks, customers, employees, invoices, and more. The schema is normalized and structured to efficiently manage music-related data.

## Table of Contents
1. [Overview](#overview)
2. [Database Diagram](#database-diagram)
3. [Tables and Relationships](#tables-and-relationships)
4. [Usage Instructions](#usage-instructions)
5. [Sample Queries](#sample-queries)
6. [Contributing](#contributing)

---

## Overview

The Chinook Database is commonly used in tutorials and projects involving SQL, data analysis, and database management. It simulates a music store with tables for artists, albums, tracks, customers, employees, invoices, and playlists. The database is highly normalized, ensuring data integrity and efficient querying.

---

## Database Diagram

Below is a visual representation of the Chinook Database schema:

![Chinook Database Diagram](attachment:chinook_database_diagram.png)

> **Note**: If you are viewing this README on GitHub, the image may not render directly. You can download or view the image separately.

---

## Tables and Relationships

### 1. **Artist**
- **Columns**:
  - `ArtistId`: Primary key.
  - `Name`: Name of the artist.
- **Purpose**: Stores information about music artists.

### 2. **Album**
- **Columns**:
  - `AlbumId`: Primary key.
  - `Title`: Title of the album.
  - `ArtistId`: Foreign key referencing `Artist.ArtistId`.
- **Purpose**: Stores information about albums and their associated artists.

### 3. **Track**
- **Columns**:
  - `TrackId`: Primary key.
  - `Name`: Name of the track.
  - `AlbumId`: Foreign key referencing `Album.AlbumId`.
  - `MediaTypeId`: Foreign key referencing `MediaType.MediaTypeId`.
  - `GenreId`: Foreign key referencing `Genre.GenreId`.
  - `Composer`: Composer of the track.
  - `Milliseconds`: Duration of the track in milliseconds.
  - `Bytes`: Size of the track in bytes.
  - `UnitPrice`: Price of the track.
- **Purpose**: Stores detailed information about individual tracks, including metadata and pricing.

### 4. **MediaType**
- **Columns**:
  - `MediaTypeId`: Primary key.
  - `Name`: Type of media (e.g., MP3, AAC).
- **Purpose**: Categorizes tracks by their media type.

### 5. **Genre**
- **Columns**:
  - `GenreId`: Primary key.
  - `Name`: Name of the genre.
- **Purpose**: Categorizes tracks by their musical genre.

### 6. **Playlist**
- **Columns**:
  - `PlaylistId`: Primary key.
  - `Name`: Name of the playlist.
- **Purpose**: Represents user-created playlists.

### 7. **PlaylistTrack**
- **Columns**:
  - `PlaylistId`: Foreign key referencing `Playlist.PlaylistId`.
  - `TrackId`: Foreign key referencing `Track.TrackId`.
- **Purpose**: Maps tracks to playlists, allowing multiple tracks per playlist.

### 8. **InvoiceLine**
- **Columns**:
  - `InvoiceLineId`: Primary key.
  - `InvoiceId`: Foreign key referencing `Invoice.InvoiceId`.
  - `TrackId`: Foreign key referencing `Track.TrackId`.
  - `UnitPrice`: Price of the track.
  - `Quantity`: Quantity purchased.
- **Purpose**: Links invoices to tracks, detailing what was purchased.

### 9. **Invoice**
- **Columns**:
  - `InvoiceId`: Primary key.
  - `CustomerId`: Foreign key referencing `Customer.CustomerId`.
  - `InvoiceDate`: Date of the invoice.
  - `BillingAddress`, `BillingCity`, `BillingState`, `BillingCountry`, `BillingPostalCode`: Billing address details.
  - `Total`: Total amount of the invoice.
- **Purpose**: Stores customer invoices and purchase details.

### 10. **Customer**
- **Columns**:
  - `CustomerId`: Primary key.
  - `FirstName`, `LastName`: Customer's name.
  - `Company`, `Address`, `City`, `State`, `Country`, `PostalCode`: Contact information.
  - `Phone`, `Fax`, `Email`: Communication details.
  - `SupportRepId`: Foreign key referencing `Employee.EmployeeId`.
- **Purpose**: Stores customer information and their support representative.

### 11. **Employee**
- **Columns**:
  - `EmployeeId`: Primary key.
  - `LastName`, `FirstName`: Employee's name.
  - `Title`: Job title.
  - `ReportsTo`: Foreign key referencing `Employee.EmployeeId` (self-referential for hierarchy).
  - `BirthDate`, `HireDate`: Dates of birth and hire.
  - `Address`, `City`, `State`, `Country`, `PostalCode`: Address details.
  - `Phone`, `Fax`, `Email`: Communication details.
- **Purpose**: Stores employee information, including hierarchical reporting.

### Relationships
- **One-to-Many Relationships**:
  - `Artist` → `Album`
  - `Album` → `Track`
  - `MediaType` → `Track`
  - `Genre` → `Track`
  - `Customer` → `Invoice`
  - `Employee` → `Customer` (via `SupportRepId`)
  - `Employee` → `Employee` (hierarchical relationship via `ReportsTo`)
- **Many-to-Many Relationships**:
  - `Playlist` ↔ `Track` (via `PlaylistTrack`)
  - `Invoice` ↔ `Track` (via `InvoiceLine`)

---

## Usage Instructions

### 1. Importing the Database
You can import the database using the SQL dump file (`Chinook.sql`) provided in the `database/` directory:
```bash
mysql -u root -p < database/Chinook.sql
```

### 2. Connecting to the Database
Use the following connection string to connect to the database:
```python
db_url = "mysql+mysqlconnector://root:password@localhost:3306/Chinook"
```

### 3. Exploring the Data
Here are some sample queries to get started:
- **List all artists**:
  ```sql
  SELECT * FROM Artist;
  ```
- **List all tracks from a specific album**:
  ```sql
  SELECT Track.Name FROM Track
  INNER JOIN Album ON Track.AlbumId = Album.AlbumId
  WHERE Album.Title = 'Specific Album Name';
  ```

---

## Sample Queries

Here are some example queries to demonstrate how to interact with the database:

1. **Count the number of artists**:
   ```sql
   SELECT COUNT(*) AS NumberOfArtists FROM Artist;
   ```

2. **List all customers who have made purchases**:
   ```sql
   SELECT DISTINCT Customer.FirstName, Customer.LastName
   FROM Customer
   INNER JOIN Invoice ON Customer.CustomerId = Invoice.CustomerId;
   ```

3. **Calculate total revenue by country**:
   ```sql
   SELECT Invoice.BillingCountry, SUM(Invoice.Total) AS TotalRevenue
   FROM Invoice
   GROUP BY Invoice.BillingCountry
   ORDER BY TotalRevenue DESC;
   ```

---

## License

This database schema is licensed under the [MIT License](LICENSE).

---

## Acknowledgments

- **Chinook Database**: Originally created by Microsoft as part of the SQL Server sample databases.
- **Schema Visualization**: Generated using [DB Designer](https://www.dbdesigner.net/) or similar tools.

---
