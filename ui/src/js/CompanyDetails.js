import { useEffect, useState, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { Chart } from 'react-chartjs-2';
import { Tabs, Tab, Table } from 'react-bootstrap';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import ReactWordCloud from 'react-wordcloud';

import { TICKER_PRICES_ROUTE, COMPANY_SUMMARY_ROUTE, WORD_COUNTS_ROUTE, COMPANY_FUNDAMENTALS_ROUTE, MOVING_AVERAGES_ROUTE, BASIC_INFO_ROUTE } from './Routes';

import "../css/CompanyDetails.css";

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);


function AboutCompany (props) {

    const [summary, setSummary] = useState('');

    useEffect( () => {
        fetch(COMPANY_SUMMARY_ROUTE.replace('{COMPANY}', props.company))
            .then((response) => response.json())
            .then((json_data) => setSummary(json_data['data'])
        )}, [props.company]);

    return (
        <p class="text-wrap text-white py-4">{summary}</p>
    );
}

function WordCloud (props) {

    const [wordCounts, setWordCounts] = useState({});
    const wordCloudOptions = {
        fontSizes: [30, 60],
        colors: ['#FF6384', '#1ff073', '#54B4D3', '#B23CFD', '#FFA900'],
        enableTooltip: false
    };
    const wordCloudSize = [500, 300];

    useEffect( () => {
        const modified_counts_route = WORD_COUNTS_ROUTE.replace('{COMPANY}', props.company)
                                                        .replace('{TIME_RANGE}', props.timeRange);
        fetch(modified_counts_route)
            .then((response) => response.json())
            .then((json_data) => {
                const data = json_data['data'].map(
                            ([word, count]) => { return {text:word, value:count }; }
                        );
                setWordCounts(data);
            });
    }, [props.company, props.timeRange]);

    return (
        <div class="word-cloud-wrapper-wrapper pt-4">
            <div class="word-cloud-wrapper">
                <ReactWordCloud words={wordCounts} size={wordCloudSize} options={wordCloudOptions}/>
            </div>
        </div>
    );

}

function CompanyFundamentals (props) {

    const [fundamentalsData, setFundamentalsData] = useState(null);

    useEffect( () => {
        fetch(COMPANY_FUNDAMENTALS_ROUTE.replace('{COMPANY}', props.company))
            .then((response) => response.json())
            .then((json_data) => setFundamentalsData(json_data['data']));
    }, [props.company]);

    return (

        fundamentalsData && 

        <div class="fundamentals-data pt-4">
            <Table striped bordered hover variant="dark">
                <tbody>
                    <tr><td colspan="2">Basic stats</td></tr>
                    <tr>
                        <th>Revenue</th>
                        <td>{fundamentalsData['basicStats']['revenue']}</td>
                    </tr>
                    <tr>
                        <th>EPS</th>
                        <td>{fundamentalsData['basicStats']['eps']}</td>
                    </tr>
                    <tr>
                        <th>Total Debt</th>
                        <td>{fundamentalsData['basicStats']['totalDebt']}</td>
                    </tr>
                    <tr>
                        <th>P/E Ratio</th>
                        <td>{fundamentalsData['basicStats']['trailingPE']}</td>
                    </tr>
                    <tr>
                        <th>Profit Margin</th>
                        <td>{fundamentalsData['basicStats']['profitMarign']}</td>
                    </tr>
                    <tr>
                        <th>Market Cap</th>
                        <td>{fundamentalsData['basicStats']['marketCap']}</td>
                    </tr>
                </tbody>
            </Table>

            <Table striped bordered hover variant="dark">
                <tbody>
                <tr><td colspan="2">Historic Growth</td></tr>
                    <tr>
                        <th>Revenue Growth</th>
                        <td>{fundamentalsData['historicGrowth']['revenueGrowth']}</td>
                    </tr>
                    <tr>
                        <th>EPS Growth</th>
                        <td>{fundamentalsData['historicGrowth']['epsGrowth']}</td>
                    </tr>
                    <tr>
                        <th>52 Week High</th>
                        <td>{fundamentalsData['historicGrowth']['fiftyTwoWeekHigh']}</td>
                    </tr>
                    <tr>
                        <th>52 Week Low</th>
                        <td>{fundamentalsData['historicGrowth']['fiftyTwoWeekLow']}</td>
                    </tr>
                    <tr>
                        <th>Float Shares</th>
                        <td>{fundamentalsData['historicGrowth']['floatShares']}</td>
                    </tr>
                    <tr>
                        <th>Beta</th>
                        <td>{fundamentalsData['historicGrowth']['beta']}</td>
                    </tr>
                    <tr>
                        <th>Divdend Rate</th>
                        <td>{fundamentalsData['historicGrowth']['dividendRate']}</td>
                    </tr>
                </tbody>
            </Table>

            <Table striped bordered hover variant="dark">

                <tbody>
                    <tr><td colspan="2">Future Estimates</td></tr>
                    <tr>
                        <th>Earnings Quarterly Growth</th>
                        <td>{fundamentalsData['futureEstimates']['earningsQuarterlyGrowth']}</td>
                    </tr>
                    <tr>
                        <th>Revenue Quarterly Growth</th>
                        <td>{fundamentalsData['futureEstimates']['revenueQuarterlyGrowth']}</td>
                    </tr>
                    <tr>
                        <th>Price To Sales Ratio</th>
                        <td>{fundamentalsData['futureEstimates']['priceToSales']}</td>
                    </tr>
                    <tr>
                        <th>Price To Book Ratio</th>
                        <td>{fundamentalsData['futureEstimates']['priceToBook']}</td>
                    </tr>
                    <tr>
                        <th>Short Ratio</th>
                        <td>{fundamentalsData['futureEstimates']['shortRatio']}</td>
                    </tr>
                    <tr>
                        <th>Short Interest</th>
                        <td>{fundamentalsData['futureEstimates']['shortInterest']}</td>
                    </tr>
                </tbody>
            </Table>

        </div>
    );
}

