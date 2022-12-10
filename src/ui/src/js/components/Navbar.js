import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import CustomOffcanvas from './Offcanvas';

function CustomNavbar() {
  return (
    <>
        <Navbar key={false} expand={false} variant="dark" bg="dark">
          <Container fluid>
          <Navbar.Toggle aria-controls={`offcanvasNavbar-expand-false`} />
            <Navbar.Brand href="#" placement="start">Stock Sentiment Analysis</Navbar.Brand>
            <Navbar.Text >Made by: <u>Harshaa Vardaan</u></Navbar.Text>
            <CustomOffcanvas/>
          </Container>
        </Navbar>
    </>
  );
}

export default CustomNavbar;