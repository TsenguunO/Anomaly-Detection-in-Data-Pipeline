import React from 'react';
import { useHistory } from 'react-router-dom';
import { useAuthStore } from "../stores";
import { Container, Card } from "react-bootstrap";

const HomePage = () => {
    const history = useHistory();
    const loggedInStatus = useAuthStore((state) => state.loggedInStatus);

    if (!loggedInStatus) {
        history.push('/login');
    }

    const goToDatasetManagement = () => {
        history.push('/dataset/management');
    };

    const goToPipelineManagement = () => {
        history.push('/pipeline/management');
    };

    return (
        <Container className="mt-5" style={{ height: '100vh' }}>
            <div className="d-flex flex-column align-items-stretch justify-content-center h-100">
                <Card onClick={goToDatasetManagement} className="mb-3" style={{ cursor: 'pointer' }}>
                    <Card.Body className="d-flex align-items-center justify-content-center" style={{ height: '40vh' }}>
                        <Card.Title style={{ fontSize: '2rem' }}>Dataset Management</Card.Title>
                    </Card.Body>
                </Card>
                <Card onClick={goToPipelineManagement} style={{ cursor: 'pointer' }}>
                    <Card.Body className="d-flex align-items-center justify-content-center" style={{ height: '40vh' }}>
                        <Card.Title style={{ fontSize: '2rem' }}>Pipeline Management</Card.Title>
                    </Card.Body>
                </Card>
            </div>
        </Container>
    );
}

export default HomePage;
