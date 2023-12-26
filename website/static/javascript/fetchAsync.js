async function fetchImageUrls(params) {
    url = window.location.origin + "/api/fetch"
    try {
        // Convert parameters object to query string
        const queryString = Object.keys(params)
          .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
          .join('&');
    
        // Append query string to the URL if parameters are present
        const fullUrl = queryString ? `${url}?${queryString}` : url;
    
        // Make the fetch request
        console.log(fullUrl)
        const response = await fetch(fullUrl);
    
        // Check if the request was successful (status code 200-299)
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
    
        // Parse and return the JSON response
        return await response.json();
      } catch (error) {
        console.error('Error during fetch:', error);
      }
}

