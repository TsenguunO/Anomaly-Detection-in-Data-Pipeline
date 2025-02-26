import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import Button from 'react-bootstrap/Button';
import { Link, useHistory, useLocation } from 'react-router-dom';
import { useAuthStore } from "../stores";

function Header() {
    const history = useHistory();
    const location = useLocation();
    const loggedInStatus = useAuthStore((state) => state.loggedInStatus);
    const isHomePage = location.pathname === '/';

    const authButtons = loggedInStatus ? (
        <>
            <Link to="/">
                <Button variant="light" style={{ marginRight: '10px', backgroundColor: 'white' }}>
                    <img src="/home.png" alt="Home" style={{ marginRight: '5px', height: '20px' }} />
                    Home
                </Button>
            </Link>
            <Link to="/data/initialisation">
                <Button variant="primary" style={{ marginRight: '10px' }}>
                    <img src="/data.png" alt="Data" style={{ marginRight: '5px', height: '20px' }} />
                    Data
                </Button>
            </Link>
            <Link to="/pipeline/data">
                <Button variant="success" style={{ marginRight: '10px' }}>
                    <img src="/pipeline.png" alt="Pipeline" style={{ marginRight: '5px', height: '20px' }} />
                    Pipeline
                </Button>
            </Link>
            <Button variant="secondary" onClick={() => handleLogout()}>Logout</Button>
        </>
    ) : (
        <>
            <Link to="/login"><Button variant="secondary" style={{ marginRight: '10px' }}>Login</Button></Link>  
            <Link to="/signup"><Button variant="primary">Register</Button></Link>
        </>
    );

    const handleLogout = () => {
        history.push('/login');
        useAuthStore.getState().logout();
    };

    return (
        <header className='header' style={{ borderBottom: '1px solid #dee2e6', boxShadow: '0 2px 4px rgba(0,0,0,.1)', height: '80px' }}>
            <Navbar fixed="top" style={{ backgroundColor: '#001449', height: '80px' }}>
                <Container>
                    <Row className="position-relative w-100 align-items-center">
                        <Col className="d-flex justify-content-start">
                            <Navbar.Brand className="d-flex" href="/">
                                <img src="/gptea.png" alt="LOGO" style={{ maxHeight: '100%', height: '80px', width: 'auto' }} />
                            </Navbar.Brand>
                        </Col>
                        <Col className="d-flex justify-content-end">
                            { authButtons }
                        </Col>
                    </Row>
                </Container>
            </Navbar>
        </header>
    );
}

export default Header;
