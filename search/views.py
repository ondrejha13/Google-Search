import csv
import requests
import base64
from datetime import datetime
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render

# Function to generate the SOCS cookie for Google search requests
def generate_socs_cookie():
    socs_value = f"\b\x01\x12\x1C\b\x01\x12\x12gws_{datetime.today().strftime('%Y%m%d')}-0_RC3\x1A\x02en \x01\x1A\x06\b\x80º¦±\x06"  # Create the SOCS cookie value
    return base64.encodebytes(socs_value.encode()).decode().strip()  # Return the base64 encoded value of the cookie

# Main function to handle the search functionality
def search_view(request):
    query = ""

    if request.method == 'POST':
        query = request.POST.get('query')  # Retrieve the search query from the POST data
        socs_cookie = generate_socs_cookie()  # Generate the SOCS cookie

        # Define the headers for the GET request to Google, including the User-Agent and SOCS cookie
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/123.0.2420.97",
            "Cookie": f"SOCS={socs_cookie}",
        }

        # Send a GET request to Google with the search query and headers
        response = requests.get(f"https://www.google.com/search?q={query}", headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')  # Parse the HTML response using BeautifulSoup

        results = []  # Initialize an empty list to store search results

        # Loop through the search results and extract relevant information
        for result in soup.select('.tF2Cxc'):
            title = result.select_one('.DKV0Md').text if result.select_one('.DKV0Md') else ''
            link = result.select_one('.yuRUbf a')['href'] if result.select_one('.yuRUbf a') else ''
            description = result.select_one('.VwiC3b').text if result.select_one('.VwiC3b') else ''

            results.append({'title': title, 'link': link, 'description': description})

        # Store the results and query in the session
        request.session['search_results'] = results
        request.session['query'] = query

    # If the request method is GET, load results from the session
    else:
        results = request.session.get('search_results', [])

    # Render the search results page
    return render(request, 'search.html', {'results': results, 'query': query})

# Function to export search results to a CSV file
def export_csv(request):
    results = request.session.get('search_results', [])
    query = request.session.get('query', '')

    response = HttpResponse(content_type='text/csv')  # Create an HTTP response with CSV content type
    response[
        'Content-Disposition'] = f'attachment; filename="results_{query}.csv"'  # Set the CSV file name with the query

    writer = csv.writer(response)  # Create a CSV writer object

    writer.writerow([f"Search results for: {query}"]) # Add the query as a title in the first row
    writer.writerow(['Title', 'Link', 'Description'])  # Write the header row to the CSV file

    # Loop through the results and write each result as a row in the CSV file
    for result in results:
        writer.writerow([result['title'], result['link'], result['description']])

    return response  # Return the response containing the CSV file