/* eslint-disable react/prop-types */
import { Container } from 'react-bootstrap';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import AnomalyCard from './AnomalyCard';

function AnomalyGrid(props) {
  const enableActionButton = props.enableActionButton;
  return (
    <Container>
      <Row xs={1} md={1} className="g-1">
        {Array.from({ length: 4 }).map((_, idx) => (
          <Col key={idx}>
            <AnomalyCard enableActionButton={enableActionButton} />
          </Col>
        ))}
      </Row>
    </Container>
  );
}

export default AnomalyGrid;