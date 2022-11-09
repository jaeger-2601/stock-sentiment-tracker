
// Change URL in production
const ROOT_URL = 'http://localhost:8000';

// Routes
export const TICKERS_INFO_ROUTE = `${ROOT_URL}/tickers-info/{TIME_RANGE}`;
export const TICKER_PRICES_ROUTE = `${ROOT_URL}/ticker-prices/{COMPANY}/{TIME_RANGE}`;
