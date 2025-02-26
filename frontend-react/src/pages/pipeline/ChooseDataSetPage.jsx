import React, { useEffect, useState } from 'react';
import { useHistory } from 'react-router-dom';
import { useAuthStore, usePipelineStore } from "../../stores";
import { Container, Row, Button, Col, Form } from 'react-bootstrap';
import PipelineSideBar from '../../components/PipelineSidebar';

const ChooseDataSetPage = () => {
    const history = useHistory();
    const loggedInStatus = useAuthStore((state) => state.loggedInStatus);
    const loggedInUserEmail = useAuthStore((state) => state.loggedInUser);
    const setTargetDataSetName = usePipelineStore((state) => state.setTargetDataSetName);
    const [dropdownData, setDropdownData] = useState([]);
    const [selectedDataset, setSelectedDataset] = useState('');
    const [email, setEmail] = useState(localStorage.getItem('email'));

    useEffect(() => {
        if (!loggedInStatus) {
            history.push('/login');
        } else {
            listDatasetsApi();
        }
    }, [loggedInStatus, email, history]);

    const listDatasetsApi = async () => {
        // event.preventDefault();
        const url = 'http://localhost:8000/api/dataset/list_user_datasets';
        const response = await fetch(url, {
          method: 'post',
          headers: {
            'Content-type': 'application/json',
          },
          body: JSON.stringify({
            email: loggedInUserEmail
          }),
        });
        const data = await response.json();
        if (data.error) {
          // errorDialog
          alert(data.error)
        } else {
          // localStorage.setItem('token', data.token)
          // localStorage.setItem('email', email)
          // props.setToken(data.token);
          // navigate('/dashboard');
          // navigate('/');
          console.log(data.tables)
          setDropdownData(data.tables)
        //   return 
        }
      }

    const handleNextButtonClick = () => {
        if (selectedDataset) {
            history.push('/pipeline/select', { selectedDataset });
        } else {
            alert("Please select a dataset first.");
        }
    };

    const handleUploadNewDataset = () => {
        history.push('/pipeline/update');
    };

    const handleSetSelectedDataset = (selectedValue) => {
        setTargetDataSetName(selectedValue);
        setSelectedDataset(selectedValue);
    };

    return (
        <Container fluid className="choose-dataset-page-container">
            <Row>
                <Col md={2} className="d-none d-md-block">
                    <PipelineSideBar />
                </Col>
                <Col md={10}>
                    <Row className="justify-content-md-center">
                        <h1>Choose Data Set for Pipeline</h1>
                    </Row>
                    <Row className="justify-content-md-center">
                        <Form.Group controlId="datasetSelect" className="mb-3">
                            <Form.Control 
                                as="select"
                                className="dataset-select"
                                onChange={(e) => handleSetSelectedDataset(e.target.value)}
                                value={selectedDataset}
                            >
                                <option value="">Select a dataset</option>
                                {dropdownData.map((item, index) => (
                                    <option key={index} value={item}>
                                        {item}
                                    </option>
                                ))}
                            </Form.Control>
                        </Form.Group>
                    </Row>
                    <Row className="justify-content-md-center">
                        <Col md={3} className="text-center mb-3">
                            <Button variant="secondary" onClick={handleUploadNewDataset}>Upload New Dataset</Button>
                        </Col>
                        <Col md={3} className="text-center">
                            <Button variant="primary" onClick={handleNextButtonClick}>Next</Button>
                        </Col>
                    </Row>
                </Col>
            </Row>
        </Container>
    );
}

export default ChooseDataSetPage;
