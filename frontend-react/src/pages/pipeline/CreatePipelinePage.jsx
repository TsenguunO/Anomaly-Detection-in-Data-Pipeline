import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import { useAuthStore } from "../../stores";
import { Container, Row, Button, Col, Form, Alert } from 'react-bootstrap';
import PipelineSideBar from '../../components/PipelineSidebar';

const CreatePipelinePage = () => {
    const history = useHistory();
    const loggedInStatus = useAuthStore((state) => state.loggedInStatus);
    const [pipelineLabel, setPipelineLabel] = useState('');
    const [modelName, setModelName] = useState('');
    const [modelVersion, setModelVersion] = useState('');
    const [selectedModel, setSelectedModel] = useState('');
    const [models, setModels] = useState([]);
    const [showSuccessAlert, setShowSuccessAlert] = useState(false);

    if (!loggedInStatus) {
        history.push('/login');
    }

    // const handleSaveButtonClick = () => {
    //     setShowSuccessAlert(true);
    //     setTimeout(() => {
    //         setShowSuccessAlert(false);
    //     }, 3000);
    // };
    const handleSaveButtonClick = async () => {
        // const payload = {
        //     pipeline_name: pipelineLabel,
        // };
        CreatePipelineApi();

    
    };

    useEffect(() => {
        // event.preventDefault();
        listModelsApi();
    }, []);

    const listModelsApi = async () => {
        // event.preventDefault();
        const url = 'http://localhost:8000/api/model/get_all_models';
        const response = await fetch(url, {
          method: 'get',
          headers: {
            'Content-type': 'application/json',
          }
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
          console.log(data.model_list)
          setModels(data.model_list)
        //   return 
        }
      }

    const CreatePipelineApi = async () => {
        // event.preventDefault();
        const url = 'http://localhost:8000/api/pipeline/';
        const response = await fetch(url, {
          method: 'post',
          headers: {
            'Content-type': 'application/json',
          },
          body: JSON.stringify({
            pipeline_name:pipelineLabel
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
          // console.log(data)
          alert('success!')
        }
      }
    

    const handleModelChange = (index) => {
        const updatedModels = [...modelsSelected];
        updatedModels[index] = !updatedModels[index];
        setModelsSelected(updatedModels);
    };

    const handleNextButtonClick = () => {
        history.push('/pipeline/select');
    };

    return (
        <Container fluid className="create-pipeline-page-container">
            <Row>
                <Col md={2} className="sidebar">
                    <PipelineSideBar />
                </Col>
                <Col md={10}>
                    <Row>
                        <Col>
                            <h2>New Pipeline Label</h2>
                            <Form.Control 
                                type="text" 
                                placeholder="Enter pipeline label"
                                value={pipelineLabel}
                                onChange={(e) => setPipelineLabel(e.target.value)} 
                            />
                        </Col>
                    </Row>
                    {/* <Row className="mt-3">
                        <Col md={6}>
                            <Form.Group as={Row} className="mb-3" controlId="modelName">
                                <Form.Label column sm="4">Model Name:</Form.Label>
                                <Col sm="8">
                                    <Form.Control 
                                        type="text" 
                                        placeholder="Enter model name"
                                        value={modelName}
                                        onChange={(e) => setModelName(e.target.value)} 
                                    />
                                </Col>
                            </Form.Group>
                        </Col>
                        <Col md={6}>
                            <Form.Group as={Row} className="mb-3" controlId="modelVersion">
                                <Form.Label column sm="4">Model Version:</Form.Label>
                                <Col sm="8">
                                    <Form.Control 
                                        type="text" 
                                        placeholder="Enter model version"
                                        value={modelVersion}
                                        onChange={(e) => setModelVersion(e.target.value)} 
                                    />
                                </Col>
                            </Form.Group>
                        </Col>
                    </Row> */}
                    <Row className="mt-3">
                        <Col>
                            <Form.Group controlId="modelSelect">
                                <Form.Control as="select" value={selectedModel} onChange={(e) => setSelectedModel(e.target.value)}>
                                    <option value="">Select a model</option>
                                    {models.map((model, index) => (
                                        <option key={index} value={model.model_id}>
                                            {model.model_name}
                                        </option>
                                    ))}
                                </Form.Control>
                            </Form.Group>
                        </Col>
                    </Row>
                    <Row className="mt-3">
                        <Col>
                            {showSuccessAlert && (
                                <Alert variant="success">
                                    Save successfully!
                                </Alert>
                            )}
                        </Col>
                    </Row>
                    <Row className="mt-3 justify-content-md-center">
                        <Col md="auto">
                            <Button onClick={handleSaveButtonClick} className="me-2">Save</Button>
                            <Button onClick={handleNextButtonClick}>Next</Button>
                        </Col>
                    </Row>
                </Col>
            </Row>
        </Container>
    );
}

export default CreatePipelinePage;
