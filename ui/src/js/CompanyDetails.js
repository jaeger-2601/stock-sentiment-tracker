import { useEffect, useState, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { Chart } from 'react-chartjs-2';
import { Tabs, Tab} from 'react-bootstrap';
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

import { TICKER_PRICES_ROUTE } from './Routes';

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

const options = {
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

function TabbedCompanydInfo () {
    
    return (
        <Tabs
        defaultActiveKey="about"
        className="mb-3"
        fill
      >
        <Tab eventKey="about" title="About">
          <p> About </p>
        </Tab>
        <Tab eventKey="wordcloud" title="Word Cloud">
            <p> Word Cloud </p>
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

    useEffect(() => {
        const modified_prices_route = TICKER_PRICES_ROUTE.replace('{COMPANY}', companyTicker)
                                                         .replace('{TIME_RANGE}', timeRange);
        fetch(modified_prices_route)
            .then((response) => response.json())
            .then((json_data) => {
                setTickerPrices(json_data['data'])
            })
    }, [companyTicker]);

    return (
        <div class="details-body">
            <h1 class="text-center text-white pt-4"> {companyTicker} </h1>
            <div class="container price-chart pt-3">
                <Chart
                    id="ticker_prices"
                    type="line"
                    ref={ref}
                    options={options}
                    data={{ 
                            labels: [...Array(tickerPrices.length).keys()],

                            datasets: [{
                                label: `${companyTicker} Prices`,
                                data: tickerPrices,
                                borderColor: 'rgb(255, 99, 132)',
                                backgroundColor: 'rgba(255, 99, 132, 0.5)',
                            }],

                            
                        }} 
                />
            </div>
            <div class="container pt-5">
                <TabbedCompanydInfo />
            </div>
        </div>
    )
}

export default CompanyDetails;