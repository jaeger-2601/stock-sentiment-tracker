
// Change URL in production
const ROOT_URL = 'http://localhost:8000';

class PathParametersException {

    constructor(message) {
        this.message = message;
        this.name = 'PathParametersException';
    }
}

function route(routeStrings, ...pathParameters) {
    return (...values) => { 

        // Check if correct number of path parameters are provided
        if (values.length > pathParameters.length || values.length < pathParameters.length) 
            throw new PathParametersException(`Route takes ${pathParameters.length} path parameters but ${values.length} was provided`);

        let route = ROOT_URL;
        for (let i=0; i < pathParameters.length; ++i) { 
            route += routeStrings[i];
            route += values[i];
        }
        return route;
    }
}

// Routes
export const TICKERS_INFO_ROUTE = route`/tickers-info/${"TIME_RANGE"}`;
export const TICKER_PRICES_ROUTE = route`/ticker-prices/${"COMPANY"}/${"TIME_RANGE"}`;
export const COMPANY_SUMMARY_ROUTE = route`/company-summary/${"COMPANY"}`;
export const WORD_COUNTS_ROUTE = route`/word-counts/${"COMPANY"}/${"TIME_RANGE"}`;
export const COMPANY_FUNDAMENTALS_ROUTE = route`/company-fundamentals/${"COMPANY"}`;
export const MOVING_AVERAGES_ROUTE = route`/moving-averages/${"COMPANY"}/${"TIME_RANGE"}`;
export const BASIC_INFO_ROUTE = route`/basic-info/${"COMPANY"}`;