function SentimentAnalysisGraph (props) {

    const [movingAverages, setMovingAverages] = useState([]);
    const { ref } = useRef();

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
          },
        },
        elements: {
            line: {
                borderWidth: 1,
            }
        },
    };

    useEffect( () => {
        const modified_averages_route = MOVING_AVERAGES_ROUTE.replace('{COMPANY}', props.company)
                                                             .replace('{TIME_RANGE}', props.timeRange);
        fetch(modified_averages_route)
            .then((response) => response.json())
            .then((json_data) => setMovingAverages(json_data['data']));
    }, [props.company, props.timeRange]);

    return (
        <div class="averages-chart py-4">
        <Chart
            id="moving_averages"
            type="line"
            ref={ref}
            options={chartOptions}
            data={{
                labels: [...Array(movingAverages.length).keys()],
                datasets: [{
                    label: `${props.company} sentiment graph`,
                    data: movingAverages,
                    borderColor:  movingAverages.at(0) >= movingAverages.at(-1) ? '#FF6384': '#1ff073',
                    backgroundColor: movingAverages.at(0) >= movingAverages.at(-1) ? '#FF638480': '#1ff07380',
                }],      
            }} 
        />
        </div>
    );
}

function TabbedCompanydInfo (props) {
    
    return (
        <Tabs
        defaultActiveKey="about"
        className="mb-3"
        fill>

          <Tab eventKey="about" title="About">
            <AboutCompany company={props.company}/>
          </Tab>

          <Tab eventKey="wordcloud" title="Word Cloud">
            <WordCloud company={props.company} timeRange={props.timeRange} />
          </Tab>

          <Tab eventKey="fundamentals" title="Fundamentals">
            <CompanyFundamentals company={props.company} />
          </Tab>

          <Tab eventKey="sentiment-analysis" title="Sentiment Analysis">
            <SentimentAnalysisGraph company={props.company} timeRange={props.timeRange} />
          </Tab>

      </Tabs>
    );
}

function CompanyDetails () {

    const { companyTicker } = useParams();
    const [ basicCompanyInfo, setBasicCompanyInfo ] = useState(null);
    const [ tickerPrices, setTickerPrices ] = useState([]);
    const [ timeRange, setTimeRange ] = useState('month');

    const { ref } = useRef();

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
          },
        },
        elements: {
            line: {
                borderWidth: 1,
            }
        }
    };

    useEffect(() => {
        const modified_prices_route = TICKER_PRICES_ROUTE.replace('{COMPANY}', companyTicker)
                                                         .replace('{TIME_RANGE}', timeRange);
        fetch(modified_prices_route)
            .then((response) => response.json())
            .then((json_data) => setTickerPrices(json_data['data']));
        
        fetch(BASIC_INFO_ROUTE.replace('{COMPANY}', companyTicker))
            .then((response) => response.json())
            .then((json_data) => setBasicCompanyInfo(json_data['data']));
    }, [companyTicker, timeRange]);

    return (
        <div class="details-body">
            {basicCompanyInfo && (
                <div class="py-1">
                <h1 class="text-center text-white py-4"> {basicCompanyInfo['fullName']} </h1>
                <div class="container">
                    <p class="text-center text-white"><b class="info-title">Country of Origin:</b> {basicCompanyInfo['country']} 
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b class="info-title">Industry:</b>  {basicCompanyInfo['industry']} 
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b class="info-title">Recommendation:</b>  {basicCompanyInfo['recommendation']} </p>
                </div>
                </div>
                )
            }
            <div class="container price-chart pt-3">
                <Chart
                    id="ticker_prices"
                    type="line"
                    ref={ref}
                    options={chartOptions}
                    data={{ 
                            labels: [...Array(tickerPrices.length).keys()],

                            datasets: [{
                                label: `${companyTicker} Prices`,
                                data: tickerPrices,
                                borderColor: tickerPrices.at(0) >= tickerPrices.at(-1) ? '#FF6384': '#1ff073',
                                backgroundColor: tickerPrices.at(0) >= tickerPrices.at(-1) ? '#FF638480': '#1ff07380',
                            }],

                            
                        }} 
                />
            </div>
            <div class="container pt-5">
                <TabbedCompanydInfo company={companyTicker} timeRange={timeRange} />
            </div>
        </div>
    )
}

export default CompanyDetails;