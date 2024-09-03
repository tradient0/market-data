// automation/fetch_cookies.js

const axios = require('axios');
const tough = require('tough-cookie');
const { wrapper } = require('axios-cookiejar-support');

(async () => {
  // Initialize a cookie jar
  const cookieJar = new tough.CookieJar();
  
  // Wrap axios to add cookie jar support
  const client = wrapper(axios.create({ jar: cookieJar, withCredentials: true }));

  try {
    // Make a request with the cookie jar
    const response = await client.get('https://www.nseindia.com/companies-listing/corporate-filings-actions');

    // Retrieve and format cookies
    const cookies = cookieJar.getCookieStringSync(response.config.url);
    console.log('Cookies:', cookies);

    // Output cookies for GitHub Actions
    console.log(`::set-output name=cookies::${cookies}`);
  } catch (error) {
    console.error('Error fetching cookies:', error);
    process.exit(1);
  }
})();
