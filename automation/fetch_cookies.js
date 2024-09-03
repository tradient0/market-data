const axios = require('axios');
const tough = require('tough-cookie');
const { wrapper } = require('axios-cookiejar-support');
const axiosRetry = require('axios-retry');

(async () => {
  const cookieJar = new tough.CookieJar();
  const client = wrapper(axios.create({ jar: cookieJar, withCredentials: true }));

  // Set up retry logic
  axiosRetry(client, { retries: 3, retryDelay: axiosRetry.exponentialDelay });

  try {
    const response = await client.get('https://www.nseindia.com/companies-listing/corporate-filings-actions', {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Connection': 'keep-alive',
      },
    });

    const cookies = cookieJar.getCookieStringSync(response.config.url);
    console.log('Cookies:', cookies);

    console.log(`::set-output name=cookies::${cookies}`);
  } catch (error) {
    console.error('Error fetching cookies:', error);
    process.exit(1);
  }
})();
