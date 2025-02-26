import { useHistory } from 'react-router-dom';
import { useAuthStore } from "../../stores";
import { Row, Col, Container } from 'react-bootstrap';
import SideBar from '../../components/Sidebar';
import AnomalyGrid from '../../components/AnomalyGrid';


const AnomaliesPage = () => {
    const history = useHistory();
    const loggedInStatus = useAuthStore((state) => state.loggedInStatus);

    if (!loggedInStatus) {
        history.push('/login');
    }
    
    return (
        <Container>
            <Row>
                <Col className="col-2">
                    <SideBar />
                </Col>
                <Col className="col-10">
                    <Container>
                        <Row>
                            <Col>
                                <h1>Data Anomalies</h1>
                            </Col>
                        </Row>
                        <Row>
                            <Col>
                                <AnomalyGrid enableActionButton="false"/>
                            </Col>
                        </Row>

                        </Container>
                </Col>
            </Row>


        </Container>
    );
}

export default AnomaliesPage;