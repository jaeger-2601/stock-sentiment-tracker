import Navbar from 'react-bootstrap/Navbar';
import Offcanvas from 'react-bootstrap/Offcanvas';
import Container from 'react-bootstrap/esm/Container';
import Table from 'react-bootstrap/Table';

import '../css/Offcanvas.css';


function CustomOffcanvas() {
    return (
        <>
        <Navbar.Offcanvas
              id={`offcanvasNavbar-expand-false`}
              aria-labelledby={`offcanvasNavbarLabel-expand-false`}
              placement="start"
              className="navbar-offcanvas"
            >
              <Offcanvas.Header closeButton>
                    <Offcanvas.Title id={`offcanvasNavbarLabel-expand-false`} className="offcanvas-title container">
                    Ranking
                    </Offcanvas.Title>
              </Offcanvas.Header>

              <Offcanvas.Body>
                <Table className="ticker-ranks">
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Ticker</th>
                            <th>Average Sentiment Score</th>
                            <th>Overall Sentiment</th>
                        </tr>
                    </thead>
                </Table>
              </Offcanvas.Body>
            </Navbar.Offcanvas>
        </>
    )
}

export default CustomOffcanvas