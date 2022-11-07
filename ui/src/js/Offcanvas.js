import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import NavDropdown from 'react-bootstrap/NavDropdown';
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
                <Container>
                    <Offcanvas.Title id={`offcanvasNavbarLabel-expand-false`}>
                    Ranking
                    </Offcanvas.Title>
                </Container>
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