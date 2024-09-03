// automation/fetch_cookies.js

const axios = require('axios');
const tough = require('tough-cookie');
const axiosCookieJarSupport = require('axios-cookiejar-support').default;

(async () => {
  // Initialize a cookie jar
  const cookieJar = new tough.CookieJar();
  axiosCookieJarSupport(axios);

  try {
    // Make a request with the cookie jar
    const response = await axios.get('https://www.nseindia.com/companies-listing/corporate-filings-actions', {
      jar: cookieJar,
      withCredentials: true,
    });

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
