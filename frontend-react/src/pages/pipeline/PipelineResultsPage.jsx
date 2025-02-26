import { useHistory } from 'react-router-dom';
import { useAuthStore } from "../../stores";
import { Container, Row, Button, Col } from 'react-bootstrap';
import AnomalyGrid from '../../components/AnomalyGrid';
import PipelineSideBar from '../../components/PipelineSidebar';

const PipelineResultsPage = () => {
    const history = useHistory();
    const loggedInStatus = useAuthStore((state) => state.loggedInStatus);

    if (!loggedInStatus) {
        history.push('/login');
    }
    
    const handleDoneButtonClick = () => {
        history.push('/data/anomalies');
    }
    
    return (
        <Container fluid>
            <Row>
                <Col xs={2} id="sidebar-wrapper">
                    <PipelineSideBar />
                </Col>
                <Col xs={10} id="page-content-wrapper">
                    <h1>Upload new data to dataset</h1>
                    <AnomalyGrid enableActionButton="true" />
                    <Button onClick={() => handleDoneButtonClick()}>
                        Done
                    </Button>
                </Col>
            </Row>
        </Container>
    );
}

export default PipelineResultsPage;
