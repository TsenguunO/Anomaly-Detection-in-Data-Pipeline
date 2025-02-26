/* eslint-disable react/prop-types */
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';


function AnomalyCard(props) {
  const enableActionButton = props.enableActionButton;
  return (

        <Card border="primary" style={{ width: '50rem' }}>
          <Card.Body>
            <Card.Title>Card Title</Card.Title>
            <Container>
                <Row>
                    <Col>
                        <Card.Text>
                            Some quick example text to build on the card title and make up the
                            bulk of the card content.
                        </Card.Text>
                    </Col>
                    <Col>
                        <Card.Text>
                            Some quick example text to build on the card title and make up the
                            bulk of the card content.
                        </Card.Text>
                    </Col>
                </Row>
            </Container>

            {enableActionButton && <Button variant="primary">Go somewhere</Button>}
          </Card.Body>
        </Card>
      );
    }

export default AnomalyCard;
