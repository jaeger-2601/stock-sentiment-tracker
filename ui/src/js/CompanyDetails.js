import { useEffect, useState, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { Chart } from 'react-chartjs-2';
import { Tabs, Tab } from 'react-bootstrap';
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

import { TICKER_PRICES_ROUTE, COMPANY_SUMMARY_ROUTE, WORD_COUNTS_ROUTE } from './Routes';

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
            <p> Fundamentals </p>
          </Tab>

          <Tab eventKey="sentiment-analysis" title="Sentiment Analysis">
            <p> Sentiment Analysis </p>
          </Tab>

      </Tabs>
    );
}

function CompanyDetails () {

    const { companyTicker } = useParams();
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
            .then((json_data) => setTickerPrices(json_data['data']))
    }, [companyTicker, timeRange]);

    return (
        <div class="details-body">
            <h1 class="text-center text-white pt-4"> {companyTicker} </h1>
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
                                borderColor: '#FF6384',
                                backgroundColor: '#FF638480',
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