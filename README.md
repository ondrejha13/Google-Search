# Google Search and CSV Export Application

## Description

This is a Django-based web application that allows users to perform a Google search and export the search results to a CSV file. The application enables the following features:

- **Search Functionality**: Users can search for content using a query, and the results will be displayed on the page.
- **Export to CSV**: After performing a search, users can export the results to a CSV file, which includes the title, link, and description of the search results.

## Features

- **Search**: Submit a search query to find relevant content.
- **CSV Export**: Export search results in CSV format, including the following columns:
  - Title
  - Link
  - Description

## Tests

This application includes automated tests to ensure its functionality:

- **Search Test**: Verifies that a search query returns the expected results and displays the query within the page.
- **Export Test**: Verifies that search results can be exported to a CSV file, and the file contains the correct structure and data.
