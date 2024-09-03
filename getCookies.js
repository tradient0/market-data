const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: "new" }); // Use the new headless mode
  const page = await browser.newPage();
  
  // Set user agent and headers
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36');
  await page.setExtraHTTPHeaders({
    'Accept-Language': 'en-US,en;q=0.9'
  });

  // Capture request cookies
  await page.setRequestInterception(true);
  page.on('request', interceptedRequest => {
    const cookies = interceptedRequest.headers()['cookie'];
    console.log(cookies);
    interceptedRequest.continue();
  });

  // Navigate to the NSE India Corporate Actions page
  await page.goto('https://www.nseindia.com/companies-listing/corporate-filings-actions');

  // Wait for the page to fully load
  await page.waitForTimeout(5000); // Adjust timeout as necessary

  await browser.close();
})();
