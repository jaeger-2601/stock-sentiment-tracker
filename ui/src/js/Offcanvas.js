import Navbar from 'react-bootstrap/Navbar';
import Offcanvas from 'react-bootstrap/Offcanvas';
import Table from 'react-bootstrap/Table';

import { useState, useEffect } from 'react';

import { TICKERS_INFO_ROUTE } from './Routes';

import '../css/Offcanvas.css';


function TickerTable(props) {

    const sentimentCssTable = {
        'Positive': 'pos',
        'Slightly Positive':'sli-pos',
        'Neutral':'neu',
        'Slightly Negative':'sli-neg',
        'Negative':'neg'
    };

    return (
        <>
        <Table className="ticker-ranks">
            <thead>
            <tr>
                <th>Rank</th>
                <th>Ticker</th>
                <th>Average Sentiment Score</th>
                <th>Overall Sentiment</th>
            </tr>
            </thead>
            
            <tbody>
              {
              props.tickerInfo.map(data => (
                <tr key={data['rank']}>
                    <td>{data['rank']}</td>
                    <td>
                        <a href={`/company/${data['company']}`} className="ticker-name">{data['company']}</a>
                    </td>
                    <td className={`sentiment-${sentimentCssTable[data['sentiment']]}`}>{data['score'].toFixed(3)}</td>
                    <td className={`sentiment-${sentimentCssTable[data['sentiment']]}`}>{data['sentiment']}</td>
                </tr>
              ))
              }
            </tbody>
        </Table>
        </>
    )
}

function CustomOffcanvas() {

    const [tickerInfo, setTickerInfo] = useState([]);

    useEffect(() => {
        fetch(TICKERS_INFO_ROUTE)
            .then((response) => response.json())
            .then((json_data) => {

                // Add overall sentiment attribute to data
                json_data['data'].map( data => {
                    if (data['score'] > 0.19) { data['sentiment'] = 'Positive'; }
                    else if (data['score'] > 0.13) { data['sentiment'] = 'Slightly Positive'; }
                    else if (data['score'] > 0) { data['sentiment'] = 'Neutral'; }
                    else if (data['score'] > -0.1) { data['sentiment'] = 'Slightly Negative'; }
                    else { data['sentiment'] = 'Negative'; }
                });

                // Set ticker info
                setTickerInfo(json_data['data'])
            });
    }, []);

    return (
        <>
        <Navbar.Offcanvas
              id={`offcanvasNavbar-expand-false`}
              aria-labelledby={`offcanvasNavbarLabel-expand-false`}
              placement="start"
              className="navbar-offcanvas"
            >
              <Offcanvas.Header closeButton className='offcanvas-header'>
                    <Offcanvas.Title id={`offcanvasNavbarLabel-expand-false`} className="offcanvas-title container border-bottom">
                    Ranking
                    </Offcanvas.Title>
              </Offcanvas.Header>

              <Offcanvas.Body className='offcanvas-body'>
                <TickerTable tickerInfo={tickerInfo}/>
              </Offcanvas.Body>
            </Navbar.Offcanvas>
        </>
    )
}

export default CustomOffcanvas